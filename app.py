from flask import Flask, request 
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
app = Flask(__name__)
def main(file_name):
    start_time = int(round(time.time() * 1000))

    configuration = Configuration()
    configuration.parseFile(file_name)

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
        className = _dict["Course"].__dict__["Name"]
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
                    shift_weekday_room.append({
                        "shift": _shift, 
                        "weekday": _weekday,
                        "room": _room})
        dataOutput.append({
            "classID": classID,
            "className": className,
            "room": _room,
            "shift_weekday_room": shift_weekday_room
        })
        
    for i in dataOutput: 
        print(i)
    return json.dumps(dataOutput)
   

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
@app.route('/', methods=['GET'])
def hello():
    alo = {"data": "hello"}
    return json.dumps(alo)

@app.route('/scheduling', methods=['POST'])
def process_form():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        
        return main(json)
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    app.run()
