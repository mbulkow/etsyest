import numpy as np
epsilon = 10e-8
cap = 800
upperlimitJ = 10000

def sigmoid(x):
	return 1./(1.+np.exp(-x))

def cappedsigmoid(x):
	y = np.maximum(x,-cap)
	return 1./(1.+np.exp(-y))
	
def initialize_parameters(layersdims):
	""" randomly initialize parameters W and set parameters b to zero"""
	parameters = {}
	L = len(layersdims) -1
	for l in range(L):
		parameters["W" + str(l+1)] = np.random.randn(layersdims[l+1],layersdims[l])*.01
		parameters["b" + str(l+1)] = np.zeros((layersdims[l+1],1))
	return parameters
	
def forward_prop(X, parameters, layersdims, layerfunctions):
	""" performs forward propogation on a neural zet with input X """
	L = len(layersdims)-1
	activations = {}
	activations["A0"] = X
	for l in range(L):
		activations["Z" + str(l+1)] = np.dot(parameters["W"+str(l+1)], activations["A" + str(l)]) + parameters["b"+str(l+1)]
		if layerfunctions[l] == "relu":
			activations["A" + str(l+1)] = np.maximum(activations["Z" + str(l+1)],0)
		elif layerfunctions[l] == "sigmoid":
			activations["A" + str(l+1)] = cappedsigmoid(activations["Z" + str(l+1)])
		else:
			print("Function for layer " + str(l+1) + "not supported")
	return activations
	
def compute_cost(Yhat, Y, activationtype):
	"""compute cost between predicted and actual final layer """
	m = Y.shape[1]
	if activationtype == "relu":
		return (1./(2.*m))*np.sum(np.dot((Y-Yhat).T,Y-Yhat))
	elif activationtype == "sigmoid":
		return -(1./m)*np.sum(np.multiply(Y,np.log(Yhat+epsilon))+np.multiply(1-Y,np.log(1-Yhat+epsilon)))
	else:
		print("Final activation function not supported")
		return 0

def back_prop(Y, parameters, layersdims, activations, layerfunctions):
	""" performs back propogation """
	L = len(layersdims)-1
	m = Y.shape[1]
	grads = {}
	if layerfunctions[L-1] == "relu":
		dAl = (1./m)*(Y-activations["A"+str(L)])
		dZl = np.multiply((activations["Z"+str(L)]>0),dAl)
	elif layerfunctions[L-1] == "sigmoid":
		#dAl = -(1./m)*(np.divide(Y,Yhat)-np.divide(1-Y,1-Yhat)
		dZl = (1./m)*np.multiply((activations["A"+str(L)] - Y),(activations["Z"+str(L)]>-cap))
	else:
		print("Final activation function not supported")
	grads["dW"+str(L)] = np.dot(dZl,activations["A"+str(L-1)].T)
	grads["db"+str(L)] = np.sum(dZl,axis = 1, keepdims = True)
	dAlminusone = np.dot(parameters["W"+str(L)].T,dZl)
	for s in range(L-1):
		l = L - s - 1
		if layerfunctions[l] == "relu":
			dZl = np.multiply((activations["Z"+str(l)]>0),dAlminusone)
		elif layerfunctions[l] == "sigmoid":
			mask = (activations["Z"+str(l)]>-cap)
			dZl = np.multiply(np.multiply(activations["A"+str(l)]*(1-activations["A"+str(l)]),dAlminusone),mask)
		else:
			print("Activation function not supported")
		grads["dW"+str(l)] = np.dot(dZl,activations["A"+str(l-1)].T)
		grads["db"+str(l)] = np.sum(dZl,axis = 1, keepdims = True)
		dAlminusone = np.dot(parameters["W"+str(l)].T,dZl)
	return grads

def update_parameters(parameters, grads, L, learningrate):
	for l in range(L):
		parameters["W"+str(l+1)] = parameters["W"+str(l+1)] - learningrate*grads["dW"+str(l+1)]
		parameters["b"+str(l+1)] = parameters["b"+str(l+1)] - learningrate*grads["db"+str(l+1)]
	return parameters
	
def neuralnet(X, Y, layersdims, layersfunctions, iterations, learningrate):
	parameters = initialize_parameters(layersdims)
	L = len(layersdims)-1
	for i in range(iterations):
		activations = forward_prop(X, parameters, layersdims, layersfunctions)
		J = compute_cost(activations["A"+str(L)],Y, layersfunctions[L-1])
		if i % 100 == 1:
			print(J)
		grads = back_prop(Y, parameters, layersdims, activations, layersfunctions)
		parameters = update_parameters(parameters, grads, L, learningrate)
	return parameters
	
	
"""
X = np.array([[0.1,1.],[0.1,1.],[0.1,1.],[0.1,1],[0.1,1.]])
Y = np.array([[0.,1.]])
layersdims = [5,1,1]
layersfunctions = ["relu","sigmoid"]
parameters = neuralnet(X, Y, layersdims, layersfunctions, 10000, 1.)
"""





