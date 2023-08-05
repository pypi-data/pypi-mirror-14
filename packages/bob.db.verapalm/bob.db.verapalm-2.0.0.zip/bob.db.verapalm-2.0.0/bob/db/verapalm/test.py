#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <Pedro.Tome@idiap.ch>
#
# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the VERA Palm vein database.
"""

import os, sys
import unittest
import bob.db.base
import bob.db.verapalm

class VERAPalmDatabaseTest(unittest.TestCase):
  """Performs various tests on the VERA Palm vein database."""

  def test01_clients(self):
    # test whether the correct number of clients is returned
    db = bob.db.verapalm.Database()

    self.assertEqual(len(db.groups()), 3)
    self.assertEqual(len(db.protocols()), 6)
    self.assertEqual(len(db.protocol_names()), 6)
    self.assertEqual(len(db.purposes()), 3)
   
    self.assertEqual(len(db.clients()), 220) #110 subjects * 2 hands
    #self.assertEqual(len(db.clients(protocol='1vsall')), 220)
    self.assertEqual(len(db.clients(protocol='nom')), 220) #110 subjects * 2 hands
    self.assertEqual(len(db.clients(protocol='spoofingAttack')), 220)
    self.assertEqual(len(db.clients(protocol='nom50')), 100) #50 subjects * 2 hands
    self.assertEqual(len(db.clients(protocol='spoofingAttack50')), 100)
    self.assertEqual(len(db.clients(protocol='nomLeftHand')), 110) #110 subjects * 1 hands
    self.assertEqual(len(db.clients(protocol='nomRightHand')), 110)
    
    self.assertEqual(len(db.client_ids()), 220) #110 subjects * 2 hands
    #self.assertEqual(len(db.client_ids(protocol='1vsall')), 220)
    #self.assertEqual(len(db.client_ids(protocol='1vsall', groups='dev')), 180) #110 subjects * 2 hands - 20 * 2 hands
    #self.assertEqual(len(db.client_ids(protocol='1vsall', groups='eval')), 0) 
    self.assertEqual(len(db.client_ids(protocol='nom')), 220) #110 subjects * 2 hands
    self.assertEqual(len(db.client_ids(protocol='nom', groups='dev')), 60) #30 subjects * 2 hands 
    self.assertEqual(len(db.client_ids(protocol='nom', groups='eval')), 120) #60 subjects * 2 hands 
    self.assertEqual(len(db.client_ids(protocol='spoofingAttack')), 220) #110 subjects * 2 hands
    self.assertEqual(len(db.client_ids(protocol='spoofingAttack', groups='dev')), 60) #30 subjects * 2 hands 
    self.assertEqual(len(db.client_ids(protocol='spoofingAttack', groups='eval')), 120) #60 subjects * 2 hands 
    self.assertEqual(len(db.client_ids(protocol='nom50')), 100) #50 subjects * 2 hands
    self.assertEqual(len(db.client_ids(protocol='nom50', groups='dev')), 90) #45 subjects * 2 hands 
    self.assertEqual(len(db.client_ids(protocol='nom50', groups='eval')), 0) 
    self.assertEqual(len(db.client_ids(protocol='spoofingAttack50')), 100) #50 subjects * 2 hands
    self.assertEqual(len(db.client_ids(protocol='spoofingAttack50', groups='dev')), 90) #45 subjects * 2 hands 
    self.assertEqual(len(db.client_ids(protocol='spoofingAttack50', groups='eval')), 0)
    self.assertEqual(len(db.client_ids(protocol='nomLeftHand')), 110) #110 subjects * 1 hands
    self.assertEqual(len(db.client_ids(protocol='nomLeftHand', groups='dev')), 30) #30 subjects * 1 hands 
    self.assertEqual(len(db.client_ids(protocol='nomLeftHand', groups='eval')), 60) #60 subjects * 1 hands 
    self.assertEqual(len(db.client_ids(protocol='nomRightHand')), 110) #110 subjects * 1 hands
    self.assertEqual(len(db.client_ids(protocol='nomRightHand', groups='dev')), 30) #30 subjects * 1 hands 
    self.assertEqual(len(db.client_ids(protocol='nomRightHand', groups='eval')), 60) #60 subjects * 1 hands 
    
    self.assertEqual(len(db.models()), 720) #1800 + 180 *2 + 90 * 4
    #self.assertEqual(len(db.models(protocol='1vsall')), 1800) #90 subjects * 2 sessions * 2 hands * 5 Acq
    self.assertEqual(len(db.models(protocol='nom')), 180)  #90 subjects * 2 hands 
    self.assertEqual(len(db.models(protocol='spoofingAttack')), 180) 
    self.assertEqual(len(db.models(protocol='nom50')), 90) #45 subjects * 2 hands 
    self.assertEqual(len(db.models(protocol='spoofingAttack50')), 90)
    self.assertEqual(len(db.models(protocol='nomLeftHand')), 90) #90 subjects * 1 hands 
    self.assertEqual(len(db.models(protocol='nomRightHand')), 90)
    
    self.assertEqual(len(db.model_ids()), 720) #1800 + 180 *2 + 90 * 4
    #self.assertEqual(len(db.model_ids(protocol='1vsall')), 1800)
    #self.assertEqual(len(db.model_ids(protocol='1vsall', groups='dev')), 1800) #90 subjects * 2 sessions * 2 hands * 5 Acq
    #self.assertEqual(len(db.model_ids(protocol='1vsall', groups='eval')), 0) 
    self.assertEqual(len(db.model_ids(protocol='nom')), 180) #90 subjects * 2 hands 
    self.assertEqual(len(db.model_ids(protocol='nom', groups='dev')), 60) #30 subjects * 2 hands 
    self.assertEqual(len(db.model_ids(protocol='nom', groups='eval')), 120) #60 subjects * 2 hands 
    self.assertEqual(len(db.model_ids(protocol='spoofingAttack')), 180)
    self.assertEqual(len(db.model_ids(protocol='spoofingAttack', groups='dev')), 60) #30 subjects * 2 hands 
    self.assertEqual(len(db.model_ids(protocol='spoofingAttack', groups='eval')), 120) #60 subjects * 2 hands 
    self.assertEqual(len(db.model_ids(protocol='nom50')), 90) #45 subjects * 2 hands 
    self.assertEqual(len(db.model_ids(protocol='nom50', groups='dev')), 90) #45 subjects * 2 hands 
    self.assertEqual(len(db.model_ids(protocol='nom50', groups='eval')), 0) 
    self.assertEqual(len(db.model_ids(protocol='spoofingAttack50')), 90)
    self.assertEqual(len(db.model_ids(protocol='spoofingAttack50', groups='dev')), 90) #45 subjects * 2 hands 
    self.assertEqual(len(db.model_ids(protocol='spoofingAttack50', groups='eval')), 0) 
    self.assertEqual(len(db.model_ids(protocol='nomLeftHand')), 90) #90 subjects * 1 hands 
    self.assertEqual(len(db.model_ids(protocol='nomLeftHand', groups='dev')), 30) #30 subjects * 1 hands 
    self.assertEqual(len(db.model_ids(protocol='nomLeftHand', groups='eval')), 60) #60 subjects * 1 hands  
    self.assertEqual(len(db.model_ids(protocol='nomRightHand')), 90) 
    self.assertEqual(len(db.model_ids(protocol='nomRightHand', groups='dev')), 30) #30 subjects * 1 hands 
    self.assertEqual(len(db.model_ids(protocol='nomRightHand', groups='eval')), 60) #60 subjects * 1 hands 


  #def test020_objects(self):
    ## tests if the right number of File objects is returned
    #db = bob.db.verapalm.Database()
    
    ## Protocol '1vsall'
    #self.assertEqual(len(db.objects(protocol='1vsall')), 2200) #2200 = 110 subjects * 2 sessions * 2 hands * 5 acq
    
    ## World group
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='world')), 400) #20 subjects * 2 sessions * 2 hands * 5 acq
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='world', purposes='train')), 400) #20 subjects * 2 sessions * 2 hands * 5 acq
    
    ## Dev group
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='dev')), 1800) #(2200 - 400)
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('21_left_1_1_real',))), 1800) #1800 + 1
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', purposes='enroll')), 1800)
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('21_left_1_1_real',), purposes='enroll')), 1)
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('21_left_1_1_real',), purposes='probe')), 1799)
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', purposes='probe', classes='impostor')), 1800)
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('21_left_1_1_real',), purposes='probe', classes='client')), 9) # 5 acq - 1
    #self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('21_left_1_1_real',), purposes='probe', classes='impostor')), 1790) #1800 - 10 acq   
       


  def test021_objects(self):
    # tests if the right number of File objects is returned
    db = bob.db.verapalm.Database()
    
    #####################################################
    # Protocol 'nom'
    self.assertEqual(len(db.objects(protocol='nom')), 2200) #2200 = 110 subjects * 2 sessions * 2 hands * 5 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nom', groups='world')), 400) #20 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nom', groups='world', purposes='train')), 400) #20 subjects * 2 sessions * 2 hands * 5 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nom', groups='dev')), 600) #30 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('21_left_real',))), 482) # 2 enroll sample + probe samples (30 subjects * 2 hands * 2 samples 1asesion + 30 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', purposes='enroll')), 120) #30 subjects * 2 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('21_left_real',), purposes='enroll')), 2) # Samples of enroll per client
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('21_left_real',), purposes='probe')), 480) #(30 subjects * 2 hands * 2 samples 1asesion + 30 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='client')), 8) # Rest of samples that are from the client
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='impostor')), 472) #480 - 8 
    
    # Eval group 
    self.assertEqual(len(db.objects(protocol='nom', groups='eval')), 1200) #60 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('51_left_real',))), 962) # 2 enroll sample + probe samples (60 subjects * 2 hands * 2 samples 1asesion + 60 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', purposes='enroll')), 240) #60 subjects * 2 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('51_left_real',), purposes='enroll')), 2) 
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('51_left_real',), purposes='probe')), 960) #(60 subjects * 2 hands * 2 samples 1asesion + 60 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('51_left_real',), purposes='probe', classes='client')), 8)
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('51_left_real',), purposes='probe', classes='impostor')), 952) #960 - 8 
    
    
    #####################################################
    # Protocol 'spoofingAttack'
    self.assertEqual(len(db.objects(protocol='spoofingAttack')), 2200) #2200 = 110 subjects * 2 sessions * 2 hands * 5 acq

    # World group
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='world')), 400) #20 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='world', purposes='train')), 400) 
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='dev')), 600) #30 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='dev', model_ids=('21_left_real',))), 482) # 2 enroll sample + probe samples (30 subjects * 2 hands * 3 samples 1asesion + 30 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='dev', purposes='enroll')), 120) #30 subjects * 2 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='dev', model_ids=('21_left_real',), purposes='enroll')), 2) # Samples of enroll per client
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='dev', model_ids=('21_left_real',), purposes='probe')), 480) #(30 subjects * 2 hands * 2 samples 1asesion + 30 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='client')), 8) # Rest of samples that are from the client
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='impostor')), 472) #480 - 8 
    
    # Eval group 
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='eval')), 1200) #60 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='eval', model_ids=('51_left_real',))), 962) # 2 enroll sample + probe samples (60 subjects * 2 hands * 2 samples 1asesion + 60 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='eval', purposes='enroll')), 240) #60 subjects * 2 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='eval', model_ids=('51_left_real',), purposes='enroll')), 2) 
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='eval', model_ids=('51_left_real',), purposes='probe')), 960) #(60 subjects * 2 hands * 3 samples 1asesion + 60 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='eval', model_ids=('51_left_real',), purposes='probe', classes='client')), 8)
    self.assertEqual(len(db.objects(protocol='spoofingAttack', groups='eval', model_ids=('51_left_real',), purposes='probe', classes='impostor')), 952) #960 - 8 
    

  def test022_objects(self):
    # tests if the right number of File objects is returned
    db = bob.db.verapalm.Database()

    #####################################################
    # Protocol 'nom50'
    self.assertEqual(len(db.objects(protocol='nom50')), 1000) #1000 = 50 subjects * 2 sessions * 2 hands * 5 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nom50', groups='world')), 100) #5 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nom50', groups='world', purposes='train')), 100) #5 subjects * 2 sessions * 2 hands * 5 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nom50', groups='dev')), 900) #45 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nom50', groups='dev', model_ids=('21_left_real',))), 722) # 2 enroll sample + probe samples (45 subjects * 2 hands * 3 samples 1asesion + 30 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nom50', groups='dev', purposes='enroll')), 180) #45 subjects * 2 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='nom50', groups='dev', model_ids=('21_left_real',), purposes='enroll')), 2) # Samples of enroll per client
    self.assertEqual(len(db.objects(protocol='nom50', groups='dev', model_ids=('21_left_real',), purposes='probe')), 720) #(45 subjects * 2 hands * 3 samples 1asesion + 30 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nom50', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='client')), 8) # Rest of samples that are from the client
    self.assertEqual(len(db.objects(protocol='nom50', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='impostor')), 712) #720 - 8 
    
    # Eval group 
    ## Not exist in this protocol
    

    #####################################################
    # Protocol 'spoofingAttack50'
    self.assertEqual(len(db.objects(protocol='spoofingAttack50')), 1000) #1000 = 50 subjects * 2 sessions * 2 hands * 5 acq

    # World group
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='world')), 100) #5 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='world', purposes='train')), 100) #5 subjects * 2 sessions * 2 hands * 5 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='dev')), 900) #45 subjects * 2 sessions * 2 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='dev', model_ids=('21_left_real',))), 722) # 2 enroll sample + probe samples (45 subjects * 2 hands * 3 samples 1asesion + 30 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='dev', purposes='enroll')), 180) #45 subjects * 2 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='dev', model_ids=('21_left_real',), purposes='enroll')), 2) # Samples of enroll per client
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='dev', model_ids=('21_left_real',), purposes='probe')), 720) #(45 subjects * 2 hands * 3 samples 1asesion + 30 * 2 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='client')), 8) # Rest of samples that are from the client
    self.assertEqual(len(db.objects(protocol='spoofingAttack50', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='impostor')), 712) #720 - 8 
    
    # Eval group 
    ## Not exist in this protocol



  def test023_objects(self):
    # tests if the right number of File objects is returned
    db = bob.db.verapalm.Database()

    #####################################################
    # Protocol 'nomLeftHand'
    self.assertEqual(len(db.objects(protocol='nomLeftHand')), 1100) #1100 = 110 subjects * 2 sessions * 1 hand * 5 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='world')), 200) #20 subjects * 2 sessions * 1 hand * 5 acq
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='world', purposes='train')), 200) #20 subjects * 2 sessions * 1 hand * 5 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='dev')), 300) #30 subjects * 2 sessions * 1 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='dev', model_ids=('21_left_real',))), 242) # 2 enroll sample + probe samples (30 subjects * 1 hands * 3 samples 1asesion + 30 * 1 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='dev', purposes='enroll')), 60) #30 subjects * 1 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='dev', model_ids=('21_left_real',), purposes='enroll')), 2) # Samples of enroll per client
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='dev', model_ids=('21_left_real',), purposes='probe')), 240) #(30 subjects * 1 hands * 3 samples 1asesion + 30 * 1 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='client')), 8) # Rest of samples that are from the client
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='dev', model_ids=('21_left_real',), purposes='probe', classes='impostor')), 232) #240 - 8 
    
    # Eval group 
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='eval')), 600) #60 subjects * 2 sessions * 1 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='eval', model_ids=('51_left_real',))), 482) # 2 enroll sample + probe samples (60 subjects * 1 hands * 3 samples 1asesion + 60 * 1 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='eval', purposes='enroll')), 120) #60 subjects * 1 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='eval', model_ids=('51_left_real',), purposes='enroll')), 2) 
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='eval', model_ids=('51_left_real',), purposes='probe')), 480) #(60 subjects * 1 hands * 3 samples 1asesion + 60 * 1 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='eval', model_ids=('51_left_real',), purposes='probe', classes='client')), 8)
    self.assertEqual(len(db.objects(protocol='nomLeftHand', groups='eval', model_ids=('51_left_real',), purposes='probe', classes='impostor')), 472) #480 - 8 


    #####################################################
    # Protocol 'nomRightHand'
    self.assertEqual(len(db.objects(protocol='nomRightHand')), 1100) #1100 = 110 subjects * 2 sessions * 1 hand * 5 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='world')), 200) #20 subjects * 2 sessions * 1 hand * 5 acq
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='world', purposes='train')), 200) #20 subjects * 2 sessions * 1 hand * 5 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='dev')), 300) #30 subjects * 2 sessions * 1 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='dev', model_ids=('21_right_real',))), 242) # 2 enroll sample + probe samples (30 subjects * 1 hands * 3 samples 1asesion + 30 * 1 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='dev', purposes='enroll')), 60) #30 subjects * 1 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='dev', model_ids=('21_right_real',), purposes='enroll')), 2) # Samples of enroll per client
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='dev', model_ids=('21_right_real',), purposes='probe')), 240) #(30 subjects * 1 hands * 3 samples 1asesion + 30 * 1 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='dev', model_ids=('21_right_real',), purposes='probe', classes='client')), 8) # Rest of samples that are from the client
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='dev', model_ids=('21_right_real',), purposes='probe', classes='impostor')), 232) #240 - 8 
    
    # Eval group 
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='eval')), 600) #60 subjects * 2 sessions * 1 hands * 5 acq
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='eval', model_ids=('51_right_real',))), 482) # 2 enroll sample + probe samples (60 subjects * 1 hands * 3 samples 1asesion + 60 * 1 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='eval', purposes='enroll')), 120) #60 subjects * 1 hands * 2 acq of 1a session
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='eval', model_ids=('51_right_real',), purposes='enroll')), 2) 
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='eval', model_ids=('51_right_real',), purposes='probe')), 480) #(60 subjects * 1 hands * 3 samples 1asesion + 60 * 1 hands * 5 samples 2asesion)
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='eval', model_ids=('51_right_real',), purposes='probe', classes='client')), 8)
    self.assertEqual(len(db.objects(protocol='nomRightHand', groups='eval', model_ids=('51_right_real',), purposes='probe', classes='impostor')), 472) #480 - 8 

    
  def test03_driver_api(self):

    from bob.db.base.script.dbmanage import main
    self.assertEqual(main('verapalm dumplist --self-test'.split()), 0)
    self.assertEqual(main('verapalm dumplist --protocol=nom --class=client --group=dev --purpose=enroll --model=21_left_real --self-test'.split()), 0)
    self.assertEqual(main('verapalm checkfiles --self-test'.split()), 0)
    self.assertEqual(main('verapalm reverse Palmvein/raw/021-M/01/021_L_1_1 --self-test'.split()), 0)
    self.assertEqual(main('verapalm path 37 --self-test'.split()), 0)
    
