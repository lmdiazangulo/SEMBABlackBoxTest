#! /usr/bin/env python3
# OpenSEMBA
# Copyright (C) 2015 Salvador Gonzalez Garcia                    (salva@ugr.es)
#                    Luis Manuel Diaz Angulo          (lmdiazangulo@semba.guru)
#                    Miguel David Ruiz-Cabello Nuñez        (miguel@semba.guru)
#                    Alejandra Lopez de Aberasturi Gomez (aloaberasturi@ugr.es)
#                    
# This file is part of OpenSEMBA.
#
# OpenSEMBA is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# OpenSEMBA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with OpenSEMBA. If not, see <http://www.gnu.org/licenses/>.


from . import filemanager as FM
from . import filters
from . import comparison
import colored
from colored import stylize
from termcolor import colored as clrd
from termcolor import cprint
import json
import pathlib
import subprocess
from subprocess import Popen,PIPE
import os
import shutil


def searchMatchingProject(caseFile):
    global caseOptions
    global testOptions
    with caseFile.open("r") as jsonFile:
        j = json.loads(jsonFile.read())
        caseOptions = filters.Filters(j["filters"]["size"],
                                    [ j["filters"]["keyWords"]["materials"],
                                      j["filters"]["keyWords"]["excitation"],
                                      j["filters"]["keyWords"]["mesh"]
                                    ],
                                      j["filters"]["comparison"],
                                      j["filters"]["execution"]
        )
        caseOptions.keyWords = [x.upper() for x in caseOptions.keyWords]
          
    if (
       (set(caseOptions.keyWords) &  set(testOptions.keyWords))!= set() 
       and (caseOptions.size <= testOptions.size)
    ):
        return True

    else : 
        return False

def callSemba(fileName):

    blue = colored.fg(38)
    purple = colored.fg(177)

    print(stylize(
            "                 Entering project " + str(test.projectFolder.name),
            purple)
    )

    try:
        print(stylize(
            "-----------------------------------------------------------------", 
            blue)
        )

        print("\n")

        cprint(
            "                        1. Executing SEMBA",
            "blue",
            attrs=["blink","bold"]
        )

        #--------------Please comment to display SEMBA's std output-------------

        process = Popen(
            ["./semba","-i",str(fileName.name)],
            stdout = PIPE,
            cwd = fileName.parent
        )
        process.communicate() 

        #--------------Please uncomment to display SEMBA's std output-----------

        #subprocess.run([str(exePath),"-i",str(fileName)])   
        
        os.remove(str(fileName.parent / "semba"))   


    except RuntimeError:"Unable to launch semba"



def callUGRFDTD(nfde):

    blue = colored.fg(38)

    try:
        print("\n")

        cprint(
            "                        2. Executing UGRFDTD",
            "blue",
            attrs=["blink","bold"]
        )

        print("\n")

        print(stylize(
            "-----------------------------------------------------------------",
            blue)
        )

   
#----------------Please comment to display UGRFDTD's std output-----------------
   
        process = Popen(
            ["./ugrfdtd","-i",str(nfde.name)],
            stdout = PIPE, 
            cwd = nfde.parent
        )

        process.communicate() 

#----------------Please uncomment to display UGRFDTD's std output---------------

        #subprocess.call(["./ugrfdtd","-i",str(nfde.name)], cwd = str(nfde.parent))

        os.system('cls' if os.name == 'nt' else 'clear')
        os.remove(str(nfde.parent / "ugrfdtd"))

    except RuntimeError :"Unable to launch UGRFDTD"


def storeOutputs():
    OptRqs = []
    for i in case.ugrfdtdFolder.glob('**/*_Outputrequests_*'):   
            with i.open("r") as listOfOutputs:
                lines = listOfOutputs.readlines()
                for line in lines:
                    if "!END" in line: 
                        break
                    line = case.ugrfdtdFolder / line.split("\n")[0]

                    OptRqs.append(pathlib.Path(line))

    return OptRqs


def launchTest(OptRqs, cast = float):
    red = colored.fg(1)
    green = colored.fg(82)
    passes = []

    for i in range (0, len(OptRqs)):
        with open(OptRqs[i]) as caseOutput:
            with open(test.ugrfdtdFolder / OptRqs[i].name) as testOutput:
                passes.append(True)    

                try:                    
                    print(
                        stylize("[----------]",green),
                        "Testing", 
                        OptRqs[i].name)

                    print(
                        stylize("[ RUN      ]",green),
                        caseOptions.comparison,
                        "test")

                    for j in caseOutput:
                        modelLine = (j.split("\n")[0]).split()
                        testLine = (
                            (
                                testOutput.readline()
                            ).split("\n")[0]
                        ).split()

                        if ((caseOptions.comparison).upper() == "ISEQUAL") : 
                            try:   

                                if comparison.IsEqual(
                                        cast(modelLine[1]),
                                        cast(testLine[1])
                                ) == False:
                                    passes[i] = False
                            except ValueError: continue

                        elif ((caseOptions.comparison).upper() == "ISALMOSTEQ"):
                            try:
                                if comparison.IsAlmostEqual(
                                        cast(modelLine[1]),
                                        cast(testLine[1]),
                                        relTolerance,
                                        absTolerance
                                ) == False:
                                    passes[i] = False
                            except ValueError: continue

                    if passes[i] ==True:
                        print(
                        stylize("[       OK ]",green),
                        caseOptions.comparison,
                        "test")                        
                        print(stylize("[----------]",green))
                    else:
                        print(
                            stylize("[  FAILED  ]",red),
                            caseOptions.comparison,
                            "test")


                except IndexError: 
                   "Test and case files don't have the same length."
                   " Please check that semba compiled correctly"
            testOutput.close() 
        caseOutput.close()

    print(
        stylize("[==========]",green)
    )           

    if sum(passes)!=len(OptRqs):       
        print(
            stylize("[  FAILED  ]", red),
            len(OptRqs)-sum(passes),
            "cases")
            
        print(len(OptRqs)-sum(passes),"FAILED CASE")
        return False
    else:
        return True
                       
                  
                            