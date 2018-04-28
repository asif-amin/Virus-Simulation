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
    dataMatrix = numpy.zeros(shape = (numTrials, numTimeSteps+150))
    resistPop = numpy.zeros(shape = (numTrials, numTimeSteps+150))
    for trial in range(numTrials):        

        # Model a random patient with the given virus charateristics.        
        viruses = resistantVirusCollection(numViruses, maxBirthProb, clearProb,resistances,mutProb)
        randPatientX = Patient(viruses, maxPop)


        # Simulate the time-steps.
        dataMatrix[trial][0] = numViruses
        dataMatrix[trial][0] = 0
        for time in range(1, numTimeSteps):
            dataMatrix[trial][time] = randPatientX.update()
            resistPop[trial][time] = randPatientX.getResistPop(['guttagonol'])
            
        #Use drug on patient
        randPatientX.addPrescription('guttagonol')

        # Simulate the time-steps.
        for time in range(numTimeSteps,numTimeSteps+150):
            dataMatrix[trial][time] = randPatientX.update()
            resistPop[trial][time] = randPatientX.getResistPop(['guttagonol'])

        
        
    # Statistical Analysis.
    meanData = dataMatrix.mean(0)
    meanData2=resistPop.mean(0)
    time = numpy.arange(numTimeSteps+150) 
    stdData95_CI = dataMatrix.std(0) * 2
    selectedTime = numpy.arange(0, numTimeSteps, 10)

    # Plotting.
    plot('Average Total Virus Population',time,meanData)
    plot('Average Resistant Virus Population',time,meanData2)

def plot(title,x,y):
    pylab.xlabel('Time-Steps')
    pylab.ylabel('Virus Population')
    pylab.title(title)
    pylab.plot(x,y)
    #pylab.errorbar(time[selectedTime], meanData[selectedTime], stdData95_CI[selectedTime], fmt = 'o')    
    pylab.show()
    

simulationWithDrug(numTimeSteps = 150)

