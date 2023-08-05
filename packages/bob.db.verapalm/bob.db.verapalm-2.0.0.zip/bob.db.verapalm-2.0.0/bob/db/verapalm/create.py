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

"""This script creates the VERA Palm vein database in a single pass.
"""

import os

from .models import *

def nodot(item):
  """Can be used to ignore hidden files, starting with the . character."""
  return item[0] != '.'

def add_files(session, imagedir, verbose):
  """Add files (and clients) to the VERA Palm database."""

  TYPEDIR_LIST = ['Palmvein/raw', 'SpoofingPalmvein/raw']
  
  def add_file(session, typedir, subdir, sessiondir, filename, client_dict, verbose):
    """Parse a single filename and add it to the list.
       Also add a client entry if not already in the database."""

    v = os.path.splitext(os.path.basename(filename))[0].split('_')
    
    subclient_id = int(v[0])
    if v[1] == 'L':
      hand_id = 'left'
    else:
      hand_id = 'right'
    client_id = "%d_%s" % (subclient_id, hand_id)
    if not (client_id in client_dict):
      c = Client(client_id, subclient_id)
      session.add(c)
      session.flush()
      session.refresh(c)
      client_dict[client_id] = True

    session_id = int(v[2])
    sample_id = int(v[3])
    
    base_path = os.path.join(typedir, subdir, sessiondir, os.path.basename(filename).split('.')[0])
    if verbose>1: print("  Adding file '%s'..." %(base_path, ))
    if typedir == TYPEDIR_LIST[0]: type_file = 'real'
    else: type_file = 'attack'    
    
    cfile = File(client_id, base_path, hand_id, session_id, sample_id, type_file)
    session.add(cfile)
    session.flush()
    session.refresh(cfile)
    
    return cfile
  
  if verbose: print("Adding files...")
  client_dict = {}
  file_list = []
  for typedir in TYPEDIR_LIST:
    if not os.path.isdir(os.path.join(imagedir,typedir)): raise RuntimeError("Cannot find directory '%s'" % os.path.join(imagedir,typedir))
    subdir_list = [l for l in list(filter(nodot, os.listdir(os.path.join(imagedir,typedir)))) if os.path.isdir(os.path.join(imagedir,typedir,l))]
    for subdir in subdir_list:
      sessiondir_list = [l for l in list(filter(nodot, os.listdir(os.path.join(imagedir,typedir,subdir)))) if os.path.isdir(os.path.join(imagedir,typedir,subdir))]
      for sessiondir in sessiondir_list:
        files_list = list(filter(nodot, os.listdir(os.path.join(imagedir, typedir, subdir, sessiondir))))
        for filename in files_list:
          filename_, extension = os.path.splitext(filename)
          if extension == '.png':
            file_list.append(add_file(session, typedir, subdir, sessiondir, os.path.join(imagedir, filename), client_dict, verbose))
  
  return file_list            

def add_protocols(session, file_list, verbose):
  """Adds protocols"""
  # 2. ADDITIONS TO THE SQL DATABASE
  
  protocol_list_spoof =  ['spoofingAttack', 'spoofingAttack50']
  protocol_list = ['nom', 'nom50', 'nomLeftHand','nomRightHand'] + protocol_list_spoof
  for proto in protocol_list:
    p = Protocol(proto)
    # Add protocol
    if verbose: print("Adding protocol %s..." % (proto))
    session.add(p)
    session.flush()
    session.refresh(p)
                 
    """
    if proto == '1vsall':
      # Helper function
      def isWorldFile(f_file):
        return f_file.client.subclient_id <= 20

      model_dict = {}
      for f_file in file_list:
        if f_file.stype == 'real':      
          if not isWorldFile(f_file):
            #model_id = "%s_%d" % (f_file.client_id, f_file.sample_id)
            model_id = "%s_%d_%d_%s" % (f_file.client_id, f_file.session_id, f_file.sample_id, f_file.stype)
            
            if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
            if not model_id in model_dict:
              model = Model(model_id, f_file.client_id, 'dev')
              p.models.append(model)
              session.add(model)
              session.flush()
              session.refresh(model)
              # Append probe files
              for f_pfile in file_list:
                if f_pfile.stype == 'real':      
                  if f_pfile.id != f_file.id and not isWorldFile(f_pfile):
                    model.probe_files.append(f_pfile)
                    if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
              model_dict[model_id] = model
            # Append enrollment file
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enrol'))
            session.flush()
            
          else:
            p.train_files.append(f_file)
            if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))
    """
    if proto == 'nom':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 21 and f_file.client.subclient_id <= 50 and f_file.session_id == 1 and f_file.sample_id <= 2 and f_file.stype == 'real')
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 21 and f_file.client.subclient_id <= 50 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.stype == 'real')
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 51 and f_file.session_id == 1  and f_file.sample_id <= 2 and f_file.stype == 'real')
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 51 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.stype == 'real')

      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%s" % (f_file.client_id, f_file.stype)

        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enrol'))
             
        elif f_file.client.subclient_id <= 20 and f_file.stype == 'real':
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))   

    if proto == 'spoofingAttack':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 21 and f_file.client.subclient_id <= 50 and f_file.session_id == 1 and f_file.sample_id <= 2 and f_file.stype == 'real')
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 21 and f_file.client.subclient_id <= 50 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.stype == 'attack')
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 51 and f_file.session_id == 1  and f_file.sample_id <= 2 and f_file.stype == 'real')
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 51 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.stype == 'attack')
        
      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%s" % (f_file.client_id, f_file.stype)
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))
             
        elif f_file.client.subclient_id <= 20 and f_file.stype == 'real':
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))   
      

    if proto == 'nom50':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 6 and f_file.client.subclient_id <= 50 and f_file.session_id == 1 and f_file.sample_id <= 2 and f_file.stype == 'real')
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 6 and f_file.client.subclient_id <= 50 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.stype == 'real')
              
      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%s" % (f_file.client_id, f_file.stype)
        if isDevEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))
             
        elif f_file.client.subclient_id <= 5 and f_file.stype == 'real':
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))         


    if proto == 'spoofingAttack50':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 6 and f_file.client.subclient_id <= 50 and f_file.session_id == 1 and f_file.sample_id <= 2 and f_file.stype == 'real')
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 6 and f_file.client.subclient_id <= 50 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.stype == 'attack')
        
      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%s" % (f_file.client_id, f_file.stype)
        if isDevEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))
             
        elif f_file.client.subclient_id <= 5 and f_file.stype == 'real':
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))    
    

    if proto == 'nom10':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 1 and f_file.client.subclient_id <= 10 and f_file.session_id == 1 and f_file.sample_id <= 2 and f_file.stype == 'real')
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 1 and f_file.client.subclient_id <= 10 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.stype == 'real')
              
      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%s" % (f_file.client_id, f_file.stype)
        if isDevEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))
        
    if proto == 'spoofingAttack10':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 1 and f_file.client.subclient_id <= 10 and f_file.session_id == 1 and f_file.sample_id <= 2 and f_file.stype == 'real')
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 1 and f_file.client.subclient_id <= 10 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.stype == 'attack')
        
      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%s" % (f_file.client_id, f_file.stype)
        if isDevEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))
        


    if proto == 'nomLeftHand':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 21 and f_file.client.subclient_id <= 50 and f_file.session_id == 1 and f_file.sample_id <= 2 and f_file.hand_id == 'left' and f_file.stype == 'real')
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 21 and f_file.client.subclient_id <= 50 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.hand_id == 'left' and f_file.stype == 'real')
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 51 and f_file.session_id == 1  and f_file.sample_id <= 2 and f_file.hand_id == 'left' and f_file.stype == 'real')
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 51 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.hand_id == 'left' and f_file.stype == 'real')

      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%s" % (f_file.client_id, f_file.stype)
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))
             
        elif f_file.client.subclient_id <= 20 and f_file.hand_id == 'left' and f_file.stype == 'real':
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))   
        
    if proto == 'nomRightHand':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 21 and f_file.client.subclient_id <= 50 and f_file.session_id == 1 and f_file.sample_id <= 2 and f_file.hand_id == 'right' and f_file.stype == 'real')
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 21 and f_file.client.subclient_id <= 50 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.hand_id == 'right' and f_file.stype == 'real')
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 51 and f_file.session_id == 1  and f_file.sample_id <= 2 and f_file.hand_id == 'right' and f_file.stype == 'real')
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 51 and (f_file.session_id == 1 and f_file.sample_id > 2 or f_file.session_id == 2) and f_file.hand_id == 'right' and f_file.stype == 'real')
        
      model_dict = {}
      for f_file in file_list:
        model_id = "%s_%s" % (f_file.client_id, f_file.stype)
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enroll'))
             
        elif f_file.client.subclient_id <= 20 and f_file.hand_id == 'right' and f_file.stype == 'real':
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))   
    

def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  Base.metadata.create_all(engine)

# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  file_list = add_files(s, args.imagedir, args.verbose)
  add_protocols(s, file_list, args.verbose)
  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help="If set, I'll first erase the current database")
  parser.add_argument('-v', '--verbose', action='count', help='Do SQL operations in a verbose way')
  parser.add_argument('-D', '--imagedir', metavar='DIR', default='/idiap/project/vera', help="Change the relative path to the directory containing the images of the VERA Palm database (defaults to %(default)s)")

  parser.set_defaults(func=create) #action
