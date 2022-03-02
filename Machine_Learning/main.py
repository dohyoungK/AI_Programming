import numpy as np
import math

def main():
    print("Which learning algorithm do you want to use?")
    print(" 1. Linear Regression")
    print(" 2. k-NN")
    aType = int(input("Enter the number: "))

    if aType == 1:
        lr = LinearRegression(aType)
        fileName = input("Enter the file name of training data: ")
        lr.setData('train', fileName)
        fileName = input("Enter the file name of test data: ")
        lr.setData('test', fileName)
        lr._w = lr.linearRegression()
        lr.testModel()
        lr.report()
    elif aType == 2:
        knn = kNN(aType)
        fileName = input("Enter the file name of training data: ")
        knn.setData('train', fileName)
        fileName = input("Enter the file name of test data: ")
        knn.setData('test', fileName)
        knn._k = int(input("Enter the value for k: "))
        knn.testModel()
        knn.report()


class ML:
    def __init__(self, aType):
        self._trainDX = np.array([]) # Feature value matrix (training data)
        self._trainDy = np.array([]) # Target column (training data)
        self._testDX = np.array([])  # Feature value matrix (test data)
        self._testDy = np.array([])  # Target column (test data)
        self._testPy = np.array([])  # Predicted values for test data
        self._rmse= 0                # Root mean squared error
        self._aType = aType          # Type of learning algoritm

    def setData(self, dtype, fileName): # set class variables
        XArray, yArray = self.createMatrices(fileName)
        if dtype == 'train':
            self._trainDX = XArray
            self._trainDy = yArray
        elif dtype == 'test':
            self._testDX = XArray
            self._testDy = yArray
            self._testPy = np.zeros(np.size(yArray)) # Initialize to all 0
            
    def createMatrices(self, fileName): # Read data from file and make arrays
        infile = open(fileName, 'r')
        XSet = []
        ySet = []
        for line in infile:
            data = [float(x) for x in line.split(',')]
            features = data[0:-1]
            target = data[-1]
            XSet.append(features)
            ySet.append(target)
        infile.close()
        XArray = np.array(XSet)
        yArray = np.array(ySet)
        return XArray, yArray

    def testModel(self):
        n = np.size(self._testDy)
        if self._aType == 1:
            self.testLR(n)
        elif self._aType == 2:
            self.testKNN(n)

    def report(self):
        self.calcRMSE()
        print()
        print("RMSE: ", round(self._rmse, 2))

    def calcRMSE(self):
        n = np.size(self._testDy) # Number of test data
        totalSe = 0
        for i in range(n):
            se = (self._testDy[i] - self._testPy[i]) ** 2
            totalSe += se
        self._rmse = np.sqrt(totalSe) / n


class LinearRegression(ML):
    def __init__(self, aType):
        ML.__init__(self, aType)
        self._w = np.array([])  # Optimal weights for linear regression

    def linearRegression(self): # Do linear regression and return optimal w
        X = self._trainDX
        n = np.size(self._trainDy)
        X0 = np.ones([n, 1])
        nX = np.hstack((X0, X)) # Add a column of all 1's as the first column
        y = self._trainDy
        t_nX = np.transpose(nX)
        return np.dot(np.dot(np.linalg.inv(np.dot(t_nX, nX)), t_nX), y)

    def testLR(self, n):  # Test linear regression with the test set
        for i in range(n):
            self._testPy[i] = self.LR(self._testDX[i])

    def LR(self, data):  # Apply linear regression to a test data
        nData = np.insert(data, 0, 1)
        return np.inner(self._w, nData)


class kNN(ML):
    def __init__(self, aType):
        ML.__init__(self, aType)
        self._k = 0            # k value for k-NN

    def testKNN(self, n): # Apply k-NN to the test set
        #self._testDy = self.zScoreNormalization(self._testDy)
        for i in range(n):
            self._testPy[i] = self.kNN(self._testDX[i])

    ### Implement the following and other necessary methods
    def kNN(self, query):
        distance = []
        dist = 0
        sum = 0
        n = np.size(self._testDy)
        for i in range(n):
            lst = []
            dist = math.sqrt(math.pow(self._testDX[i][0]-query[0], 2) + math.pow(self._testDX[i][1]-query[1], 2) + math.pow(self._testDX[i][2]-query[2], 2))
            lst.append(dist)
            lst.append(self._testDy[i])
            distance.append(lst)
        distance.sort()
        distance = distance[1:self._k+1]

        for i in range(self._k):
            sum += distance[i][1]
        mean = sum / self._k

        return mean

#    def zScoreNormalization(self, lst):
#        normalized = []
#        for value in lst:
#            normalized_num = (value - np.mean(lst)) / np.std(lst)
#            normalized.append(round(normalized_num, 1))
#
#        return normalized

main()
