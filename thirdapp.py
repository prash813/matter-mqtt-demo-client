
import tinytuya_monitor as tinytuyaapp
from flask import Flask, request jsonify
from flask import render_template
from devicelist import DeviceList
from OpModes import OpModes 
from matterbulbop import MatterBulbOp
import os
import subprocess
import json
from threading import Thread
import paho.mqtt.client as mqtt
import time
import sys
TuyaPlug1 = None
TuayaPlug2 =  None
devicelist1 = None
reqipaddr = None
DeviceDataBase= None
OperationModesDb = None
demolist=None
pahoclient=None
NewMsgFlag=False
NewPahoMsg=None
#app = Flask(__name__)

def getip():
    global reqipaddr
    ifacename=os.environ.get('NWIFACE')
    print(ifacename)
    ipstring = "ip addr show " + ifacename + "| grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"      
    s = subprocess.check_output([ipstring], stdin=None, stderr=None, shell=True, universal_newlines=True)
    if len(s) != 0:
        reqipaddr = s[0:len(s)-1]

def TuyaDeviceData(pluginst):
    pluginst.ReceiveDeviceData()

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



def PairCall():
    global devicelist1
    global DeviceDataBase
    global reqipaddr
    global NewPahoMsg
    global pahoclient
    """
    reqargs=request.args.to_dict()
    deviceidx=reqargs.get("index")
    """
    deviceidx = NewPahoMsg
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
    pahoclient.publish("PairRes", json.dumps(s1))
    #return json.dumps(s1)

def RenderDevicestat():
       global TuyaPlug1
       global TuyaPlug2
       global devicelist1
       data={}
       list=[]
       for dev in devicelist1:
           if dev["type"] == "plug":
               if dev["name"] == "plug1":
                   elecconsumption, data = TuyaPlug1.Getdata()
               elif dev["name"] == "plug2":
                   elecconsumption, data = TuyaPlug2.Getdata()
           if dev["type"] == "plug":        
               print(data)
               sys.stdout.flush()
               if elecconsumption != 0 and data["CurVoltage"] != "InValid":
                   data["CurPwrUsage"] = str(elecconsumption);
               list.append(data)    
       print(list)
       var1=jsonify(listdata=list)
       pahoclient.publish("devicestatresp", json.dumps(var1))
    


def QueueTheOperations(listops):
    cmdstr=""
    for i in listops:
        cmdstr+=i + '; echo \"\\n\\n\\n\"; '
    return cmdstr

#@app.route('/Performdevops', methods=['GET'])
def PerformDeviceOps():
    global NewPahoMsg
    global devicelist1
    global OperationModesDb
    global pahoclient
    CHIPCmdList=""
    snapvar = os.environ.get('SNAP')
    pathvar=snapvar + "/extra-bin/chip-tool "
    #try:
    """
    reqargs=request.args.to_dict()
    demoname=reqargs.get("demoname")
    """
    demoname=NewPahoMsg
    deviceops=OpModes.Getdevops(OperationModesDb["operationmodes"], demoname)
    print(deviceops)
    Res= {"PerformdevOpsRes": "Failure"}
    for idx in deviceops:
        nodeid = DeviceList.GetDeviceNodeID(devicelist1, idx["devicename"])
        if nodeid == '0':
            nodeid=DeviceList.GetBridgeDeviceNodeID(DeviceDataBase, idx["devicename"])
        if nodeid != '0':    
            devicetype = DeviceList.GetDeviceType(devicelist1, idx["devicename"])
            print(devicetype)
            if devicetype in ["bridge","light", "plug", "light switch", "musicplayer"]:
                listops=MatterBulbOp.PerformBulbOp(idx, nodeid, pathvar)
                CHIPCmdList+=QueueTheOperations(listops)
                Res["PerformdevOpsRes"] = "Success"
    print(CHIPCmdList)
    subprocess.call([CHIPCmdList], stdin=None, stderr=None, shell=True, universal_newlines=True)
    return Res            
    #except:
    print("some failure")

def on_connect(client, userdata, flags, rc):
    print("connected paho client with rescode " + str(rc))
    #client.subscribe([("Bulb Op", 0), ("bulb off", 2)])
    client.subscribe("Bulb Op", 0)
    
    
def on_message(client, userdata, message):
    global NewMsgFlag
    global NewPahoMsg
    print("received an message " + message.topic + " " + str(message.payload))
    if message.topic == "Bulb Op":
        NewMsgFlag = True
        NewPahoMsg = str(message.payload.decode("utf-8", "ignore"))
        print("decoded msg::" + NewPahoMsg)

              
def Spawn_Paho():
    global NewMsgFlag
    global NewPahoMsg
    global reqipaddr
    global pahoclient
    if pahoclient is not None:
        return pahoclient
    mqttip=os.environ.get('PAHOBROKIP')
    if mqttip is None:
        mqttip=reqipaddr
    pahoclient = mqtt.Client()
    pahoclient.on_connect = on_connect
    pahoclient.on_message = on_message
    pahoclient.connect(mqttip, 1883, 60)
    pahoclient.loop_start()
    while True:
        if NewMsgFlag == True:
            if NewPahoMsg  in demolist:
                PerformDeviceOps()
            else:
                PairCall()

            NewMsgFlag = False
        time.sleep(0.200)
    pahoclient.loop_stop()

#@app.route('/')
def hello_world():
    global devicelist1
    global DeviceDataBase
    global reqipaddr
    global demolist
    global OperationModesDb
    if OperationModesDb is None:
        OperationModesDb={}
    if demolist is None:
        demolist = []
    if devicelist1 is None:
        devicelist1 = []
    if reqipaddr is None:
        reqipaddr = "127.0.0.1"
    if DeviceDataBase is None:
        DeviceDataBase = {}
    getip()
    pathname = os.environ.get('TMPDIR')
    fname=pathname + "/devicelist.json"
    print(pathname, fname)
    DeviceDataBase=DeviceList.getdata(fname)
    devicelist1=DeviceList.GetDeviceList(DeviceDataBase["devices"])
    opmodefile=pathname + '/opmodes.json'
    OperationModesDb=OpModes.GetData(opmodefile)
    demolist = OpModes.GetDemoList(OperationModesDb["operationmodes"])
    print(demolist)
    Spawn_Paho() #LooP FUnction
    devstat = os.environ.get('DEVSTATS')
    if devstat == "ON":
        TuyaPlug1 = tinytuyaapp.TinyTuyaPlugData("plug1", 'd774d88399af8258ddjmjz', "192.168.1.83", 'U/$B2?kq|iO8}l`j')
        TuyaPlug2 = tinytuyaapp.TinyTuyaPlugData("plug2", "d7934fd0d469f1b0d6lmza", "192.168.1.80", "3769c7cba9b2d5ba")
    
        t2= Thread(target=TuyaDeviceData, args=(TuyaPlug2,))
        t2.start()
        t1= Thread(target=TuyaDeviceData, args=(TuyaPlug1,))
        t1.start()
    return "Success"
    #return render_template('/devicedemo.html', ipaddr=reqipaddr, devicedemolist=demolist)

if __name__ == '__main__':
   
    reqipaddr=None
    ifacename=os.environ.get('NWIFACE')
    print(ifacename)
    ipstring = "ip addr show " + ifacename + "| grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"      
    s = subprocess.check_output([ipstring], stdin=None, stderr=None, shell=True, universal_newlines=True)
    if len(s) != 0:
        reqipaddr = s[0:len(s)-1]
    hello_world()    
    """ 
    if reqipaddr is not None:
        app.run(host=reqipaddr, debug=True, port=5002)
    else:    
        app.run(host='0.0.0.0', debug=True, port=5002)
   """


def UnapairAll():
    snapdatacomvar = os.environ.get('SNAP_DATA')
    fname=snapdatacomvar + "/"
    fname+="*_pairres.json"
    cmd="rm -f /tmp/chip_* /mnt/chip_*" + " "  + fname
    print(cmd)
    subprocess.call([cmd], stdin=None, stderr=None, shell=True, universal_newlines=True)
    return json.dumps({"UnPairAll":"Success"})

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


