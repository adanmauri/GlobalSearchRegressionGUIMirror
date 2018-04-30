pkgs = Pkg.installed();
try
    pack = pkgs["CSV"]
    if v"0.2.4" > pack
        Pkg.update("DataFrames")
    end
catch    
    Pkg.add("CSV")
end

try
    pack = pkgs["DataFrames"]
    if v"0.11.6" > pack
        Pkg.update("DataFrames")
    end
catch
    Pkg.add("DataFrames")
end

try
    pack = pkgs["GSReg"]
catch
    Pkg.clone("git@github.com:ParallelGSReg/GSReg.jl.git")
end