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

import sys
from termcolor import colored,cprint

def IsEqual(a,b):
    try:
        assert a == b
        return True
    except AssertionError: 
        print(
            sys.modules[__name__],
            ": error: Expected: ",
            a,
            " \nto be equal to:",
            b,"\nActual: False")
        return False 
      


def IsAlmostEqual(a,b,relTolerance,absTolerance):
    try:

        assert (100*abs(a-b)/a) <= relTolerance
        return True

    except AssertionError:
        print(
            sys.modules[__name__],
            ": error: Expected: ",
            a,
            " \nto be almost equal to:",
            b,
            "\nActual: False")
        return False

    except ZeroDivisionError:     
        if b != 0.0:
            try:

                assert (abs(b) <= absTolerance)
                return True

            except AssertionError:
                print(
                    sys.modules[__name__],
                    ": error: Expected: ",
                    a,
                    " \nto be almost equal to:",
                    b,
                    "\nActual: False")
                return False
        else: 
            return True