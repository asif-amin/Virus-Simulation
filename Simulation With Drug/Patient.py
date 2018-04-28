from Virus import *


class SimplePatient(object):
    
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    
    def __init__(self, viruses, maxPop):
        
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        errorMsg1 = 'viruses must be a list containing SimpleVirus objects'
        errorMsg2 = 'maxPop, or maximum virus population must be an integer!'
        
        if type(viruses) != list: raise ValueError(errorMsg1)
        self.viruses = viruses
                
        if type(maxPop)!= int: raise ValueError(errorMsg2)
        self.maxPop = maxPop

    def getTotalPop(self):
        
        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        
        # Determine number of viruses to be cleaned, "stochastically".
        numRemoveVirus = 0
        for virus in self.viruses:
            if virus.doesClear():
                numRemoveVirus += 1

        
        

        # Remove numRemoveVirus from the patient's body.
        for virusNum in range(numRemoveVirus):
            self.viruses.pop()

        # Calculate population density. TO DO check (keep self!)
        popDensity = self.getTotalPop()/float(self.maxPop)
        
        if popDensity >= 1:
            print 'virus population reached maximum!'
            popDensity = 1       

        # Reproduce at a single time step.
        offspringViruses = []
        for virus in self.viruses:
            try:
                offspringViruses.append(virus.reproduce(popDensity))
            except NoChildException: pass
            
        self.viruses = self.viruses + offspringViruses
        
        return self.getTotalPop()

class Patient(SimplePatient):
    """  Representation of a patient. The patient is able to take drugs and
    his/her  virus population can acquire resistance to the drugs he/she
    takes.
    """  
    def __init__(self, viruses, maxPop):
        """  Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being
        administered (which should initially include no drugs).
        viruses: The list representing the virus population (a list of
        SimpleVirus instances)  maxPop: The  maximum virus population
        for this patient (an integer)  """

        errorMsg1 = 'viruses must be a list containing SimpleVirus objects'
        errorMsg2 = 'maxPop, or maximum virus population must be an integer!'
        
        if type(viruses) != list: raise ValueError(errorMsg1)
        self.viruses = viruses
                
        if type(maxPop)!= int: raise ValueError(errorMsg2)
        self.maxPop = maxPop

        self.drugs = []
        
    def addPrescription(self, newDrug):
        """  Administer a drug to this patient. After a prescription is
        added, the  drug acts on the virus population for all subsequent
        time steps. If the  newDrug is already prescribed to this
        patient, the method has no effect.  newDrug: The name of the
        drug to administer to the patient (a string).  postcondition:
        The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)
        
    def getPrescriptions(self):
        """  Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to
        this  patient.  """
        return self.drugs  
    def getResistPop(self, drugResist):
        """  Get the population of virus particles resistant to the drugs listed
        in  drugResist.  drugResist: Which drug resistances to include
        in the population (a list  of strings - e.g. ['guttagonol'] or
        ['guttagonol', 'grimpex'])

        returns: The population of viruses
        (an integer) with resistances to all  drugs in the drugResist
        list.  """
        resistPop=0
        for virus in self.viruses:
            resistAll=True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistAll= False
            if resistAll: resistPop+=1

        return resistPop
                               
    def update(self):
        """  Update the state of the virus population in this patient for a
        single  time step. update() should execute these actions in
        order:
        - Determine whether each virus particle survives and
        update the list of virus particles accordingly
        - The current population density is calculated. This population density  value
        is used until the next call to update().
        - Determine whether each virus particle should reproduce and add offspring virus
        particles to the list of viruses in this patient.The listof
        drugs being administered should be accounted for in the
        determination of whether each virus particle reproduces.
        returns: The total virus population at the end of the update (an
        integer)  """
        # Determine number of viruses to be cleaned, "stochastically".
        numRemoveVirus = 0
        for virus in self.viruses:
            if virus.doesClear():
                numRemoveVirus += 1

        
        

        # Remove numRemoveVirus from the patient's body.
        for virusNum in range(numRemoveVirus):
            self.viruses.pop()

        # Calculate population density. TO DO check (keep self!)
        popDensity = self.getTotalPop()/float(self.maxPop)
        
        if popDensity >= 1:
            print 'virus population reached maximum!'
            popDensity = 1

        # Reproduce at a single time step,taking drugs into account.
        offspringViruses = []
        for virus in self.viruses:
            try:
                offspringViruses.append(virus.reproduce(popDensity,self.drugs))
            except NoChildException: pass
            
        self.viruses = self.viruses + offspringViruses
        
        return self.getTotalPop()
        
