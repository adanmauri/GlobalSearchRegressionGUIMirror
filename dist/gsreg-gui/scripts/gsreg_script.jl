using CSV
using GSReg
data = CSV.read(+self.csv_filename+)
GSReg.gsreg("y x1 x2", data, intercept=true, samesample=true, criteria=[:bic], csv="/home/adanmauri/Documentos/julia/12mb_gsreg_results_20180429185126.csv", ttest=true)