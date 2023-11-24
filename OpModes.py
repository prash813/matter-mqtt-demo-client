import os
import json

class OpModes:
    def GetData(fname):
        fp1=open(fname, "r")
        res=json.load(fp1)
        print(fname)
        fp1.close()
        return res
    def Getdevops(opmodelist, demoname):
        demolist=[]
        for idx in opmodelist:
            if idx["name"] == demoname:
                print("found demo  ", demoname)
                return idx["devops"]
        
    def GetDemoList(operationmodes):
        demolist=[]
        for idx in operationmodes:
            demolist.append(idx["name"])
            print(idx)
        return  demolist
