'''import random
import math
'''
from .Problems import Problem
from .Problems import Numeric

if __name__ == '__main__':
    problem = Problem()
    numeric = Numeric(problem)

    # Create an instance of numerical optimization problem
    numeric.createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    numeric.firstChoice()
    # Show the problem and algorithm settings
    numeric.describeProblem()
    numeric.displaySetting()
    # Report results
    numeric.displayResult()

'''
def createProblem():
    ## Read in an expression and its domain from a file.
    ## Then, return a problem.
    fileName = input("Enter the file name of a function: ")
    infile = open(fileName, 'r')
    expression = infile.readline() # as a string
    varNames = []  # Variable names
    low = []       # Lower bounds
    up = []        # Upper bounds
    line = infile.readline()
    while line != '':
        data = line.split(',')  # read from CSV
        varNames.append(data[0])
        low.append(float(data[1]))
        up.append(float(data[2]))
        line = infile.readline()
    infile.close()
    domain = [varNames, low, up]
    return expression, domain

def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of values
    valueC = evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC

def randomInit(p): # Return a random initial point as a list
    domain = p[1]  # domain: [varNames, low, up]
    low, up = domain[1], domain[2]
    init = []
    for i in range(len(low)):              # For each variable
        r = random.uniform(low[i], up[i])  # take a random value
        init.append(r)
    return init    # list of values

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)

def randomMutant(current, p):
    # Pick a random locus
    i = random.randint(0, len(current) - 1)
    # Mutate the chosen locus
    if random.uniform(0, 1) > 0.5:
        d = DELTA
    else:
        d = -DELTA
    return mutate(current, i, d, p)

def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", DELTA)
    print("Max evaluations with no improvement: {0:,} iterations"
          .format(LIMIT_STUCK))

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple
'''
