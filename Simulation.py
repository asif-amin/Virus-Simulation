from Virus import *
from Patient import *
import numpy
import pylab

def virusCollection(numViruses, maxBirthProb, clearProb):
    viruses = []
    for virusNum in range(numViruses):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))
    return viruses
def resistantVirusCollection(numViruses, maxBirthProb, clearProb,resistances,mutProb):
    viruses = []
    for virusNum in range(numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb,resistances,mutProb))
    return viruses
    

#
# PROBLEM 2
#
def simulationWithoutDrug(numTrials = 20, numTimeSteps = 500):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.
    """
    random.seed()

    # Virus Characteristics.
    maxPop = 1000
    numViruses = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    
    dataMatrix = numpy.zeros(shape = (numTrials, numTimeSteps))    
    for trial in range(numTrials):        

        # Model a random patient with the given virus charateristics.        
        viruses = virusCollection(numViruses, maxBirthProb, clearProb)
        randPatientX = SimplePatient(viruses, maxPop)

        # Simulate the time-steps.
        dataMatrix[trial][0] = numViruses
        for time in range(1, numTimeSteps):
            dataMatrix[trial][time] = randPatientX.update()           
            
    # Statistical Analysis.
    meanData = dataMatrix.mean(0)
    time = numpy.arange(numTimeSteps) 
    stdData95_CI = dataMatrix.std(0) * 2
    selectedTime = numpy.arange(0, numTimeSteps, 10)

    # Ploting.
    pylab.plot(time, meanData)
    pylab.errorbar(time[selectedTime], meanData[selectedTime], stdData95_CI[selectedTime], fmt = 'o')    
    pylab.show()
    
def simulationWithDrug(numTrials = 20, numTimeSteps = 500):
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.
    """
    random.seed()

    # Virus Characteristics.
    maxPop = 1000
    numViruses = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances={'guttagonol':False}
    mutProb= 0.005
    dataMatrix = numpy.zeros(shape = (numTrials, numTimeSteps))    
    for trial in range(numTrials):        

        # Model a random patient with the given virus charateristics.        
        viruses = resistantVirusCollection(numViruses, maxBirthProb, clearProb,resistances,mutProb)
        randPatientX = Patient(viruses, maxPop)

        #Use drug on patient
        randPatientX.addPrescription('guttagonol')

        # Simulate the time-steps.
        dataMatrix[trial][0] = numViruses
        for time in range(1, numTimeSteps):
            dataMatrix[trial][time] = randPatientX.update()           
            
    # Statistical Analysis.
    meanData = dataMatrix.mean(0)
    time = numpy.arange(numTimeSteps) 
    stdData95_CI = dataMatrix.std(0) * 2
    selectedTime = numpy.arange(0, numTimeSteps, 10)

    # Ploting.
    pylab.plot(time, meanData)
    pylab.errorbar(time[selectedTime], meanData[selectedTime], stdData95_CI[selectedTime], fmt = 'o')    
    pylab.show()

simulationWithoutDrug(numTimeSteps = 150)
simulationWithDrug(numTimeSteps = 150)

