from setup import Setup
import random
import math

class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0
        self._aType = 0
        self._limitStuck = 100 # Max evaluations with no improvement
        self._numExp = 0
        self._numRestart = 0

    def setVariables(self, parameters):
        self._pType = parameters['pType']
        self._aType = parameters['aType']
        self._limitStuck = parameters['limitStuck']
        self._numExp = parameters['numExp']
        self._numRestart = parameters['numRestart']


    def getAType(self):
        return self._aType

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print("Number of experiments: ", self._numExp)

    def displaySetting(self):
        if self._pType == 1 and self._aType != 4 and self._aType != 6:
            print()
            print("Mutation step size:", self._delta)


class HillClimbing(Optimizer):
    def displaySetting(self):
        print()
        print("Number of restarts: ", self._numRestart)
        Optimizer.displaySetting(self)

    def randomRestart(self, p):
        sa = SteepestAscent()
        fc = FirstChoice()
        st = Stochastic()
        gd = GradientDescent()

        if self._pType == 2:
            randValue = random.randint(1, 3)
        else:
            randValue = random.randint(1, 4)
        if randValue == 1:
            sa.run(p)
        elif randValue == 2:
            fc.run(p)
        elif randValue == 3:
            st.run(p)
        else:
            gd.run(p)

    def run(self):
        pass


class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Steepest-Ascent Hill Climbing")
        HillClimbing.displaySetting(self)

    def run(self, p):
        current = p.randomInit()  # A current candidate solution
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)

    def bestOf(self, neighbors, p):
        best = neighbors[0]
        bestValue = p.evaluate(best)
        for i in range(1, len(neighbors)):
            newValue = p.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue = newValue
        return best, bestValue


class FirstChoice(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: First-Choice Hill Climbing")
        HillClimbing.displaySetting(self)
        print("Max evaluations with no improvement: {0:,} iterations"
              .format(self._limitStuck))

    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)

class Stochastic(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Stochastic Hill Climbing")
        HillClimbing.displaySetting(self)

    def run(self, p):
        current = p.randomInit()  # A current candidate solution
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.stochasticBest(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)

    def stochasticBest(self, neighbors, p):
        # Smaller valuse are better in the following list
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]

class GradientDescent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Gradient Descent")
        print()
        print("Update rate:", self._alpha)
        print("Increment for calculating derivatives:", self._dx)

    def run(self, p):
        currentP = p.randomInit()  # Current point
        valueC = p.evaluate(currentP)
        while True:
            nextP = p.takeStep(currentP, valueC)
            valueN = p.evaluate(nextP)
            if valueN >= valueC:
                break
            else:
                currentP = nextP
                valueC = valueN
        p.storeResult(currentP, valueC)




class Metaheuristic(Optimizer):
    def __init__(self):
        self._bestFound = 0
        self._numSample = 100

    def displaySetting(self):
        Optimizer.displaySetting(self)

    def getWhenBestFound(self):
        return self._bestFound

    def run(self, p):
        pass

class SimulatedAnnealing(Metaheuristic):###
    def displaySetting(self):
        print()
        print("Search Algorithm: Simulated Annealing")

    def run(self, p):
        self._bestFound = 0
        current = p.randomInit()
        current_temp = self.initTemp(p)
        valueC = p.evaluate(current)
        final_temp = .01
        while current_temp > final_temp:
            self._bestFound += 1
            neighbor = p.randomMutant(current)
            valueN = p.evaluate(neighbor)
            diff = valueC - valueN
            if diff > 0:
                current = neighbor
                valueC = valueN
            else:
                if random.uniform(0, 1) < math.exp(-diff / current_temp):
                    current = neighbor
                    valueC = valueN
            current_temp = self.tSchedule(current_temp)
        p.storeResult(current, valueC)

    def initTemp(self, p): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()     # A random point
            v0 = p.evaluate(c0)     # Its value
            c1 = p.randomMutant(c0) # A mutant
            v1 = p.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample  # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))


class GA(Metaheuristic):
    def __init__(self):
        Metaheuristic.__init__(self)
        self._resolution = 5
        self._popSize = 0     # Population size
        self._uXp = 0   # Probability of swappping a locus for Xover
        self._mrF = 0   # Multiplication factor to 1/n for bit-flip mutation
        self._XR = 0    # Crossover rate for permutation code
        self._mR = 0    # Mutation rate for permutation code
        self._pC = 0    # Probability parameter for Xover
        self._pM = 0    # Probability parameter for mutation

    def setVariables(self, parameters):
        Metaheuristic.setVariables(self, parameters)
        self._popSize = parameters['popSize']
        self._uXp = parameters['uXp']
        self._mrF = parameters['mrF']
        self._XR = parameters['XR']
        self._mR = parameters['mR']
        if self._pType == 1:
            self._pC = self._uXp
            self._pM = self._mrF
        if self._pType == 2:
            self._pC = self._XR
            self._pM = self._mR

    def displaySetting(self):
        print()
        print("Search Algorithm: Genetic Algorithm")
        print()
        Metaheuristic.displaySetting(self)
        print()
        print("Population size:", self._popSize)
        if self._pType == 1:   # Numerical optimization
            print("Number of bits for binary encoding:", self._resolution)
            print("Swap probability for uniform crossover:", self._uXp)
            print("Multiplication factor to 1/L for bit-flip mutation:",
                  self._mrF)
        elif self._pType == 2: # TSP
            print("Crossover rate:", self._XR)
            print("Mutation rate:", self._mR)

    def runGA(self, p):
        generation = 0
        population = p.initializePop(self._popSize)
        for i in range(self._popSize):
            p.evalInd(population[i])
        population.sort()

        while population[0][0] > 0.001:
            generation += 1
            if generation > 1000:
                break
            for i in range(self._popSize):
                if i == self._popSize-1:
                    population[i], population[0] = p.crossover(population[i], population[0], self._pC)
                    p.evalInd(population[0])
                else:
                    population[i], population[i + 1] = p.crossover(population[i], population[i + 1], self._pC)
                population[i] = p.mutation(population[i], self._pM)
                p.evalInd(population[i])
            population.sort()

        p.storeResult(p.indToSol(population[0]), population[0][0])

