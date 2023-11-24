try:
    from flask import Flask, request, json, render_template
    from dateutil.tz import *
    from flask_restful import Resource,Api
    from flask_restful import reqparse
    from flask import request
    import time
#    import RPi.GPIO as GPIO
    from datetime import datetime
    import json
#    import dht11
    import os
    import subprocess
    import json
    print("All Module loaded")
except Exception as e:
    print("Error: {}".format(e))


#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#instance = dht11.DHT11(pin=17)

app = Flask(__name__)
api = Api(app)
#globals
IsbridgeCommissioned=False;
appliance_nodeid_dict = {"pairing": {"pbulb1":"1234", "pbulb2":"2345", "bridge1":"110"}, "onoff":{"pbulb1":"110","pbulb2":"110", "partymode":"110", "discobulb": "110"}}
gcreds={"uname": "noname", "passwd": "noname", "deviceip": "8.8.8.8"}
#global ends
def formatstring(pwdstr):
    nonumalphastr="!@#$%^&*?"
    newnewstr=""
    for i in pwdstr:
        ret = nonumalphastr.find(i)
        if(ret != -1):
            newnewstr+= "\\"
        newnewstr+=i   
    return newnewstr




@app.route('/logifun', methods=['POST'])
def logifun():
    global gcreds
    gcreds["uname"] = request.form["fname"]
    gcreds["deviceip"] = request.form["ipaddress"]
    val1 = request.form["pwd"]
    gcreds["passwd"] = formatstring(val1)
    value = {"creds":"Entered"}
    print(gcreds, ":pwd!!!")
    s = subprocess.check_output(["ip addr show eth0 | grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"], stdin=None, stderr=None, shell=True, universal_newlines=True)
    s1 = s[0:len(s)-1]
    value = {"ipaddr":s1}
    print(value["ipaddr"], s1)
    
    snapdatacomvar = os.environ.get('SNAP_DATA')

    s2 = CheckForPairingSuccess(snapdatacomvar, appliance_nodeid_dict["pairing"]["pbulb1"])
    value["bulb1state"] =  "notcommissioned"
    if(s2["Pairing"] == "Success"):
        value["bulb1state"] =  "commissioned"
    
    s2 = CheckForPairingSuccess(snapdatacomvar, appliance_nodeid_dict["pairing"]["pbulb2"])
    value["bulb2state"] =  "notcommissioned"
    if(s2["Pairing"] == "Success"):
        value["bulb2state"] =  "commissioned"
   
    s2 = CheckForPairingSuccess(snapdatacomvar, appliance_nodeid_dict["pairing"]["bridge1"])
    value["bulb2state"] =  "notcommissioned"
    if(s2["Pairing"] == "Success"):
        value["bridge1state"] =  "commissioned"

    print(value)    
    return render_template('login.html', **value)


@app.route("/" , methods=['POST', 'GET'])
def index():
    s = subprocess.check_output(["ip addr show eth0 | grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"], stdin=None, stderr=None, shell=True, universal_newlines=True)
    s1 = s[0:len(s)-1]
    value = {"ipaddr":s1}
    print(value["ipaddr"], s1)
    return render_template('wificreds.html', **value)
"""
prash@canonical -: This is working method
@app.route("/")
def index():
    s = subprocess.check_output(["ip addr show eth0 | grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"], stdin=None, stderr=None, shell=True, universal_newlines=True)
    s1 = s[0:len(s)-1]
    value = {"ipaddr":s1}
    print(value["ipaddr"], s1)
    return render_template('login.html', **value)

"""
def CheckForPairingSuccess(pathname, nodeid):
    global IsbridgeCommissioned
    try:
        fname=pathname + "/"
        fname+=nodeid + "_pairres.json"
        print(pathname, fname)
        fp1=open(fname, "r")
        res=json.load(fp1)
        print(res["Results"][0])
        fp1.close()
        if(res["Results"][0]["Pairing"] == "Success" and res["Results"][0]["nodeid"] == appliance_nodeid_dict["pairing"]["bridge1"]):
            IsbridgeCommissioned=True
        return res["Results"][0] 
    except IOError:
        print("File not found")
        return {"Pairing":"Failure", "nodeid": "0"}
    """
    finally: 
        print("Exit")
        return {"Pairing":"Failure", "nodeid": "0"}
    """

def CheckForClusterCmdSuccess(pathname, clustername, secondargs):
    try:
        fname=pathname + "/"
        fname+=clustername + "_" + secondargs + ".json" 
        print(pathname, fname)
        fp1=open(fname, "r")
        res=json.load(fp1)
        print(res["Results"][0])
        fp1.close()
        os.unlink(fname)
        return res["Results"][0] 
    except IOError:
        print("File not found")
        return {"CmdRes":"Success", "Command": secondargs}
    
def GetEndPointForCmd(appliancename):
    ep="0"
    if(appliancename == "pbulb1"):
        ep="1"
    elif(appliancename == "pbulb2"):
        ep="2"
    elif(appliancename == "partymode"):
        ep="4"
    elif(appliancename == "discobulb"):
        ep="3"
    return ep

"""
Note that nodeid 1234 and nodeid 2345 are used for simple bulbs not the bulbs connected to bridge
for the bulbs connected to bridge the nodeid will be 110

"""
def GetNodeid(appliancename, clustername):
    print(appliancename, clustername, IsbridgeCommissioned)
    if(clustername == "pairing"):
        return appliance_nodeid_dict["pairing"].get(appliancename, "Not Found")
    elif(clustername == "onoff"):
        if(IsbridgeCommissioned == True):
            print(appliancename, "::", appliance_nodeid_dict["onoff"][appliancename])
            return appliance_nodeid_dict["onoff"][appliancename]
        else:
            return appliance_nodeid_dict["pairing"].get(appliancename, "Not Found")




@app.route('/login', methods=['GET'])
def PairCall():
    flipstate={"on": "off", "off": "on"} #for on/off commands
    togglestate={"on": "toggle", "off": "toggle"} #for toggle commands
    nodeid="1234"
    clustername="pairing"
    pairdict = {"Pairing":"Failure", "nodeid": "0"} 
    snapdatavar = os.environ.get('PATH')
    snapvar = os.environ.get('SNAP')
    snapdatacomvar = os.environ.get('SNAP_DATA')
    pathvar=snapvar
    pathvar+="/extra-bin/chip-tool "
    #cmdextraparams="20202021 3840 192.168.1.73 5543" #ethernet pairing cluster
    cmdextraparams=gcreds["uname"] + " " + gcreds["passwd"] + " 20202021 3840"   #ble-wifi pairing cluster
    
    reqargs=request.args.to_dict()
    firstarg=reqargs.get("name")
    secondargs=reqargs.get("bulbstate", "commission")
    
    if(secondargs == "commission"):
        pathvar+="pairing ble-wifi "
    elif(secondargs == "commissionbridge"):
        #pathvar+="pairing onnetwork "
        #cmdextraparams="20202021 "
        pathvar+="pairing ethernet "
        cmdextraparams="20202021 3840 " + gcreds["deviceip"] + " " + "5540"
    elif(secondargs == "off" or secondargs == "on"):
        clustername = "onoff"
        if(firstarg== "pbulb1" or firstarg == "pbulb2"):
            pathvar+="onoff " + togglestate[secondargs] + " "
        else:
            pathvar+="onoff " + togglestate[secondargs] + " "

        cmdextraparams = GetEndPointForCmd(firstarg)

    if (firstarg == None):
        pairdict["Pairing"] = "Invalid Query"
        return json.dumps(pairdict)
    else:
        nodeid=GetNodeid(firstarg, clustername)

    pathvar+=nodeid + " "
 
    pathvar+=cmdextraparams

    print(snapvar, snapdatavar, snapdatacomvar,"\n", pathvar, "\n")
    subprocess.call([pathvar], stdin=None, stderr=None, shell=True, universal_newlines=True)
    
    if(secondargs[0:10] == "commission"):
        s1 = CheckForPairingSuccess(snapdatacomvar, nodeid)
        print(s1)
    elif(secondargs == "off" or secondargs == "on"):
        s1 = CheckForClusterCmdSuccess(snapdatacomvar, clustername, flipstate[secondargs])
        print(s1)

    return json.dumps(s1)

"""
def index():
    snapdatavar = os.environ.get('PATH')
    snapvar = os.environ.get('SNAP')
    snapdatacomvar = os.environ.get('SNAP_COMMON')
    pathvar=snapvar
    pathvar+="/extra-bin/chip-tool pairing ethernet 1 20202021 3840 192.168.1.73 5543"
    print(snapvar, snapdatavar, snapdatacomvar, pathvar)
    subprocess.call([pathvar], stdin=None, stderr=None, shell=True, universal_newlines=True)
    local = tzlocal()
    now = datetime.now()
    now = now.replace(tzinfo = local)
    timeString = now.strftime("%Y-%m-%d   %H:%M")
    temperature, humidity = sensor_DHT11()
    templateData = {'title':'Home Page','time':timeString,'temperature':temperature, 'humidity':humidity}
    return render_template('sensor.html', **templateData)
"""
"""
def sensor_DHT11():
    while True:
            result= instance.read()
            if result.is_valid():

                                
                return result.temperature, result.humidity
"""                    
"""    
def sensor_DHT11():
    counter=0
    while(counter < 10):
            #result= instance.read()
            #if result.is_valid():

                                
             #   return result.temperature, result.humidity
            #else:
        counter=counter+1
        time.sleep(1)

    return "no data", "no data"    
"""


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)
