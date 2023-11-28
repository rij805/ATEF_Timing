import subprocess
import config
from datetime import datetime
import json

print("Hutch code list: \n\nCXI_FS5: 5  \nMEC_FS6: 6  \nMFX_FS4.5: 45  \nNEH_FS11: 11 \nNEH_FS14: 14  \nXCS_FS4: 4\n")
hutch_code = input("Enter hutch code: ")
hutch_dict = {"5" : "CXI_FS5", "6" : "MEC_FS6",  "45" : "MFX_FS4.5",  "11" : "NEH_FS11", "14" : "NEH_FS14",  "4" : "XCS_FS4"}
hutch = hutch_dict[hutch_code]
folder= "/cds/home/r/rj1/atef/timing_config/"+ hutch + "/"
ioc_path = folder + hutch + '_IOC.txt'

subprocess.run(["mkdir", "-p", folder + "temp/"])
pv_lists_path = folder + "temp/" + "pv_lists/"

subprocess.run(["mkdir", "-p", pv_lists_path])

total_iterations = int(input("Enter total iterations of random sampling: "))
interval = float(input("Enter max interval of each iteration in seconds: "))





with open(ioc_path, 'r') as readtxt:
    ioc_list = [line.strip() for line in readtxt.readlines()]
    print("Estimated wait time: " + str(int(len(ioc_list) * total_iterations * (interval/2) / 60 + 2)) + " minutes.")
    for ioc in ioc_list:
        #print("Getting .pvlist file from " + ioc)
        subprocess.run(["cp", "/cds/data/iocData/"+ ioc +"/iocInfo/IOC.pvlist", pv_lists_path + ioc +"_IOC.pvlist"])
        config.run_config_json(hutch, ioc, ioc_list.index(ioc), (ioc_list.index(ioc)+1)/len(ioc_list), folder, pv_lists_path + ioc +"_IOC.pvlist", pv_lists_path + "new_" + ioc +"_IOC.pvlist", total_iterations, interval)






        
with open(folder + hutch + ".json", 'r') as openfile:
    # Reading from json file
    config_template = json.load(openfile)   

#Adding hutch name in JSON    
if config_template["root"]["name"] != hutch:
    config_template["root"]["name"] = hutch

#Adding timestamp in JSON
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
config_template["root"]["description"] = date_time
    
del config_template["root"]["configs"][0]
print("date and time:",date_time)  
print("Done")

