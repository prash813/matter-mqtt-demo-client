#chip-tool onoff on <nodeid> <endpointid>
#chip-tool onoff off <nodeid> <endpointid>
#chip-tool onoff toggle <nodeid> <endpointid<ep>>
#chip-tool levelcontrol move-to-level <level> <transition T> <OptionMask> <Optionoverrides> <nodeid> <ep>
#chip-tool colorcontrol move-to-hue Hue Direction TransitionTime OptionsMask OptionsOverride dest-nodeid endpoint-id
#chip-tool colorcontrol move-to-hue-and-saturation Hue Saturation TransitionTime OptionsMask OptionsOverride destination-id endpoint-id
class MatterBulbOp:
    CommandList= { "On": ["onoff", "on", "1", "1"], "Off": ["onoff", "off", "1", "1"], "toggle": ["onoff", "toggle", "1", "1"],
    "brightness":["levelcontrol", "move-to-level", "100", "0", "0", "0", "1", "1"], "color": ["colorcontrol", "move-to-hue", "red", "0", "0", "0", "0", "1", "1"],
    "saturation": ["colorcontrol", "move-to-saturation", "100",  "0", "0", "0", "1", "1"],
    "StartMusic": ["onoff", "on", "1", "1"], "StopMusic": ["onoff", "off", "1", "1"]}
    ColorTable= {"Red":"0","Orange":"30", "Yellow":"60","Green":"90", "Spring Green":"150", "Cyan":"180", "Azure":"210", "Blue":"240", "Violet":"270", "Magenta":"300", "Rose":"330"}          

    '''
        Mainly useful for onoff cluster commands 
    '''
    def PerformBulbOp(cmddescr, nodeid, chiptool_cmd):
        #chiptool="/extra-bin/chip-tool "
        pathvar=chiptool_cmd
        cmdparamlist=MatterBulbOp.CommandList[cmddescr["cmdname"]]
        pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + str(nodeid)+ " " + str(cmddescr["endpoint"])
        print(pathvar)
        cmdlist = []
        cmdlist.append(pathvar)
        if "color" in cmddescr.keys():
            pathvar=chiptool_cmd
            cmdparamlist=MatterBulbOp.CommandList["color"]
            pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + MatterBulbOp.ColorTable[cmddescr["color"]] + " " + cmdparamlist[3] + " " 
            pathvar+=cmdparamlist[4] + " " + cmdparamlist[5] + " " + cmdparamlist[6] + " " + str(nodeid) + " " + str(cmddescr["endpoint"])
            cmdlist.append(pathvar) 
        if "saturation" in cmddescr.keys():
            pathvar=chiptool_cmd
            cmdparamlist=MatterBulbOp.CommandList["saturation"]
            pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + cmddescr["saturation"] + " " + cmdparamlist[3] + " " + cmdparamlist[4]
            pathvar+= " " + cmdparamlist[5] + " " + str(nodeid) + " " + str(cmddescr["endpoint"])
            cmdlist.append(pathvar) 
        if "brightness" in cmddescr.keys():
            pathvar=chiptool_cmd
            cmdparamlist=MatterBulbOp.CommandList["brightness"]
            pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + cmddescr["brightness"] + " " + cmdparamlist[3] + " " + cmdparamlist[4]
            pathvar+= " " + cmdparamlist[5] + " " + str(nodeid) + " " + str(cmddescr["endpoint"])
            cmdlist.append(pathvar)

        return cmdlist    
