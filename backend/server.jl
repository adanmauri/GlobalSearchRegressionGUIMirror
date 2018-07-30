tic()
using HttpServer, HTTP, WebSockets, GSReg, HttpServer.mimetypes
using Mux, CSV, JSON, HttpCommon, DataStructures
println("Package loading took this long: ", toq())

const SERVER_BASE_DIR = ""

struct GSRegJob
    file # tempfile of data
    hash # hash id of user
    options # options for calculation
    id # unique identifier for this job
    time_enqueued # time enqueued
    GSRegJob(file, hash, options) = new(file, hash, options, Base.Random.uuid4(), time())
end

job_queue = Queue(GSRegJob)
job_queue_cond = Condition()


"""
    Consume job_queue after notification
"""
@async begin
    while(true)
        wait(job_queue_cond)
        while(!isempty(job_queue))
            gsreg(dequeue!(job_queue))
        end
    end
end

"""
    Enqueue the job and notify worker
"""
function enqueue_job(job::GSRegJob)
    global job_queue, job_queue_cond
    enqueue!(job_queue, job)
    notify(job_queue_cond)
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
        data = CSV.read(job.options.file)
        sendMessage(job.hash, Dict("operation_id" => job.id, "message" => "Executing GSReg"))
        res = gsreg(job.options["formula"], data)
        #res = gsreg(job.options["formula"], data, job.options..., onmessage = message -> sendMessage(job.hash, Dict("message" => message)))
        sendMessage(job.hash, Dict("operation_id" => job.id, "done" => true, "res" => res))
    catch
        sendMessage(job.hash, Dict("operation_id" => job.id, "message" => "Execution failed"))
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

"""
    TODO:
"""
function validateInput(options)
    options["formula"] = "y x*"
    options
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

    # TODO: validate file size, nobs and other compute limitations
    # For local executions the limit would be 25 covariates.

    Dict(
        "nworkers" => nworkers(),
        "datanames" => names(data),
        "nobs" => size(data,1),
        "filename" => tempfile
    )
end

"""
    Enqueue the execution of regressions, expecting a confirmation. If any there is any error, should be a detailed report.
"""
function solve(req)
    """
    Try to read the file from the filesystem
    """
    tempfile = try
        b64 = convert(String, req[:params][:hash])
        CSV.read(String(base64decode(b64)))
    catch
        error("The file requested doesn't exists")
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

    """
    Validate size, nobs, nvar, from input
    """
    opt = validateInput(options)

    """
    Execute regression in background, report results trough ws
    """
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
                sendMessage(ws, Dict("ok" => true, "message" => "got ya"))
            else
                sendMessage(ws, Dict("ok" => true, "message" => "loud & clear"))
            end
        catch
            sendMessage(ws, Dict("ok" => false, "message" => "the next message must be in JSON format"))
        end
    end
    delete!(connections, id)
end

function validpath(path; dirs = true)
    (isfile(path) || (dirs && isdir(path)))
end

ormatch(r::RegexMatch, x) = r.match
ormatch(r::Void, x) = x

extension(f) = ormatch(match(r"(?<=\.)[^\.\\/]*$", f), "")

fileheaders(f) = Dict("Content-Type" => get(mimetypes, extension(f), "application/octet-stream"))

fileresponse(f) = Dict(:file => f,
                    :body => read(f),
                    :headers => fileheaders(f))

fresp(f) =
  isfile(f) ? fileresponse(f) :
  isdir(f) ?  dirresponse(f) :
  error("$f doesn't exist")

function staticfiles(dirs=true)
    branch(req -> validpath(joinpath(SERVER_BASE_DIR, req[:path]..., req[:params][:resource]), dirs=dirs),
           req -> fresp(joinpath(SERVER_BASE_DIR, req[:path]..., req[:params][:resource])))
end

@app app = (
    stack(Mux.todict, logRequest, Mux.splitquery, errorCatch, authHeader, Mux.toresponse),
    route("/static/:resource", staticfiles(false)),
    page("/upload", req -> toJsonWithCors(upload(req), req)),
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
