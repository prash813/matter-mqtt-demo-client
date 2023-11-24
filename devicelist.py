import os
import json
class DeviceList:
    def CheckIfDevicePrePaired(nodeid):
        snapdatacomvar = os.environ.get('SNAP_DATA')
        retval="notpaired"  
        try:
            fname=snapdatacomvar + "/"
            fname+=nodeid + "_pairres.json"
            print(fname)
            fp1=open(fname, "r")
            res=json.load(fp1)
            print(res["Results"][0])
            if res["Results"][0]["Pairing"] == "Success":		
                retval="paired"
            fp1.close()
            print(retval)
            return retval
        except IOError:
            return retval
  	
    def getdata(fname):
        fp1=open(fname, "r")
        res=json.load(fp1)
        fp1.close()
        return res

    def formatstring(pwdstr):
        print(pwdstr)
        nonumalphastr="!@#$%^&*?"
        newnewstr=""
        for i in pwdstr:
            ret = nonumalphastr.find(i)
            if(ret != -1):
                newnewstr+= "\\"
            newnewstr+=i
        print(newnewstr)    
        return newnewstr
    def GetDeviceType(list_in, devname):

        for item in list_in:
            if item["name"] == devname:
                break
        return item["type"]
    def GetDeviceNodeID(list_in, devname):
        found=False
        for item in list_in:
            if item["name"] == devname:
                print(item["nodeid"], devname)
                found=True
                break
        if found == False:
            return "0"    #invalid nodeid
        return item["nodeid"]
        
    def GetBridgeDeviceNodeID(devicedatabase, nodename):
        found=False
        
        devicelist=devicedatabase["devices"]

        for idx in devicelist:
            if idx["type"] == "bridge":
                bridgedevlist = idx["devicelist"]
                for idx1 in bridgedevlist:
                    if idx1["devicename"] == nodename:
                        found=True;
                        break
            if found == True:
                break
        if found == True:
            print("Bridge Device Found in:: ", idx["devicename"])
            return idx["nodeid"]
        return "0" #invalid nodeid    



    def GetDevicePairingParams(list_in, devicelist, index):
        tmpitem={}
        for item in list_in:
            if int(index) == item["idxinlist"]:
                print(index, item["idxinlist"])
                break
        for data in devicelist:
            print(type(data))
            if item["name"] == data["devicename"]:
                break
        print(data["pairing-opt"])        
        return [item["nodeid"],data["pairing-opt"]]

    def GetDeviceList(list_in):
        count=0 
        list_out = []

        for item in list_in:
            #list_out[count]["name"] = item["devicename"]
            #list_out[count]["type"] = item["type"]
            #list_out[count]["nodeid"] = item["nodeid"]
            #list_out[count]["idxinlist"] = count
            tmpdictitem = {"name":"", "type":"", "nodeid":"0", "idxinlist":0, "pairstatus":"notpaired"}
            tmpdictitem["name"] = item["devicename"]
            tmpdictitem["type"] = item["type"]
            tmpdictitem["nodeid"] = item["nodeid"]
            tmpdictitem["idxinlist"] = count
            tmpdictitem["pairstatus"] = DeviceList.CheckIfDevicePrePaired(item["nodeid"]) 
            list_out.append(tmpdictitem)
            print(count,tmpdictitem["name"],item["type"],tmpdictitem["nodeid"], tmpdictitem["pairstatus"])
            count=count+1
        return list_out  

