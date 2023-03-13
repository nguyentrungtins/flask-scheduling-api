import codecs
import pathlib
import os
import sys
import tempfile
import time
import traceback
import subprocess, sys
import json
from model.Configuration import Configuration
from algorithm.GeneticAlgorithm import GeneticAlgorithm

def main(file_name):
    start_time = int(round(time.time() * 1000))

    configuration = Configuration()
    target_file = str(pathlib.Path().absolute()) + file_name
    configuration.parseFile(target_file)

    alg = GeneticAlgorithm(configuration)
    # alg = Hgasso(configuration)
    print("GaSchedule Version 1.2.3 . Making a Class Schedule Using", alg, ".\n")
    print("Copyright (C) 2022 - 2023 Miller Cy Chan.\n")
    alg.run()

    seconds = (int(round(time.time() * 1000)) - start_time) / 1000.0
    print("\nCompleted in {} secs.\n".format(seconds))
  
    _slots = alg.result.__dict__["_slots"]
    _classes = alg.result.__dict__["_classes"]
   
    

    solution = alg.result
    configuration = solution.configuration
    getRoomById = configuration.getRoomById
    print(getRoomById(1))
    dataOutput = []
    print("class len: ", len(_classes))
    for i in _classes:
        _dict  = i.__dict__.copy()
        classID = _dict["Id"]
        slotCount = 0
        shift_weekday_room = []
        for i in range(len(_slots)): 
            if (i+1)%24==0: 
                slotCount += 1
            if _slots[i]: 
                if (_slots[i][0].__dict__["Id"] == classID): 
                     
                    _slotCalculated = i-(slotCount*24)
                    _room = getRoomById(slotCount).__dict__["Name"]
                    _shift, _weekday = getScheduleBySlot(_slotCalculated)
                    shift_weekday_room.append([_shift, _weekday,_room])
        dataOutput.append({
            "classID": classID,
            "room": _room,
            "shift_weekday_room": shift_weekday_room
        })
        
    for i in dataOutput: 
        print(i)
   

def getScheduleBySlot(slot): 
    
    shift = (slot % 4) + 1
    weekday = slot // 4
    if ( weekday == 0 ):
        weekday = "MON" 
    elif ( weekday == 1 ):
        weekday = "TUE" 
    elif ( weekday == 2 ):
        weekday = "WED" 
    elif ( weekday == 3 ):
        weekday = "THU" 
    elif ( weekday == 4 ):
        weekday = "FRI" 
    elif ( weekday == 5 ):
        weekday = "SAT" 
    else:
        weekday = "SUN"
    return shift, weekday
    



if __name__ == "__main__":
    file_name = "/GaSchedule.json"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    try:
        main(file_name)
    except:
        traceback.print_exc()
