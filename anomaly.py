# Visual Anomaly FOMO-AD with TI TDA4VM
# Roni Bandini @RoniBandini May 2024 https://bandini.medium.com
# MIT License
# https://bandini.medium.com 

import subprocess
import time
import requests
import json
import os

threshold=8
counter=0
anomalies=0

# anomaly matrix
w, h = 5, 5
Matrix = [["." for x in range(w)] for y in range(h)] 


def clearMatrix():
	row=0
	while row<5:
		Matrix[0][row]="."
		Matrix[1][row]="."
		Matrix[2][row]="."
		Matrix[3][row]="."
		Matrix[4][row]="."
		row=row+1    

def printMatrix():
	row=0
	while row<5:
		print( Matrix[0][row]+Matrix[1][row]+Matrix[2][row]+Matrix[3][row]+Matrix[4][row])
		row=row+1    

def assignMatrix(coordinates):
    
    if coordinates=="0,0":    	
    	Matrix[0][0]="X"
    if coordinates=="19,0":
    	Matrix[1][0]="X"
    if coordinates=="38,0":
    	Matrix[2][0]="X"
    if coordinates=="57,0":
    	Matrix[3][0]="X"
    if coordinates=="76,0":
    	Matrix[4][0]="X"

    if coordinates=="0,19":
    	Matrix[0][1]="X"
    if coordinates=="19,19":
    	Matrix[1][1]="X"
    if coordinates=="38,19":
    	Matrix[2][1]="X"
    if coordinates=="57,19":
    	Matrix[3][1]="X"
    if coordinates=="76,19":
    	Matrix[4][1]="X"

    if coordinates=="0,38":
    	Matrix[0][2]="X"
    if coordinates=="19,38":
    	Matrix[1][2]="X"
    if coordinates=="38,38":
    	Matrix[2][2]="X"
    if coordinates=="57,38":
    	Matrix[3][2]="X"
    if coordinates=="76,38":
    	Matrix[4][2]="X"

    if coordinates=="0,57":
    	Matrix[0][3]="X"
    if coordinates=="19,57":
    	Matrix[1][3]="X"
    if coordinates=="38,57":
    	Matrix[2][3]="X"
    if coordinates=="57,57":
    	Matrix[3][3]="X"
    if coordinates=="76,57":
    	Matrix[4][3]="X"

    if coordinates=="0,76":
    	Matrix[0][4]="X"
    if coordinates=="19,76":
    	Matrix[1][4]="X"
    if coordinates=="38,76":
    	Matrix[2][4]="X"
    if coordinates=="57,76":
    	Matrix[3][4]="X"
    if coordinates=="76,76":
    	Matrix[4][4]="X"


# Runner output file
output_file = open('output.txt', 'w')

os.system('clear')

print("Visual Anomaly with Texas Instruments TDA4VM and Edge Impulse")
print("Roni Bandini, May 2024, Buenos Aires, Argentina")
print("Stop with CTRL-C")

# Launch Impulse Runner sending output to a file
subprocess.Popen(["edge-impulse-linux-runner"], stdout=output_file)


with open("output.txt", "r") as f:

	lines_seen = set()
    
	while True:
        	
		line = f.readline()
        	
		if not line:
			time.sleep(1)
			continue


		if ("[]" in line):
			print("No anomalies detected")
			counter=counter+1
			

		if ("height" in line) and line not in lines_seen:			
			
			clearMatrix()

			counter=counter+1
			anomalies=anomalies+1

			parts = line.split()    

			myLine = parts[3]

			myJson = json.loads(myLine)

			print("")

			for item in myJson:	
				if float(item["value"])>threshold:	
					atLeastOne=1	
					assignMatrix(str(item["x"]) +","+ str(item["y"]))	
					print( str('{:.2f}'.format(item["value"]) )+ " at ("+str(item["x"]) +","+ str(item["y"]) +")")				

								
			if atLeastOne==1:				
				print("")	
				printMatrix()
				print("")					
				print(str(anomalies)+"/"+str(counter)+" "+str((anomalies/counter)*100)+"%")
				
				print("")	
				print("***************************** VISUAL ANOMALY *****************************")		

		lines_seen.add(line)


