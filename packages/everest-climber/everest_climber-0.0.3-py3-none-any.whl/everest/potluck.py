"""
Inspired by Andy Fundinger's talk at PyCaribbean.

PotLuck idea is to enable objects to be created dynamically that have
a list of delegates that can be used for each attribute.

Whenever anything is access we just pick at random from those available.

TODO:

Seeding of random number generators.

Code to track choices.
"""

import random

class GlobalPotLuck:
    """ Create a class attribute with this.

    All instances will share the same set of stuff.

    That might just work.
    """

    def __init__(self):


        self.choices = []

    def __get__(self, instance, owner):
        """ Pick one at random from those we know about """
        if len(self.choices) == 0:
            return None
        
        choice = random.randint(0, len(self.choices) - 1)
        return self.choices[choice]

    def __set__(self, instance, value):
        """ Append the value to the set available """
        self.choices.append(value)

    # FIXME - may need to do something about delete

class InstancePotLuck:
    """ Create a class attribute with this.

    Each instance will have its own set of potluck.

    That might just work.
    """

    def __init__(self, label):
        self.label = label
        
    def __get__(self, instance, owner):

        choices = instance.__dict__.get(self.label)
        if not choices:
            return None
        
        choice = random.randint(0, len(choices) - 1)
        return choices[choice]
        
    
    def __set__(self, instance, value):

        choices = instance.__dict__.get(self.label)
        if choices is None:
            choices = []
            instance.__dict__[self.label] = choices
        choices.append(value)
    

    # FIXME - need to do something about delete

PotLuck = GlobalPotLuck    

if __name__ == '__main__':

    class Hurricanes:

        how_many = PotLuck()

        events = PotLuck()

        sample = PotLuck()

    def sample1():
        return 12

    def sample2():
        return 20


    h = Hurricanes()

    h.sample = sample1

    setattr(h, 'sample', sample2)

    print("10 samples, should see mix of 12 and 10")
    for x in range(10):
        print(h.sample())

    print('hurricane2')
    h2 = Hurricanes()

    print(h2.sample())

    print(h2.events)


    Hurricanes.foo = PotLuck()

    h2.foo = sample1

    print(h2.foo())
    
    Hurricanes.bar = InstancePotLuck('bar')

    h2.bar = sample1
    h2.bar = sample2

    for x in range(10):
        print(h2.bar())

    print("h.bar should return None")
    print(h.bar)
