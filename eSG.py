from argparse import ArgumentParser
import random

def D( dice ):
   result = 0
   for d in range( dice ):
      roll = int( random.random() * 6 ) + 1
      result += roll
   return result
   

class SolarSystem():
   parser = ArgumentParser()
   parser.add_argument( '-s', '--stars', type=int, default=-1,
                        help='Number of stars in the system' )
   parser.add_argument( '-p', '--planets', type=int, default=-1,
                        help='Number of planets in the system' )
   parser.add_argument( '-n', '--natural-features', type=int, default=-1,
                        help='Number of natural features in the system' )
   parser.add_argument( '-t', '--tech-features', type=int, default=-1,
                        help='Number of technological features in the system' )
   parser.add_argument( '-i', '--infra-features', type=int, default=-1,
                        help='Number of infrastructure features in the system' )
   parser.add_argument( '-f', '--faction', type=list, default=['human'],
                        help='Who owns property in the system' )
   parser.add_argument( '-T', '--tech-level', type=int, default=-1,
                        help='Maximum tech level in the system' )
   parser.add_argument( '-D', '--danger-level', type=int, default=-1,
                        help='Maximum danger level in the system' )
   parser.add_argument( '-I', '--infra-level', type=int, default=-1,
                        help='How much infrastructure is it in the system' )
   parser.add_argument( '-H', '--habitability-level', type=int, default=-1,
                        help='How habitable is it in the system' )
   parser.add_argument( '-S', '--star-type', type=str, default='random',
                        choices=['random', 'yellow', 'red giant',
                                 'white dwarf', 'neutron' ],
                        help='Preferred star type in the system' )
   

   def __init__( self,
                 Stars=None,Planets=None, NaturalFeatures=None, TechFeatures=None,
                 InfraFeatures=None ):
      print "Generating SolarSystem"
      self.args = self.parser.parse_args()
      self.Stars = Stars or []
      self.Planets = Planets or []
      self.NaturalFeatures = NaturalFeatures or []
      self.TechFeatures = TechFeatures or []
      self.InfraFeatures = InfraFeatures or []

      self.star_reqs = {}
      self.planet_reqs = {}
      self.feature_reqs = {}

      self.orbits = []
      self.system_nature = None
      self.primary_star = None

      self.generateSystemRequirements( self.Stars, self.Planets,
                                       self.NaturalFeatures, 
                                       self.TechFeatures,
                                       self.InfraFeatures )

      #### Begin Expaned Star System Generation ####
      self.generateStarSystemFeatures()
      self.placeKnownComponents()
      self.generateWorlds()
      self.generateSatallites()
      self.designateMainWorld()

   def generateSystemRequirements( self, Stars, Planets, NaturalFeatures, 
                                   TechFeatures, InfraFeatures ):
      """ Accept input objects that the system must satisfy the requirements of """
      for i,star in enumerate( Stars ):
         self.star_reqs[i].update( star.star_reqs )
      for i,planet in enumerate( Planets ):
         self.planet_reqs[i].update( planet.planet_reqs )

   def generateStarSystemFeatures( self ):
      self.systemNature()
      self.createStars()
      self.zoneDetermination()
      self.capturedPlanetsAndEmptyOrbits()
      self.gasGiants()
      self.planetoids()

   def placeKnownComponents( self ):
      self.placeGasGiants()
      self.placePlanetoids()

   def generateWorlds( self ):
      for orbit in self.orbits:
         if not orbit.occupied:
            orbit.generateWorld()

   def generateSatallites( self ):
      for orbit in self.orbits:
         orbit.numberOfSatallites()
         orbit.generateSatallites()

   def designateMainWorld( self ):
      """ Choose the most appropriate world to be the 'main_world' """
      #TODO: Add Logic for 'most appropriate'
      self.orbits[0].body.is_main_world = True

      for orbit in self.orbits:
         orbit.determineAdditionalCharacteristics()

   def systemNature( self ):
      roll = D(2)
      if roll < 8:
         roll = 'solo'
      elif roll < 12:
         roll = 'binary'
      elif roll == 12:
         roll = 'trinary'
      self.system_nature = roll

   def createStars( self ):
      self.primary_star = PrimaryStar( self.system_nature )

class Orbit(object):
   def __init__( self, star, number ):
      self.star = star
      self.number = number
      self.occupied = False
      self.zone = None
      self.body = None

   def generateWorld( self ):
      self.occupied = True
      self.body = World( self.star, self, self.zone )

   def numberOfSatallites( self ):
      self.body.numberOfSatallites()

   def generateSatallites( self ):
      self.body.generateSatallites()

   def determineAdditionalCharacteristics( self ):
      self.body.determineAdditionalCharacteristics()

class SolarObjectBase(object):
   def __init__( self, reqs={} ):
      self.reqs = reqs or {}
      self.body_type = None
      self.size = None
      for key,value in reqs.items():
         setattr( self, key, value )

   @property
   def name( self ):
      return "%s" % self.body_type

class Star( SolarObjectBase ):
   _star_types = {
         'O' : 'blue white',
         'B' : 'blue',
         'A' : 'white dwarf',
         'M' : 'red giant', 
         'K' : 'orange dwarf',
         'G' : 'yellow dwarf',
         'F' : 'yellow-white dwarf',
      }
   _zones = [
         { #  SIZE 0 
            "B0" : [ '-' , '_', '_', '_', '_', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O' ],
            "B5" : [ '-' , '_', '_', '_', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "A0" : [ '-' , '-', '_', '_', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "A5" : [ '-' , '-', '_', '_', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "F0" : [ '-' , '-', '-', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O' ],
            "F5" : [ '-' , '-', '-', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O' ],
            "G0" : [ '-' , '-', '-', '-', '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "G5" : [ '-' , '-', '-', '-', '-', '_', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "K0" : [ '-' , '-', '-', '-', '-', '-', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "K5" : [ '-' , '-', '-', '-', '-', '-', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "M0" : [ '-' , '-', '-', '-', '-', '-', '-',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "M5" : [ '-' , '-', '-', '-', '-', '-', '-', '-',
                           'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
         },
         { # SIZE 1
            "B0" : [ '-' , '_', '_', '_', '_', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O' ],
            "B5" : [ '-' , '_', '_', '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O' ],
            "A0" : [ '-' , '_', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O' ],
            "A5" : [ '-' , '_', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "F0" : [ '-' , '_', '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "F5" : [ '-' , '_', '_', '_', 
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "G0" : [ '-' , '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "G5" : [ '-' , '-', '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "K0" : [ '-' , '-', '-', '-', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "K5" : [ '-' , '-', '-', '-', '-', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O' ],
            "M0" : [ '-' , '-', '-', '-', '-', '-',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O' ],
            "M5" : [ '-' , '-', '-', '-', '-', '-', '-',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
         },
         { # SIZE 2
            "B0" : [ '-' , '_', '_', '_', '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O' ],
            "B5" : [ '-' , '_', '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
            "A0" : [ '-' , '_', '_', 
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "A5" : [ '-' , '_', 
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O' ],
            "F0" : [ '-' , '_',
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O' ],
            "F5" : [ '-' , '_', 
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O' ],
            "G0" : [ '-' , '_',
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O' ],
            "G5" : [ '-' , '_',
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O' ],
            "K0" : [ '-' , '_',
                           'I', 'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "K5" : [ '-' , '-', '_',
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "M0" : [ '-' , '-', '-', '-',
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O' ],
            "M5" : [ '-' , '-', '-', '-', '-', '-',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O' ],
         },
         { # SIZE 3
            "B0" : [ '-' , '_', '_', '_', '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O' ],
            "B5" : [ '-' , '_', '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O' ],
            "A0" : [ '-' , 
                           'I', 'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O' ],
            "A5" : [ '-' , 
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O' ],
            "F0" : [ '-' ,
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "F5" : [ '-' ,
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "G0" : [ '-' ,
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "G5" : [ '-' ,
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O' ],
            "K0" : [ '-' ,
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O' ],
            "K5" : [ '-' ,
                           'I', 'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O' ],
            "M0" : [ '-' , '_'
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O' ],
            "M5" : [ '-' , '-', '-', '-',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
         },
         { # SIZE 4
            "B0" : [ '_' , '_', '_', '_', '_', '_', '_',
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O' ],
            "B5" : [ '_' , '_', '_',
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O' ],
            "A0" : [ '_' , 
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O' ],
            "A5" : [ 
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "F0" : [
                           'I', 'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "F5" : [
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "G0" : [
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "G5" : [
                           'I', 'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "K0" : [
                           'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "K5" : [
                           'I', 'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "M0" : [
                           'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "M5" : [
                           'I', 'I', 'I',
                           'H',
                           'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
         },
         { # SIZE 5
            "B0" : [ '_' , '_', '_', '_', '_', '_',
                     'I', 'I', 'I', 'I', 'I', 'I',
                     'H',
                     'O' ],
            "B5" : [ '_' , '_', '_',
                     'I', 'I', 'I', 'I', 'I', 'I',
                     'H',
                     'O', 'O', 'O', 'O' ],
            "A0" : [ 'I', 'I', 'I', 'I', 'I', 'I', 'I',
                     'H',
                     'O', 'O', 'O', 'O', 'O', 'O' ],
            "A5" : [ 'I', 'I', 'I', 'I', 'I', 'I',
                     'H',
                     'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "F0" : [ 'I', 'I', 'I', 'I', 'I',
                     'H',
                     'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "F5" : [ 'I', 'I', 'I', 'I',
                     'H',
                     'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "G0" : [ 'I', 'I', 'I',
                     'H',
                     'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "G5" : [ 'I', 'I',
                     'H',
                     'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "K0" : [ 'I', 'I',
                     'H',
                     'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "K5" : [ 'H',
                     'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "M0" : [ 'H',
                     'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
            "M5" : [ 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O' ],
         },
      ]

   def __init__( self ):
      super( Star, self ).__init__()
      self.body_type = 'star'
      self.star_type = 'G'
      self.star_decimal = 0
      self.orbits = []
      self.binary = None
      self.trinary = None

      self._type()
      self._decimal()
      self._size()
      self.createCompanions()
      self._orbits()

   def _decimal( self ):
      roll = D(1)
      if roll <= 3:
         decimal = 0
      else:
         decimal = 5
      self.star_decimal = 5

   def createCompanions( self ):
      if self.system_nature == 'solo':
         return
      if self.system_nature == 'binary':
         self.binary = BinaryStar( self )
      if self.system_nature == 'trinary':
         self.binary = BinaryStar( self )
         self.trinary = TrinaryStar( self )

   @property
   def name( self ):
      return '%s%d %s %s' % ( self.star_type, self.star_decimal,
                              self._star_types[ self.star_type ], self.body_type )
   @property
   def star_class( self ):
      return '%s%d' % ( self.star_type, self.star_decimal )

class PrimaryStar( Star ):
   def __init__( self, system_nature=None ):
      self.system_nature = system_nature
      super( PrimaryStar, self ).__init__()

   def _type( self ):
      roll = D(2)
      self.star_type_roll = roll
      star_type = roll
      if roll < 2:
         star_type = 'B'
      elif roll < 3:
         star_type = 'A'
      elif roll < 8:
         star_type = 'M'
      elif roll < 9:
         star_type = 'K'
      elif roll < 10:
         star_type = 'G'
      else:
         star_type = 'F'
      self.star_type = star_type

   def _size( self ):
      roll = D(2)
      self.size_roll = roll
      size = roll
      if roll > 4 and roll < 11:
         size = 5
      elif roll == 11:
         size = 6
      elif roll == 12:
         size = 6
      if size == 4 and self.star_class in [ 'K5', 'M0', 'M5' ]: 
         size = 5
      if size == 6 and self.star_class in [ 'B0', 'B5', 'A0', 'A5', 'M0', 'M5', 
                                            'K0', 'K5', 'G0', 'G5', 'F0' ]:
         size = 5
      self.size = size

   def _orbits( self ):
      roll = D(2)
      if self.size == 3:
         roll = roll + 4
      elif self.size <= 2:
         roll = roll + 8
      if self.star_type == 'M':
         roll = roll - 4
      elif self.star_type == 'K':
         roll = roll - 2
      if roll < 0:
         roll = 0
      if self.size <= 2:
         if roll > 14:
            roll = 14
      elif roll > 13:
         roll = 13
      for x in range( roll ):
         self.orbits.append( Orbit( self, x ) )
      for orbit in sorted( self.orbits ):
         size = self.size
         if self.size == 6:
            size = 5
         orbit.zone = self._zones[ size ][ self.star_class ][ orbit.number ] 

class BinaryStar( Star ):
   orbit_roll_modifier = 0

   def __init__( self, primary_star=None ):
      self.primary_star = primary_star
      self.system_nature = 'solo'
      self.orbit = None

      self._orbit()
      super( BinaryStar, self ).__init__()
      if self.orbit >= 12:
         self._system_nature()
         self.createCompanions()

   def _type( self ):
      roll = D(2) + self.primary_star.star_type_roll
      self.star_type_roll = roll
      star_type = roll
      if roll == 2:
         star_type = 'A'
      elif roll < 5:
         star_type = 'F'
      elif roll < 7:
         star_type = 'G'
      elif roll < 9:
         star_type = 'K'
      else:
         star_type = 'M'
      self.star_type = star_type

   def _size( self ):
      roll = D(2) + self.primary_star.size_roll
      self.size_roll = roll
      size = roll
      if roll < 4 and roll < 7:
         size = 4
      elif roll < 9:
         size = 5
      elif roll == 9:
         size = 6
      else:
         size = 6
      if size == 4 and self.star_class in [ 'K5', 'M0', 'M5' ]: 
         size = 5
      if size == 6 and self.star_class in [ 'B0', 'B5', 'A0', 'A5', 'M0', 'M5', 
                                            'K0', 'K5', 'G0', 'G5', 'F0' ]:
         size = 5
      self.size = size

   def _orbits( self ):
      roll = D(2)
      if self.size == 3:
         roll = roll + 4
      elif self.size in [ '1a', '1b', 2 ]:
         roll = roll + 8
      if self.star_type == 'M':
         roll = roll - 4
      elif self.star_type == 'K':
         roll = roll - 2
      if roll > ( self.orbit / 2 ):
         roll = self.orbit
      if roll < 0:
         roll = 0
      if self.size <= 2:
         if roll > 14:
            roll = 14
      elif roll > 13:
         roll = 13
      for x in range( roll ):
         self.orbits.append( Orbit( self, x ) )
      for orbit in sorted( self.orbits ):
         size = self.size
         if self.size == 6:
            size = 5
         orbit.zone = self._zones[ size ][ self.star_class ][ orbit.number ] 

   def _orbit( self ):
      roll = D(2) + self.orbit_roll_modifier
      orbit = roll - 3
      if isinstance(self.primary_star, BinaryStar):
         orbit = orbit - 4
      if orbit < 0:
         orbit = 0
      if orbit >= 4:
         orbit = orbit + D(1)
      self.orbit = orbit

   def _system_nature( self ):
      roll = D(2) 
      if roll < 8:
         roll = 'solo'
      elif roll <= 12:
         roll = 'binary'
      self.system_nature = roll

class TrinaryStar( BinaryStar ):
   orbit_roll_modifier = 4
      
class PlanetoidBase( SolarObjectBase ):
   def __init__( self ):
      super( PlanetoidBase, self ).__init__()
      self.body_type = 'planetoid'
      self.atmoshphere = None
      self.hydrography = None
      self.population = None
      self.orbit = None

   def _atmoshphere( self ):
      """ Determine the atmosphere present """
      pass
   def _hydrography( self ):
      """ Determine the hydrography """
      pass
   def _population( self ):
      """ Determine the population level """
      pass
      
class World( PlanetoidBase ):
   def __init__( self, star, orbit, zone ):
      """ Generate A Random World inside 'zone' """
      super( World, self ).__init__()
      self.body_type = 'world'
      self.num_of_satallites = None
      self.satallites = []
      self.star = star
      self.orbit = orbit
       
      self._size()
      self._atmosphere()
      self._hydrography()
      self._population()

   def _size( self ):
      roll = D(2) - 2;
      orbit = self.orbit
      if orbit.number == 0:
         roll = roll - 5
      elif orbit.number == 1:
         roll = roll - 4
      elif orbit.number == 2:
         roll = roll - 2
      if self.star.star_type == 'M':
         roll = roll - 2
      if roll <= 0:
         size = 'S'
      else:
         size = roll
      self.size = size

   def numberOfSatallites( self ):
      if not self.size == 'S':
         self.num_of_satallites = D(1) - 3
   def generateSatallites( self ):
      for x in range( self.num_of_satallites ):
         size = D(self.size - 1)
         if size == 0:
            size = 'R'
         satallites[x] = Satallite( self, x, size )

   def determineAdditionalCharacteristics( self ):
      if is_main_world:
         self._government()
         self._lawLevel()
         self._starPortType()
         self._techLevel()
         self._tradeClassifications()
         self._navalAndScoutBases()
         self._majorRoutes()
      else:
         self._subordinateGovt()
         self._subordinateLawLevel()
         self._subordinateFacilities()
         self._subordinateTechLevel()
         self._spacePortType()

   @property
   def name( self ):
      return '%s %s %s %s %s' % ( self.size, self.hydrogrophy, self.atmosphere, 
                               self.population, self.body_type )

class Satallite( PlanetoidBase ):
   def __init__( self, world, orbit, size ):
      """ Generate A Random Satallite of 'size' """
      super( Satallite, self ).__init__()
      self.body_type = 'satallite'
      self.world = world
      self.orbit = orbit
      self.size = size

      self._atmosphere()
      self._hydrography()
      self._population()

if __name__ == '__main__':
   var = 'hey'
   lastVar = ''
   while var:
      var = raw_input("Please enter something: ")
      raw = var.strip(' \t\n\r')
      import sys
      sys.argv = sys.argv[:1] + raw.split( ' ' )

      system = SolarSystem()
      lastVar = var


def TestStars():
   for x in range( 100 ):
      s = PrimaryStar('binary')
      print s.name
      print 'binary', s.binary.name
      if s.binary.system_nature == 'binary':
         print 'binary,binary', s.binary.binary.name
