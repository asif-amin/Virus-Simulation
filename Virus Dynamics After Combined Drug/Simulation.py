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
    

def problem5_populationDynamics(numTrials=20,delayTimeSteps=300,treatmentSteps=150):
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
    guttagonolResistantCount = numpy.zeros(shape = (numTrials, delayTimeSteps+(2*treatmentSteps)))
    grimpexResistantCount = numpy.zeros(shape = (numTrials, delayTimeSteps+(2*treatmentSteps)))
    completelyResistantCount= numpy.zeros(shape = (numTrials, delayTimeSteps+(2*treatmentSteps)))
    for trial in range(numTrials):
        if trial%50==0:print trial+1

        # Model a random patient with the given virus charateristics.        
        viruses = resistantVirusCollection(numViruses, maxBirthProb, clearProb,resistances,mutProb)
        randPatientX = Patient(viruses, maxPop)


        # wait before adminstering guttagonol.
        dataMatrix[trial][0] = numViruses
        guttagonolResistantCount[trial][0] =0
        grimpexResistantCount[trial][0] =0
        completelyResistantCount[trial][0] =0
        for time in range(1, treatmentSteps):
            dataMatrix[trial][time] = randPatientX.update()
            guttagonolResistantCount[trial][time] =randPatientX.getResistPop(['guttagonol'])
            grimpexResistantCount[trial][time] =randPatientX.getResistPop(['grimpex'])
            completelyResistantCount[trial][time] =randPatientX.getResistPop(['guttagonol','grimpex'])

        #Use guttagonol on patient
        randPatientX.addPrescription('guttagonol')

        # wait before using grimpex 
        for time in range(treatmentSteps,delayTimeSteps+treatmentSteps):
            dataMatrix[trial][time] = randPatientX.update()
            guttagonolResistantCount[trial][time] =randPatientX.getResistPop(['guttagonol'])
            grimpexResistantCount[trial][time] =randPatientX.getResistPop(['grimpex'])
            completelyResistantCount[trial][time] =randPatientX.getResistPop(['guttagonol','grimpex'])

        #Use grimpex on patient
        randPatientX.addPrescription('grimpex')

        # wait 150 steps for combined effect 
        for time in range(treatmentSteps+delayTimeSteps,delayTimeSteps+(2*treatmentSteps)):
            dataMatrix[trial][time] = randPatientX.update()
            guttagonolResistantCount[trial][time] =randPatientX.getResistPop(['guttagonol'])
            grimpexResistantCount[trial][time] =randPatientX.getResistPop(['grimpex'])
            completelyResistantCount[trial][time] =randPatientX.getResistPop(['guttagonol','grimpex'])

        
        
            


    # Statistical Analysis.
    meanData = dataMatrix.mean(0)
    time = numpy.arange(delayTimeSteps+2*treatmentSteps)
    meanData2 = guttagonolResistantCount.mean(0)
    meanData3=grimpexResistantCount.mean(0)
    meanData4=completelyResistantCount.mean(0)
    
    stdData95_CI = dataMatrix.std(0) * 2
    selectedTime = numpy.arange(0, delayTimeSteps+treatmentSteps, 10)

    # Plotting.
    pylab.plot(time, meanData,label='Virus Population')
    pylab.plot(time, meanData2,label='Guttagonol Resistant Population')
    pylab.plot(time, meanData3,label='Grimpex Resistant Population')
    pylab.plot(time, meanData4,label='Completely Resistant Population')
    pylab.xlabel('Time-Steps')
    pylab.ylabel('Virus Population')
    #pylab.errorbar(time[selectedTime], meanData[selectedTime], stdData95_CI[selectedTime], fmt = 'o')
    pylab.legend(loc='upper right')
    pylab.show()


problem5_populationDynamics(numTrials=100,delayTimeSteps=300,treatmentSteps=150)
problem5_populationDynamics(numTrials=100,delayTimeSteps=0,treatmentSteps=150)

