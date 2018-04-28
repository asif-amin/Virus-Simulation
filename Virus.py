import numpy
import random


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """        
        return random.random() < self.clearProb

    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # Does the virus reproduce?        
        maxReproduceProb = self.maxBirthProb * (1 - popDensity)
        
        if random.random() < maxReproduceProb:
            childOfVirus = SimpleVirus(self.maxBirthProb, self.clearProb)
            return childOfVirus
        
        else: raise NoChildException('Child not created!')
class ResistantVirus(SimpleVirus):
    """ 
    Representation of a virus which can have drug resistance.
    """     
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """  Initialize a ResistantVirus instance, saves all parameters as
        attributes of the instance.  maxBirthProb: Maximum reproduction
        probability (a float between 0-1)  clearProb: Maximum clearance
        probability (a float between 0-1). resistances: A dictionary of
        drug names (strings) mapping to the state of this virus
        particle's resistance (either True or False) to each drug. e.g.
        {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.
        mutProb: Mutation probability for this virus particle (a float).
        This is the probability of the offspring acquiring or losing
        resistance to a drug. """
        # TODO
        self.maxBirthProb=maxBirthProb
        self.clearProb=clearProb
        self.resistances=resistances
        self.mutProb=mutProb


        
    def isResistantTo(self, drug):
        """  Get the state of this virus particle's resistance to a drug. This
        method  is called by getResistPop() in Patient to determine how
        many virus  particles have resistance to a drug.  drug: The drug
        (a string)  returns: True if this virus instance is resistant to
        the drug, False  otherwise.  """
        # TODO
        try:return self.resistances[drug]
        except:return False
        
    def reproduce(self, popDensity, activeDrugs):
        """ Stochastically determines whether this virus particle reproduces at
        a  time step. Called by the update() method in the Patient
        class.  A virus particle will only reproduce if it is resistant
        to ALL the drugs  in the activeDrugs list. For example, if there
        are 2 drugs in the  activeDrugs list, and the virus particle is
        resistant to 1 or no drugs,  then it will NOT reproduce.  Hence,
        if the virus is resistant to all drugs  in activeDrugs, then the
        virus reproduces with probability:  self.maxBirthProb * (1 -
        popDensity).  If this virus particle reproduces, then
        reproduce() creates and returns  the instance of the offspring
        ResistantVirus (which has the same  maxBirthProb and clearProb
        values as its parent).  For each drug resistance trait of the
        virus (i.e. each key of  self.resistances), the offspring has
        probability 1-mutProb of  inheriting that resistance trait from
        the parent, and probability  mutProb of switching that
        resistance trait in the offspring.  For example, if a virus
        particle is resistant to guttagonol but not  grimpex, and
        `self.mutProb` is 0.1, then there is a 10% chance that  that the
        offspring will lose resistance to guttagonol and a 90%  chance
        that the offspring will be resistant to guttagonol.  There is
        also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be
        resistant to  grimpex.  popDensity: the population density (a
        float), defined as the current  virus population divided by the
        maximum population  activeDrugs: a list of the drug names acting
        on this virus particle  (a list of strings).  returns: a new
        instance of the ResistantVirus class representing the  offspring
        of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.  """
        # TODO

        resistAll = True
        for drug in activeDrugs:
            if (self.resistances[drug]==False):resistAll = False
                


        maxReproduceProb = self.maxBirthProb * (1 - popDensity)
        
        
        if (resistAll and random.random() < maxReproduceProb):
            childResistances = {}
            for drug in self.resistances:
                if random.random() < self.mutProb:
                    childResistances[drug] = (not self.resistances[drug])
                else:childResistances[drug] = (self.resistances[drug])

                
            childOfVirus = ResistantVirus(self.maxBirthProb, self.clearProb,childResistances,self.mutProb)
            return childOfVirus
        
        else: raise NoChildException('Child not created!')

