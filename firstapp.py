# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from flask import render_template
import os
import json
from devicelist import DeviceList
import subprocess
devicelist1 = None
reqipaddr = None
DeviceDataBase= None
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 
def CheckForPairingSuccess(pathname, nodeid):
    try:
        fname=pathname + "/"
        fname+=nodeid + "_pairres.json"
        print(pathname, fname)
        fp1=open(fname, "r")
        res=json.load(fp1)
        print(res["Results"][0])
        fp1.close()
        return res["Results"][0] 
    except IOError:
        print("File not found")
        return {"Pairing":"Failure", "nodeid": "0"}

# ‘/devicelist’ URL is bound with hello_world() function.
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
#json.dump returns a string not the json so please be mindful



@app.route('/CommissionMatterDevice', methods=['GET'])
def PairCall():
    global devicelist1
    global DeviceDataBase
    global reqipaddr
    reqargs=request.args.to_dict()
    deviceidx=reqargs.get("index")
    pairparams = DeviceList.GetDevicePairingParams(devicelist1, DeviceDataBase["devices"], deviceidx)
    snapvar = os.environ.get('SNAP')
    snapdatacomvar = os.environ.get('SNAP_DATA')
    pathvar=snapvar
    pathvar+="/extra-bin/chip-tool.sh " + snapvar + "/extra-bin/chip-tool "
    pathvar+= "pairing" + " " + pairparams[1][0] + " " + pairparams[0] + " " 
    if pairparams[1][0] == "ethernet":
        tmpdict=pairparams[1][1]
        print(type(tmpdict["port"]))
        pathvar+= tmpdict["PINCode"] + " " + tmpdict["Discriminator"] + " " + tmpdict["ip"] + " " + tmpdict['port']
    elif pairparams[1][0] == "ble-wifi":
        passwd=DeviceList.formatstring(pairparams[1][1]["passwd"])
        tmpdict=pairparams[1][1]
        pathvar+= tmpdict["ssid"] + " " + passwd + " " + tmpdict["PINCode"] + " " + tmpdict["Discriminator"]
    elif pairparams[1][0] == "onnetwork":
        tmpdict=pairparams[1][1]
        pathvar+= tmpdict["PINCode"]
    elif pairparams[1][0] == "code-thread":
        tmpdict=pairparams[1][1]
        print(tmpdict)
        pathvar+= tmpdict["thnwopsDataset"] + " " + tmpdict["QRCode"] + " "
        if tmpdict["productiondev"] == "1":
            pathvar+= "--paa-trust-store-path" + " " + "pemcerts" 
		
    print(pathvar)
    subprocess.call([pathvar], stdin=None, stderr=None, shell=True, universal_newlines=True)
    s1 = CheckForPairingSuccess(snapdatacomvar, pairparams[0])
    return json.dumps(s1)

@app.route('/UnpairAll', methods=['GET'])
def UnapairAll():
    snapdatacomvar = os.environ.get('SNAP_DATA')
    fname=snapdatacomvar + "/"
    fname+="*_pairres.json"
    cmd="rm -f /tmp/chip_* /mnt/chip_*" + " "  + fname
    print(cmd)
    subprocess.call([cmd], stdin=None, stderr=None, shell=True, universal_newlines=True)
    return json.dumps({"UnPairAll":"Success"})

@app.route('/UnpairMatterDevice', methods=['GET'])
def UnpairCall():
    global devicelist1
    global DeviceDataBase
    global reqipaddr
    reqargs=request.args.to_dict()
    deviceidx=reqargs.get("index")
    pairparams = DeviceList.GetDevicePairingParams(devicelist1, DeviceDataBase["devices"], deviceidx)
    snapvar = os.environ.get('SNAP')
    snapdatacomvar = os.environ.get('SNAP_DATA')
    pathvar=snapvar
    pathvar+="/extra-bin/chip-tool.sh " + snapvar + "/extra-bin/chip-tool "
    pathvar+= "pairing" + " " + "unpair" + " " + pairparams[0];
    print(pathvar)
    subprocess.call([pathvar], stdin=None, stderr=None, shell=True, universal_newlines=True)
    fname=snapdatacomvar + "/"
    fname+=pairparams[0] + "_pairres.json"
    print("deleting::=>", fname)
    os.unlink(fname)
    return json.dumps({"Unpairing":"Success"})

def getip():
    global reqipaddr
    ifacename=os.environ.get('NWIFACE')
    print(ifacename)
    ipstring = "ip addr show " + ifacename + "| grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"      
    s = subprocess.check_output([ipstring], stdin=None, stderr=None, shell=True, universal_newlines=True)
    if len(s) != 0:
        reqipaddr = s[0:len(s)-1]
    


@app.route('/')
def hello_world():
    global devicelist1
    global DeviceDataBase
    global reqipaddr
    if devicelist1 is None:
        devicelist1 = []
    if reqipaddr is None:
        reqipaddr = "127.0.0.1"
    if DeviceDataBase is None:
        DeviceDataBase = {}
    getip()    
    pathname=os.environ.get('TMPDIR')
    fname=pathname + '/devicelist.json'
    DeviceDataBase=DeviceList.getdata(fname)
    devicelist1=DeviceList.GetDeviceList(DeviceDataBase["devices"]);
    #devicelist=json.dumps(devicelist1)
    #devicelist = {"name1": "Prashant", "name2": "Amruta", "name3":"Gargi"};
    #print(devicelist1)
    isdebug=os.environ.get('DEBUG')
    if isdebug == "true": #This is original woking code as on Aug17 2023 	
        return render_template('/login_dummy.html', ipaddr=reqipaddr, devicelist=devicelist1)
    elif isdebug== "false":
        return render_template('/login_dummy_nodbg.html', ipaddr=reqipaddr, devicelist=devicelist1)
    else:    
        return render_template('/login_dummy.html', ipaddr=reqipaddr, devicelist=devicelist1)
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0', debug=True, port=5001)
