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
    


def problem4_multipleDrugs(numTrials=20,delayTimeSteps=300,treatmentSteps=150):
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).
    """
    random.seed()

    # Virus Characteristics.
    maxPop = 1000
    numViruses = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances={'guttagonol':False,'grimpex':False}
    mutProb= 0.005
    dataMatrix = numpy.zeros(shape = (numTrials, delayTimeSteps+(2*treatmentSteps)))
    finalCount=[]
    for trial in range(numTrials):
        if trial%50==0:print trial+1

        # Model a random patient with the given virus charateristics.        
        viruses = resistantVirusCollection(numViruses, maxBirthProb, clearProb,resistances,mutProb)
        randPatientX = Patient(viruses, maxPop)


        # wait before adminstering guttagonol.
        dataMatrix[trial][0] = numViruses
        for time in range(1, treatmentSteps):
            dataMatrix[trial][time] = randPatientX.update()

        #Use guttagonol on patient
        randPatientX.addPrescription('guttagonol')

        # wait before using grimpex 
        for time in range(treatmentSteps,delayTimeSteps+treatmentSteps):
            dataMatrix[trial][time] = randPatientX.update()

        #Use grimpex on patient
        randPatientX.addPrescription('grimpex')

        # wait 150 steps for combined effect 
        for time in range(treatmentSteps+delayTimeSteps,delayTimeSteps+(2*treatmentSteps)):
            dataMatrix[trial][time] = randPatientX.update()

        
        finalCount.append(dataMatrix[trial][delayTimeSteps+treatmentSteps-1])
            
    # Statistical Analysis.
    meanData = dataMatrix.mean(0)
    time = numpy.arange(delayTimeSteps+treatmentSteps) 
    stdData95_CI = dataMatrix.std(0) * 2
    selectedTime = numpy.arange(0, delayTimeSteps+treatmentSteps, 10)

    # Plotting.
    n, bins, patches = pylab.hist(finalCount,100,facecolor='red')
    pylab.xlabel('Virus Population After 50 Steps of combined Drug Use')
    pylab.ylabel('Number of Patients')
    pylab.title('Effect of Delayed Second Drug - Delay : '+ str(delayTimeSteps)+' Steps' )
    pylab.show()


problem4_multipleDrugs(numTrials=250,delayTimeSteps=300,treatmentSteps=50)
problem4_multipleDrugs(numTrials=250,delayTimeSteps=150,treatmentSteps=50)
problem4_multipleDrugs(numTrials=250,delayTimeSteps=75,treatmentSteps=50)
problem4_multipleDrugs(numTrials=250,delayTimeSteps=0,treatmentSteps=50)
problem4_multipleDrugs(numTrials=250,delayTimeSteps=40,treatmentSteps=50)
problem4_multipleDrugs(numTrials=250,delayTimeSteps=45,treatmentSteps=50)


