tic()
using HttpServer, HTTP, WebSockets, GSReg, HttpServer.mimetypes
using DataFrames
using Mux, Mux.stack, CSV, JSON, HttpCommon, DataStructures
using DotEnv

DotEnv.config()
println("Package loading took this long: ", toq())

const SERVER_BASE_DIR = "./static"
const GSREG_VERSION = Pkg.installed("GSReg")

struct GSRegJob
    file # tempfile of data
    hash # hash id of user
    options # options for calculation
    id # unique identifier for this job
    time_enqueued # time enqueued
    GSRegJob(file, hash, options) = new(file, hash, options, string(Base.Random.uuid4()), time())
end

files_dict = Dict{String,String}()

job_queue = Queue(GSRegJob)
job_queue_cond = Condition()

#Consume job_queue after notification
@schedule begin
    while true
        info("waiting for new jobs")
        wait(job_queue_cond)
        while !(isempty(job_queue))
            info("job consumed")
            gsreg(dequeue!(job_queue))
        end
        info("jobs consumed")
    end
end

"""
    Enqueue the job and notify worker
"""
function enqueue_job(job::GSRegJob)
    global job_queue
    global job_queue_cond
    enqueue!(job_queue, job)
    info("job enqueued")
    notify(job_queue_cond)
    job
end

function sendMessage(id::String, data)
    global connections
    if haskey(connections, id)
        ws = connections[id]
        sendMessage(ws, data)
    end
end

function sendMessage(ws::WebSocket, data)
    writeguarded(ws, JSON.json(data))
end

function gsreg(job::GSRegJob)
    try
        sendMessage(job.hash, Dict("operation_id" => job.id, "message" => "Reading data"))
        data = CSV.read(job.file)
        sendMessage(job.hash, Dict("operation_id" => job.id, "message" => "Executing GSReg"))

        opt = job.options["options"]

        res = GSReg.gsreg(job.options["depvar"] * " " * join(job.options["expvars"], " "), data; opt...,
                    onmessage = message -> sendMessage(job.hash, Dict("operation_id" => job.id, "message" => message)) )
        sendMessage(job.hash, Dict("operation_id" => job.id, "done" => true, "message" => "Successful operation", "result" => GSReg.to_dict(res)))
    catch e
        io = IOBuffer()
        showerror(io, e)
        sendMessage(job.hash, Dict("operation_id" => job.id, "done" => false, "message" => String(take!(io))))
    end
end

"""
    Log request for analytics and debugging
"""
function logRequest(app, req)
    log = string(
        task_local_storage(:ip), " ",
        get(req[:headers], "Host", ""), " ",
        get(req[:headers], "Origin", ""), " ",
        Libc.strftime("%d/%b/%Y:%H:%M:%S %z", time()), " ",
        "\"", req[:method], " ", req[:resource], "\"", " ",
        size(req[:data],1), "B",
        "\n")

    open("access.log","a") do fp
        write(fp, log)
    end
    app(req)
end

"""
    Try to execute controller and if there is any exception, show exception message
"""
function errorCatch(app, req)
    try
        app(req)
    catch e
        io = IOBuffer()
        showerror(io, e)
        err_text = String(take!(io))
        log = string(Libc.strftime("%d-%b %H:%M:%S", time()), " ", err_text, "\n")
        open("error.log","a") do fp
            write(fp, log)
        end
        toJsonWithCors(Dict("message" => err_text, "error" => true), req)
    end
end

"""
    Setting CORS headers and parsing it to JSON
"""
function toJsonWithCors(res, req)
    headers  = HttpCommon.headers()
    if( req[:method] != "OPTIONS" )
        headers["Content-Type"] = "application/json; charset=utf-8"
    end
    headers["Access-Control-Allow-Headers"] = "X-User-Token, Content-Type"
    if get(req[:headers], "Origin", "") == "http://localhost:8080"
        headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    else
        headers["Access-Control-Allow-Origin"] = "https://app.gsreg.org"
    end

    Dict(
        :headers => headers,
        :body => (req[:method] == "OPTIONS") ? "" : JSON.json(res)
    )
end

"""
    Get Auth from header, and reply an error when it's not present
"""
function authHeader(app, req)
    if(haskey(req[:headers], "X-User-Token"))
        req[:token] = get(req[:headers], "X-User-Token", "")
        app(req)
    else
        error("X-User-Token header it's required")
    end
end

function cloudLimits(data, options)
    error("The selected formula it's too large to be computed online. To perform this operation please install Julia and GSReg.jl in your local environment, initialize Julia and run the following command:" * constructCommand(options))
end

function constructCommand(options)
    command = """Pkg.add("GSReg")
using GSReg, CSV
data = CSV.read("yourcsvfile.csv")
res = GSReg.gsreg("", data; opts...)"""
end

"""
    TODO:
"""
function validateInput(opt)
    """
    # Input should be a dict with the next required keys:
    "workers": ?
    "depvar": String,
    "expvars": [String],
    "options":
        "intercept": Boolean,
        "time": String,
        "residualtest": Boolean,
        "keepwnoise": Boolean,
        "ttest": Boolean,
        "orderresults": Boolean,
        "modelavg": Boolean,
        "outsample": Integer,
        "csv": String,
        "method": String,
        "criteria": ["r2adj","bic","aic","aicc","cp","rmse","rmseout","sse"]
    """

    options = Dict{Symbol,Any}()
    opt_types = Dict(
        "intercept" => Bool,
        "time" => string,
        "residualtest" => Bool,
        "keepwnoise" => Bool,
        "ttest" => Bool,
        "orderresults" => Bool,
        "modelavg" => Bool,
        "outsample" => Integer,
        "csv" => string,
        "method" => string,
        "criteria" => Array{Symbol}
    )
    for (name, value) in opt["options"]
        if value != nothing
            println(name, value)
            push!(options, Pair(Symbol(name), opt_types[name](value)) )
        end
    end
    opt["options"] = options
    opt
end

"""
    Receives base64 encoded data in path with regression
    options and a content body with CSV file for processing

    req[:data] -> Array{UInt8,1}
    req[:params][:b64] -> String
"""
function upload(req)
    tic()

    """
    Save the file to tmp folder, if there is any exception, it should be returned to the user for
    reuse. It must be available until the user explicit deletes it, or its deleted from
    operating system. If it is deleted, the file must be uploaded again.
    """
    tempfile = try
        temp = tempname()
        write(temp, IOBuffer(req[:data]))
        temp
    catch
        error("We can't save that file, try again later.")
    end

    """
    Check csv parsing & get data
    """
    data = try
        CSV.read(IOBuffer(req[:data]))
    catch
        error("The file must be a valid CSV")
    end

    # if we're in cloud solution, limit upload to 100MB
    if ( haskey(ENV, "ENVIRONMENT") && ENV["ENVIRONMENT"] == "cloud" )
        if ( filesize(tempfile) > 100 * (1000 ^ 2) )
            error("Max filesize (100MB) exceeded")
        end
    end

    global files_dict
    id = string(Base.Random.uuid4())
    push!(files_dict, Pair(id, tempfile))

    Dict(
        "filename" => id,
        "datanames" => names(data),
        "nobs" => size(data, 1)
    )
end

function server_info(req)
    global job_queue
    Dict(
        "ncores" => Sys.CPU_CORES,
        "nworkers" => nworkers(),
        "gsreg_version" => string(GSREG_VERSION),
        "julia_version" => string(VERSION),
        "job_queue" => Dict(
            "length" => length(job_queue)
        )
    )
end

"""
    Enqueue the execution of regressions, expecting a confirmation. If any there is any error, should be a detailed report.
"""
function solve(req)
    """
    Try to get the filename from params
    """
    global files_dict

    if haskey(files_dict, req[:params][:hash])
        tempfile = files_dict[req[:params][:hash]]
        if (!isfile(tempfile))
            error("File was deleted")
        end
    else
        error("Filekey inexistent")
    end

    """
    Input options should be a valid base64:json encoded String.
    """
    options = try
        b64 = convert(String, req[:params][:options])
        JSON.parse(String(base64decode(b64)))
    catch
        error("Bad format in options")
    end

    # validate correct use of options
    opt = validateInput(options)

    # if we're in cloud solution, skip computations larger than our capabilities
    if ( haskey(ENV, "ENVIRONMENT") && ENV["ENVIRONMENT"] == "cloud" )
        cloudLimits(data, options)
    end

    # Enqueue the job
    job = GSRegJob(tempfile, req[:token], opt)
    enqueue_job(job)

    Dict(
        "ok" => true,
        "operation_id" => job.id,
        "in_queue" => length(job_queue)
    )
end

# Array of connections based in user token
global connections = Dict{String,WebSocket}()

"""
 This WebSocket handler mantain a collection of ws opened with the user id.
"""
function wsapp(req, ws)
    global connections
    while isopen(ws)
        msg, = readguarded(ws)
        try
            msg = JSON.parse(String(copy(msg)))
            id = msg["user-token"]
            if !haskey(connections, id)
                connections[id] = ws
            end
            sendMessage(ws, Dict("ok" => true, "message" => "Waiting in queue"))
        catch
            sendMessage(ws, Dict("ok" => false, "message" => "The next message must be in JSON format"))
        end
    end
    # TODO: find some way for delete connection with any reference
    # delete!(connections, id)
end

function validpath(path; dirs = true)
    (isfile(path) || (dirs && isdir(path)))
end

ormatch(r::RegexMatch, x) = r.match
ormatch(r::Void, x) = x

extension(f) = ormatch(match(r"(?<=\.)[^\.\\/]*$", f), "")

fileheaders(f) = Dict("Content-Type" => get(mimetypes, extension(f), "application/octet-stream"))

fileresponse(f) = Dict(
                    :body => read(f),
                    :headers => fileheaders(f)
                    )

fresp(f) =
  isfile(f) ? fileresponse(f) :
  isdir(f) ?  dirresponse(f) :
  error("$f doesn't exist")

function staticfiles(dirs=true)
    branch( req -> validpath(joinpath(SERVER_BASE_DIR, req[:path]...); dirs=dirs),
            req -> fresp(joinpath(SERVER_BASE_DIR, req[:path]...)))
end

@app app = (
    stack(Mux.todict, logRequest, Mux.splitquery, errorCatch, authHeader, Mux.toresponse),
    staticfiles(false),
    page("/upload", req -> toJsonWithCors(upload(req), req)),
    page("/server-info", req -> toJsonWithCors(server_info(req), req)),
    page("/solve/:hash/:options", req -> toJsonWithCors(solve(req), req)),
    Mux.notfound()
)

# take the remote addr for logging
function handle_connect(client)
    try
        buffer = Array{UInt8}(32)
        bufflen::Int64 = 32
        ccall(:uv_tcp_getpeername, Int64, (Ptr{Void},Ptr{UInt8},Ptr{Int64}), client.sock.handle, buffer, &bufflen)
        peername::IPv4 = IPv4(buffer[5:8]...)
        task_local_storage(:ip,peername)
    catch e
        println("Error ... $e")
    end
end

handler(req, res) = app.warez(req)

http_handler = HttpHandler(handler)
http_handler.events["connect"]=(client)->handle_connect(client)

server = Server(http_handler, WebSocketHandler(wsapp))

@sync serve(server, port=parse(Int64, ARGS[1]))
