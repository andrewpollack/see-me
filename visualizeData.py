"""
  Code written by Andrew Pollack, adapted from code written for use at VHIL.  
  If you need help understanding any parts, reach out to me at andrewpk@stanford.edu and/or andrewpkq@gmail.com

  Package Dependencies:imageio, matplotlib
  	To install: issue these commands in shell:
  		pip3 install imageio
  		pip3 install matplotlib

"""

import subprocess
import csv
import os
import math
# To install imageio package, issue the command "pip3 install imageio" in your shell/command line
import imageio
import glob
import os.path
from os import path
import matplotlib.pyplot as plt
# To install matplotlib package, issue the command "pip3 install matplotlib" in your shell/command line



DATA_PATH = "dataLogs/"
OUTPUT_PATH = "finalOutput/"
INTERMEDIATE_PATH = "intermediateFiles/"
CSV_TO_RUN = []

# Adjustable Constants
REDUCED_FRAMERATE = False # If True, cuts framerate to be a fifth
KEEP_INTERMEDIATE_PNGS = False
KEEP_INTERMEDIATE_CSVS = False

# CSV Constants
HEAD_POS = 1
HEAD_EULER = 2
CONTROLLER_1_POS = 3
CONTROLLER_1_EULER = 4
CONTROLLER_2_POS = 5
CONTROLLER_2_EULER = 6

# Globals to reset on each run
CSV_ITER = 0
TITLE_POS = 0

# DICT Constants
HEAD_POS_X = 0
HEAD_POS_Y = 1
HEAD_POS_Z = 2
HEAD_EULER_YAW = 3
HEAD_EULER_PITCH = 4
HEAD_EULER_ROLL = 5
CONTROLLER_1_POS_X = 6
CONTROLLER_1_POS_Y = 7
CONTROLLER_1_POS_Z = 8
CONTROLLER_1_YAW = 9
CONTROLLER_1_PITCH = 10
CONTROLLER_1_ROLL = 11
CONTROLLER_2_POS_X = 12
CONTROLLER_2_POS_Y = 13
CONTROLLER_2_POS_Z = 14
CONTROLLER_2_YAW = 15
CONTROLLER_2_PITCH = 16
CONTROLLER_2_ROLL = 17

# Data Processing Constants
OFFANGLE = math.radians(30)
LENGTH_OF_SIGHT_LINE = 3
LENGTH_OF_CONTROLLER_LINE = 2


def getMinMax(boundsToFind, currCSV):
	lines = ""
	with open(currCSV , "r") as f:
		lines = f.readlines()
	minNum = 500 # impossibly large
	maxNum = -500 # impossibly negative
	for line in lines:
		for l in csv.reader([line], delimiter=',', quotechar='"'):
			# Below if statement will ignore all blank lines in csv
			if l[CONTROLLER_2_POS] != "":
				# Below if statement will ignore all 
				if len(l[CONTROLLER_2_POS].split(",")) == 1:
					break
				csvPos = 0
				listPos = 0

				if(boundsToFind.startswith("POS")):
					csvHead = HEAD_POS
					csvControllerOne = CONTROLLER_1_POS
					csvControllerTwo = CONTROLLER_2_POS
					if(boundsToFind.endswith("X")):
						listPos = 0
					if(boundsToFind.endswith("Y")):
						listPos = 1
					if(boundsToFind.endswith("Z")):
						listPos = 2
				if(boundsToFind.startswith("EUL")):
					csvHead = HEAD_EULER
					csvControllerOne = CONTROLLER_1_EULER
					csvControllerTwo = CONTROLLER_2_EULER
					if(boundsToFind.endswith("YAW")):
						listPos = 0
					if(boundsToFind.endswith("PITCH")):
						listPos = 1
					if(boundsToFind.endswith("ROLL")):
						listPos = 2


				headVal = float(((l[csvHead]).strip("][")).split(",")[listPos])
				handOneVal = float(((l[csvControllerOne]).strip("][")).split(",")[listPos])
				handTwoVal = float(((l[csvControllerTwo]).strip("][")).split(",")[listPos])
				if(headVal > maxNum):
					maxNum = headVal
				if(headVal < minNum):
					minNum = headVal
				if(handOneVal > maxNum):
					maxNum = handOneVal
				if(handOneVal < minNum):
					minNum = handOneVal
				if(handTwoVal > maxNum):
					maxNum = handTwoVal
				if(handTwoVal < minNum):
					minNum = handTwoVal

	return (minNum, maxNum)





def getAllPositionsAndEulers(currPositionDict, l):

	# Rest of code is purely for tracking positions from csv
	currPositionDict[HEAD_POS_X] = float(((l[HEAD_POS]).strip("][")).split(",")[0])
	currPositionDict[HEAD_POS_Y] = float(((l[HEAD_POS]).strip("][")).split(",")[1])
	currPositionDict[HEAD_POS_Z] = float(((l[HEAD_POS]).strip("][")).split(",")[2])
	currPositionDict[HEAD_EULER_YAW] = float(((l[HEAD_EULER]).strip("][")).split(",")[0])
	currPositionDict[HEAD_EULER_PITCH] = float(((l[HEAD_EULER]).strip("][")).split(",")[1])
	currPositionDict[HEAD_EULER_ROLL] = float(((l[HEAD_EULER]).strip("][")).split(",")[2])

	currPositionDict[CONTROLLER_1_POS_X] = float(((l[CONTROLLER_1_POS]).strip("][")).split(",")[0])
	currPositionDict[CONTROLLER_1_POS_Y] = float(((l[CONTROLLER_1_POS]).strip("][")).split(",")[1])
	currPositionDict[CONTROLLER_1_POS_Z] = float(((l[CONTROLLER_1_POS]).strip("][")).split(",")[2])
	currPositionDict[CONTROLLER_2_POS_X] = float(((l[CONTROLLER_2_POS]).strip("][")).split(",")[0])
	currPositionDict[CONTROLLER_2_POS_Y] = float(((l[CONTROLLER_2_POS]).strip("][")).split(",")[1])
	currPositionDict[CONTROLLER_2_POS_Z] = float(((l[CONTROLLER_2_POS]).strip("][")).split(",")[2])

	currPositionDict[CONTROLLER_1_YAW] = float(((l[CONTROLLER_1_EULER]).strip("][")).split(",")[0])
	currPositionDict[CONTROLLER_1_PITCH] = float(((l[CONTROLLER_1_EULER]).strip("][")).split(",")[1])
	currPositionDict[CONTROLLER_1_ROLL] = float(((l[CONTROLLER_1_EULER]).strip("][")).split(",")[2])
	currPositionDict[CONTROLLER_2_YAW] = float(((l[CONTROLLER_2_EULER]).strip("][")).split(",")[0])
	currPositionDict[CONTROLLER_2_PITCH] = float(((l[CONTROLLER_2_EULER]).strip("][")).split(",")[1])
	currPositionDict[CONTROLLER_2_ROLL] = float(((l[CONTROLLER_2_EULER]).strip("][")).split(",")[2])




def mergePngs(currCSV):
	global CSV_ITER

	out_name = currCSV.split('.')[0] + ".gif"
	percentComplete = 0

	with imageio.get_writer(out_name, mode='I', loop = 1, fps=70, palettesize=32, subrectangles = True ) as writer:
		for i in range(1, CSV_ITER+1):
			pngName = INTERMEDIATE_PATH + str(i) + ".png"
			image = imageio.imread(pngName)
			percentComplete = round( i / (CSV_ITER+1) * 100, 1)
			print(str(percentComplete) + "% frames stitched")
			writer.append_data(image)
	newOutname = out_name
	if(len(newOutname.split("/")) > 1 ):
		newOutname = newOutname.split("/")[len(newOutname.split("/")) - 1]
	os.rename(out_name, OUTPUT_PATH + newOutname)
	print("Finished " + newOutname)

def removeIntermediateFiles():
	global CSV_ITER

	if not KEEP_INTERMEDIATE_PNGS:
		for i in range(1, CSV_ITER+1):
			if os.path.isfile(INTERMEDIATE_PATH + str(i) + ".png"):
				os.remove(INTERMEDIATE_PATH + str(i) + ".png")


def createFinalOutputs(currCSV):
	mergePngs(currCSV)
	removeIntermediateFiles()




def generateGraph(currPositionDict, l, totalLines, posYMinMax):
	global CSV_ITER, prevWholeNum
	# Coordinates for eye vision lines
	headRadianX = math.radians(currPositionDict[HEAD_EULER_YAW])
	eyeRightOneX = currPositionDict[HEAD_POS_X] + (LENGTH_OF_SIGHT_LINE / math.sqrt(3)) * math.sin(headRadianX + OFFANGLE)
	eyeRightOneZ = currPositionDict[HEAD_POS_Z] + (LENGTH_OF_SIGHT_LINE / math.sqrt(3)) * math.cos(headRadianX + OFFANGLE)
	eyeRightTwoX = currPositionDict[HEAD_POS_X] + (LENGTH_OF_SIGHT_LINE / math.sqrt(3)) * math.sin(headRadianX - OFFANGLE)
	eyeRightTwoZ = currPositionDict[HEAD_POS_Z] + (LENGTH_OF_SIGHT_LINE / math.sqrt(3)) * math.cos(headRadianX - OFFANGLE)

	# headYOffAngle = abs(math.cos(math.radians(currPositionDict[CONTROLLER_2_PITCH])))
	headPitchX = -1 + ((2 / math.sqrt(3)) * (math.cos(math.radians(currPositionDict[HEAD_EULER_PITCH]))))
	headPitchY = 0 + ((2 / math.sqrt(3)) * (math.sin(math.radians(currPositionDict[HEAD_EULER_PITCH]))))

	# Coordinates for controller vision lines
	controllerOneRadianX = math.radians(currPositionDict[CONTROLLER_1_YAW])
	controllerOneOffAngle = abs(math.cos(math.radians(currPositionDict[CONTROLLER_1_PITCH])))
	controllerTwoRadianX = math.radians(currPositionDict[CONTROLLER_2_YAW])
	controllerTwoOffAngle = abs(math.cos(math.radians(currPositionDict[CONTROLLER_2_PITCH])))
	controllerOneX = currPositionDict[CONTROLLER_1_POS_X] + (controllerOneOffAngle * (LENGTH_OF_CONTROLLER_LINE / math.sqrt(3)) * math.sin(controllerOneRadianX))
	controllerOneZ = currPositionDict[CONTROLLER_1_POS_Z] + (controllerOneOffAngle * (LENGTH_OF_CONTROLLER_LINE / math.sqrt(3)) * math.cos(controllerOneRadianX))
	controllerTwoX = currPositionDict[CONTROLLER_2_POS_X] + (controllerTwoOffAngle * (LENGTH_OF_CONTROLLER_LINE / math.sqrt(3)) * math.sin(controllerTwoRadianX))
	controllerTwoZ = currPositionDict[CONTROLLER_2_POS_Z] + (controllerTwoOffAngle * (LENGTH_OF_CONTROLLER_LINE / math.sqrt(3)) * math.cos(controllerTwoRadianX))

	plt.close('all')
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
	axes[0].plot([currPositionDict[CONTROLLER_1_POS_X], controllerOneX], [currPositionDict[CONTROLLER_1_POS_Z], controllerOneZ], 'r.--', markersize=1) # armLine1
	axes[0].plot([currPositionDict[CONTROLLER_2_POS_X], controllerTwoX], [currPositionDict[CONTROLLER_2_POS_Z], controllerTwoZ], 'r.--', markersize=1) # armLine2
	axes[0].plot([currPositionDict[HEAD_POS_X], currPositionDict[CONTROLLER_1_POS_X]], [currPositionDict[HEAD_POS_Z], currPositionDict[CONTROLLER_1_POS_Z]], 'ro-', markersize=15) # ARM1
	axes[0].plot([currPositionDict[HEAD_POS_X], currPositionDict[CONTROLLER_2_POS_X]], [currPositionDict[HEAD_POS_Z], currPositionDict[CONTROLLER_2_POS_Z]], 'ro-', markersize=15) # ARM2
	axes[0].plot([currPositionDict[HEAD_POS_X], eyeRightOneX], [currPositionDict[HEAD_POS_Z], eyeRightOneZ], 'b.-', markersize=1) # vision1
	axes[0].plot([currPositionDict[HEAD_POS_X], eyeRightTwoX], [currPositionDict[HEAD_POS_Z], eyeRightTwoZ], 'b.-', markersize=1) # vision2
	
	currHeadYMin = posYMinMax[0]
	currHeadYMax = posYMinMax[1]
	currHeadY = currPositionDict[HEAD_POS_Y]

	axes[0].plot(currPositionDict[HEAD_POS_X], currPositionDict[HEAD_POS_Z], 'ko', markersize=(25 * currHeadY / currHeadYMax)) # HEAD

	axes[1].plot([-1, headPitchX], [0, headPitchY], 'b.-', markersize=1) # Profile - Head Vision
	axes[1].plot(-1, 0, 'ko', markersize=25) # Profile - Head Dot
	
	axes[1].axis([-2, 2, -2, 2])
	axes[0].axis([-3, 3, -3, 3])

	plt.savefig(INTERMEDIATE_PATH + str(CSV_ITER) + '.png')
	percentComplete = round( CSV_ITER / (totalLines+1) * 100, 1)
	print(str(percentComplete) + "% frames generated")



def processLine(l):
	if l[CONTROLLER_2_POS] != "" and not len(l[CONTROLLER_2_POS].split(",")) == 1:
		return True
	else:
		return False

def getBoundaries(currCSV):
	posXMinMax = getMinMax("POS_X", currCSV)
	posYMinMax = getMinMax("POS_Y", currCSV)

	return posYMinMax

def runPipeline(currCSV):
	global CSV_ITER, TITLE_POS, prevWholeNum

	if(len(currCSV.split(".csv")) != 2):
		print(currCSV  + " doesn't appear to be a csv file, skipping to next.")
		return
	finalDirectoryAndFileName = OUTPUT_PATH + currCSV.split("/")[len(currCSV.split(".csv"))-1].split(".csv")[0] + ".gif"
	if(path.exists(finalDirectoryAndFileName)):
		print(finalDirectoryAndFileName + " Already exists, skipping")
		return

	print("Beginning run on " + finalDirectoryAndFileName)

	CSV_ITER = 0
	TITLE_POS = 0
	TRUE_ITER = 0
	prevWholeNum = 0

	posYMinMax = getBoundaries(currCSV)

	lines = ""
	with open(currCSV , "r") as f:
		lines = f.readlines()


	# For each of the rows in the main csv
	for line in lines:
		for l in csv.reader([line], delimiter=',', quotechar='"'):
			if processLine(l):
				TRUE_ITER += 1
				if(REDUCED_FRAMERATE):
					if(TRUE_ITER % 10 != 0):
						continue
				CSV_ITER += 1 # Unique name for individual pdfs and csvs to be generated
				currPositionDict = dict() # new dictionary to track current row's positionings

				getAllPositionsAndEulers(currPositionDict, l)
				generateGraph(currPositionDict, l, len(lines), posYMinMax)
				#createIntermediateCsv(currPositionDict, l)

	createFinalOutputs(currCSV)


def getAllCsvs():
	return glob.glob(DATA_PATH + "*csv")

def main():
	CSV_TO_RUN = getAllCsvs()
	for currCSV in CSV_TO_RUN:
		try:
			runPipeline(currCSV)
		except KeyboardInterrupt:
			removeIntermediateFiles()
		finally:
			removeIntermediateFiles()

if __name__=='__main__':
    main()
