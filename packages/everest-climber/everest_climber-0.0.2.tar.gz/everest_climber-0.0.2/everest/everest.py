"""
================

Event Generation
================

Starting at the top, with event generation, everest seems like the
obvious choice.

Trivia
======

So Everest is the highest, at least above sea level.  As far as I am
aware there is no danger of it losing that title any time soon.  Maybe
an asteroid hit might have something to say about it.

But there other mountains that can claim the record of the hightest.

The earth bulges along the equator, so the closer you are to the
equator, the further sea level is from the centre of the earth.

The summit of Chimborazo in Ecuador is the furthest point on earth from
the centre. It is just 1 degree south of the equator.  From wikipedia:

     The summit of Mount Everest reaches a higher elevation above sea
     level, but the summit of Chimborazo is widely reported to be the
     farthest point on the surface from Earth's center, with
     Huascarán a very close second. The summit of the Chimborazo is
     the fixed point on Earth which has the utmost distance from the
     center – because of the oblate spheroid shape of the planet Earth
     which is "thicker" around the Equator than measured around the
     poles.  Chimborazo is one degree south of the Equator and
     the Earth's diameter at the Equator is greater than at the
     latitude of Everest (8,848 m (29,029 ft) above sea level), nearly
     27.6° north, with sea level also elevated. Despite being 2,580 m
     (8,465 ft) lower in elevation above sea level, it is 6,384.4 km
     (3,967.1 mi) from the Earth's center, 2,168 m (7,113 ft) farther
     than the summit of Everest (6,382.3 km (3,965.8 mi) from the
     Earth's center).[note 4] However, by the criterion of elevation
     above sea level, Chimborazo is not even the highest peak of the
     Andes.

And then there is the question, which mountain on earth has the
longest climb.  You could argue the answer is Chimborazo.  Start at
the point under the ocean that is closest to the centre of the earth
and work your way to the summit.

Mount Lamlam (meaning lightning in Chamoru) is a peak on the United
States island of Guam. It is located near the village of Agat (5 km or
3 mi[3] north), in the southwest of the island.

Rising to 406 meters (1,332 ft) above sea level, it is the highest
peak in Guam (before Mount Jumullong Manglo). The distance from the
peak to the bottom of the nearby Mariana Trench is the greatest change
in elevation on Earth over such a short distance.

So, if you go to Guam and make the modest 1300 foot climb you can
arguably claim to be on the tallest mountain on earth.


LICENSE
=======

FIXME: add a license file
GPL v 3
"""
import os
import json
import importlib
from collections import defaultdict

import pandas as pd
import numpy as np

class Everest(object):
    """ A mountain of events

    The events come from separate hills, or EventGenerators.
    """
    def __init__(self):
        """ Initialise Everest """
        self.hills = defaultdict(list)
        
    def load(self, folder=None):
        """ Load a model by recursively scanning a folder for model pieces

        If folder is not given, use current working directory.
        """
        if folder is None:
            folder = '.'

        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if filename.endswith('.json'):
                    fullpath = os.path.join(dirpath, filename)
                    with open(fullpath) as infile:
                        json_data = infile.read()
                        print(json_data)
                        data = json.loads(json_data)

                    clazz = self._get_class(data.get('class', 'everest.everest.EventGenerator'))

                    name = data.get('name', 'unknown')

                    self.hills[name].append(clazz(data))

    def dump(self):
        """ Dump out current model """
        print(self.hills)


    def _get_class(self, path):
        """ Given a path, return the clazz """
        path = path.split('.')

        module_name = '.'.join(path[:-1])

        module = importlib.import_module(module_name)

        return getattr(module, path[-1])


    def seed(self, seed):
        """ Seed random number generators """
        pass

    def generate_trials(self, start=0, end=1000, start_time=None, end_time=None):
        """ Generate trials of events.

        Each trial covers a period from start_time to end_time.

        Trials will be numbered from start to end-1.

        Seeding of random number generators will be such that the same
        results will be returned given the same input parameters.

        start: datetime object, default datetime.datetime.now()

        end: datetime object, defauilt datetime.datetime.now + 1 year  """

    def generate_trial(self, trial_number=None, start_time=None, end_time=None):
        pass

class EventGenerator(object):

    def __init__(self, parms=None):

        if parms:
            self.__dict__.update(parms)

    def initialise(self):
        """ Do stuff like setting up random number seeds 

        Also load pools of events and their frequencies.
        """
        pass

    def generate_trials(n=1):
        """ Generate n trials of events """
        for trial in range(n):
            yield self.generate_trial()

    def generate_trial():
        """ Generate a single trial of events """
        pass


class Event(object):
    pass


class WeightedEventSampler(object):
    """ Given n objects with weights w_1, ... 2_n select m of them 

    For example:

    >>> data = {a=1., b=2., c=3.}
    
    >>> sampler = WeightedEventSampler(data)

    >>> sampler.sample(1)
    """
    def __init__(self, data):
        """ """
        self.data = data
        self.total_weight = sum(data[x] for x in data)

    def sample(self, n):

        delta = self.total_weight / n

        
        
        


class Poisson(EventGenerator):


    def generate_trial():

        # Get number of events
        for trial in range(n):
            yield self.generate_trial()


            
