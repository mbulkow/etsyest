import csv
import neuralnet as nn
import numpy as np

def filestoarrays(filenameX, filenameY):
	""" takes csv and text files with each row an example, returns numpy arrays with each column an example """
	fileX = open(filenameX, 'r')
	linesX = fileX.readlines()
	fileX.close()
	fileY = open(filenameY, 'r')
	linesY = fileY.readlines()
	fileY.close()
	m = len(linesY)
	nx = len(linesX[0])-1
	ny = len(linesY[0])-1
	X = np.zeros((nx,m))
	Y = np.zeros((ny,m))
	for j in range(m):
		for i in range(nx):
			X[i,j] = int(linesX[2*j][i])
		for k in range(ny):
			Y[k, j] = int(linesY[j][k])
	return X, Y
	

X, Y = filestoarrays('Desktop\\etsyest\\tags.txt', 'Desktop\\etsyest\\favs.txt')
layerdims = [X.shape[0],5,1]
layerfunctions = ["relu","sigmoid"]
parameters = nn.neuralnet(X,Y,layerdims,layerfunctions,6000, .1)
activations = nn.forward_prop(X, parameters, layerdims, layerfunctions)
Yhat = activations["A2"]
predict = (Yhat>.5)
numwrong = np.sum((Y-predict) != 0)
falsepos = np.sum((predict-Y) == 1)
print(numwrong)
print(falsepos)