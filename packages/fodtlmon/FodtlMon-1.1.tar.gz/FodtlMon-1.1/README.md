[![License](https://img.shields.io/badge/version-1.0-orange.svg)]()
[![License](https://img.shields.io/badge/license-GPL3-blue.svg)]()
[![License](https://img.shields.io/badge/python->%3D3.4-green.svg)]()

# FodtlMon

FodtlMon Last release : Version 1.1

What is it?
-----------

FodtlMon is a monitoring framework based on distributed first order linear temporal logic.

Installation
------------

You need PythonX.X.X >= Python3.4.0 installed on your system
To run the main program : python mon.py

    You need to install the following dependencies :  
    
        $ sudo pip3 install antlr4-python3-runtime
            
To install the framework run setup.py:

        $ sudo python3 setup.py install


Usage
-----


    Usage : mon.py [OPTIONS] formula trace
      -h 	--help          	 display this help and exit
      -i 	--input= [file] 	 the input file
      -o 	--output= [path]	 the output file
      -f 	--formula       	 the formula
         	--iformula      	 path to file that contains the formula
      -t 	--trace         	 the trace
         	--itrace        	 path to file that contains the trace
      -1 	--ltl           	 use LTL monitor
         	--l2m           	 call ltl2mon also
      -2 	--fotl          	 use FOTL monitor
      -3 	--dtl           	 use DTL monitor
      -4 	--fodtl         	 use FODTL monitor
         	--sys= [file]   	 Run a system from json file
         	--rounds= int   	 Number of rounds to run in the system
      -z 	--fuzzer        	 run fuzzing tester
            --server        	 start web service
     	    --port= int     	 server port number

* formula format : true | false | ~formula | P(variable) | P('constant') | formula (=> | & | '|' | U | R ) formula | @name(formula) | G formula | F formula | X formula  | ![x1:type1 x2:type2 ...] formula | ?[x1:type1 x2:type2 ...] formula 
* event format : {Predicate(args) | ....}
* trace format : {event1; event2; .... } 

Licensing
---------

GPL V3 . Please see the file called LICENSE.

Contacts
--------

###### Developer :
>   Walid Benghabrit        <Walid.Benghabrit@mines-nantes.fr>

###### Contributors :
>   Pr.Jean-Claude Royer  <Jean-Claude.Royer@mines-nantes.fr>  (Theory)  
>   Dr. Hervé Grall       <Herve.Grall@mines-nantes.fr>        (Theory)  

-------------------------------------------------------------------------------
Copyright (C) 2014-2016 Walid Benghabrit  
Ecole des Mines de Nantes - ARMINES  
ASCOLA Research Group  
A4CLOUD Project http://www.a4cloud.eu/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
