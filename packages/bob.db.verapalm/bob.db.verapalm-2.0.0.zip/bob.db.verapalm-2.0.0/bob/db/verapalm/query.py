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

"""This module provides the Dataset interface allowing the user to query the
VERA Palm vein database in the most obvious ways.
"""

import os
import six
from bob.db.base import utils
from .models import *
from .driver import Interface

import bob.db.verification.utils

SQLITE_FILE = Interface().files()[0]

class Database(bob.db.verification.utils.SQLiteDatabase):
  """The dataset class opens and maintains a connection opened to the Database.

  It provides many different ways to probe for the characteristics of the data
  and for the data itself inside the database.
  """

  def __init__(self, original_directory = None, original_extension = None):
    # call base class constructors
    bob.db.verification.utils.SQLiteDatabase.__init__(self, SQLITE_FILE, File,
      original_directory=original_directory, 
      original_extension=original_extension
    )

    
  def groups(self, protocol=None):
    """Returns the names of all registered groups"""
    if protocol == '1vsall': return ('world', 'dev')
    else: return ('world', 'dev', 'eval')

  def clients(self, protocol=None, groups=None):
    """Returns a set of clients for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the VERAPalm protocols ('1vsall', 'nom','nom50','nomLeftHand','nomRightHand','spoofingAttack', 'spoofingAttack50').

    groups
      The clients belong to 'world', 'dev' and 'eval'

    Returns: A list containing all the clients which have the given properties.
    """

    protocols = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())    
    
    retval = []
    # List of the clients
    if 'world' in groups:
      q = self.query(Client).join((File, Client.files)).join((Protocol, File.protocols_train)).filter(Protocol.name.in_(protocols))
      q = q.order_by(Client.id)
      retval += list(q)

    if 'dev' in groups or 'eval' in groups:
      q = self.query(Client).join((Model, Client.models)).join((Protocol, Model.protocol)).filter(Protocol.name.in_(protocols))
      q = q.filter(Model.sgroup.in_(groups))
      q = q.order_by(Client.id)
      retval += list(q)
    
    if len(protocols) == len(self.protocols()):
      retval = list(self.query(Client))

    return retval

  def client_ids(self, protocol=None, groups=None):
    """Returns a set of client ids for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the VERAPalm protocols ('1vsall', 'nom','nom50','nomLeftHand','nomRightHand','spoofingAttack', 'spoofingAttack50').

    groups
      The clients belong to 'world', 'dev' and 'eval'

    Returns: A list containing all the clients which have the given properties.
    """
    
    return [client.id for client in self.clients(protocol, groups)]

  def models(self, protocol=None, groups=None):
    """Returns a set of models for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the VERAPalm protocols ('1vsall', 'nom','nom50','nomLeftHand','nomRightHand','spoofingAttack', 'spoofingAttack50').

    groups
      Returns models from the 'world', 'dev' or 'eval' .
      
    Returns: A list containing all the models which have the given properties.
    """

    protocols = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())

    retval = []

    if 'dev' or 'eval' in groups:
      # List of the clients
      q = self.query(Model).join((Protocol, Model.protocol)).filter(Protocol.name.in_(protocols))
      q = q.filter(Model.sgroup.in_(groups)).order_by(Model.name)
      retval += list(q)

    return retval

  def model_ids(self, protocol=None, groups=None):
    """Returns a set of models ids for the specific query by the user.

    Keyword Parameters:

    protocol
      Two possible protocols: '1vsall', 'nom','nom50','nomLeftHand','nomRightHand','spoofingAttack', 'spoofingAttack50'

    groups
      The groups to which the subjects attached to the models belong ('world', 'dev', 'eval')

    Returns: A list containing all the models ids which have the given properties.
    """

    return [model.name for model in self.models(protocol, groups)]

  def has_client_id(self, id):
    """Returns True if we have a client with a certain integer identifier"""

    return self.query(Client).filter(Client.id==id).count() != 0

  def client(self, id):
    """Returns the client object in the database given a certain id. Raises
    an error if that does not exist."""

    return self.query(Client).filter(Client.id==id).one()

  def get_client_id_from_model_id(self, model_id):
    """Returns the client_id attached to the given model_id

    Keyword Parameters:

    model_id
      The model_id to consider

    Returns: The client_id attached to the given model_id
    """
    
    return self.query(Model).filter(Model.name==model_id).first().client_id

  def objects(self, protocol=None, purposes=None, model_ids=None, groups=None,
      classes=None, hand_ids=None, session_ids=None):
    """Returns a set of Files for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the VERAPalm protocols ('1vsall', 'nom','nom50','nomLeftHand','nomRightHand','spoofingAttack', 'spoofingAttack50').

    purposes
      The purposes required to be retrieved ('enroll', 'probe', 'train') or a tuple
      with several of them. If 'None' is given (this is the default), it is
      considered the same as a tuple with all possible values. This field is
      ignored for the data from the "world" group.

    model_ids
      Only retrieves the files for the provided list of model ids.
      If 'None' is given (this is the default), no filter over
      the model_ids is performed.

    groups
      One of the groups ('world', 'dev', 'eval') or a tuple with several of them.
      If 'None' is given (this is the default), it is considered the same as a
      tuple with all possible values.

    classes
      The classes (types of accesses) to be retrieved ('client', 'impostor')
      or a tuple with several of them. If 'None' is given (this is the
      default), it is considered the same as a tuple with all possible values.

    hand_ids
      Only retrieves the files for the provided list of hand ids.
      If 'None' is given (this is the default), no filter over
      the hand_ids is performed.

    session_ids
      Only retrieves the files for the provided list of session ids.
      If 'None' is given (this is the default), no filter over
      the session_ids is performed.

    sample_ids
      Only retrieves the files for the provided list of sample ids.
      If 'None' is given (this is the default), no filter over
      the sample_ids is performed.

    Returns: A list of files which have the given properties.
    """

    protocols = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    purposes = self.check_parameters_for_validity(purposes, "purpose", self.purposes())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())
    classes = self.check_parameters_for_validity(classes, "class", ('client', 'impostor'))

    from six import string_types
    if model_ids is None:
      model_ids = ()
    elif isinstance(model_ids, string_types):
      model_ids = (model_ids,)
    import collections
    if hand_ids is None:
      hand_ids = ()
    elif not isinstance(hand_ids, collections.Iterable):
      hand_ids = (hand_ids,)
    if session_ids is None:
      session_ids = ()
    elif not isinstance(session_ids, collections.Iterable):
      session_ids = (session_ids,)

    # Now query the database
    retval = []
    if 'world' in groups:
      q = self.query(File).join((Protocol, File.protocols_train)).\
            filter(Protocol.name.in_(protocols))
      if hand_ids:  q = q.filter(File.hand_id.in_(hand_ids))
      if session_ids: q = q.filter(File.session_id.in_(session_ids))
      q = q.order_by(File.client_id, File.hand_id, File.session_id)
      retval += list(q)

    
    if 'dev' in groups or 'eval' in groups:
      sgroups = []
      if 'dev' in groups: sgroups.append('dev')
      if 'eval' in groups: sgroups.append('eval')
      if 'enroll' in purposes:
        q = self.query(File).join(Client).join((Model, File.models_enroll)).join((Protocol, Model.protocol)).\
              filter(and_(Protocol.name.in_(protocols), Model.sgroup.in_(sgroups)))
        if model_ids:
          q = q.filter(Model.name.in_(model_ids))
        if hand_ids:  q = q.filter(File.hand_id.in_(hand_ids))
        if session_ids: q = q.filter(File.session_id.in_(session_ids))
        q = q.order_by(File.client_id, File.hand_id, File.session_id)
        retval += list(q)
        
      if 'probe' in purposes:
        if 'client' in classes:
          q = self.query(File).join(Client).join((Model, File.models_probe)).join((Protocol, Model.protocol)).\
                filter(and_(Protocol.name.in_(protocols), Model.sgroup.in_(sgroups), File.client_id == Model.client_id))
          if model_ids:
            q = q.filter(Model.name.in_(model_ids))
          if hand_ids:  q = q.filter(File.hand_id.in_(hand_ids))
          if session_ids: q = q.filter(File.session_id.in_(session_ids))
          q = q.order_by(File.client_id, File.hand_id, File.session_id)
          retval += list(q)
          
        if 'impostor' in classes:
          q = self.query(File).join(Client).join((Model, File.models_probe)).join((Protocol, Model.protocol)).\
                filter(and_(Protocol.name.in_(protocols), Model.sgroup.in_(sgroups), File.client_id != Model.client_id))
          if len(model_ids) != 0:
            q = q.filter(Model.name.in_(model_ids))
          if hand_ids:  q = q.filter(File.hand_id.in_(hand_ids))
          if session_ids: q = q.filter(File.session_id.in_(session_ids))
          q = q.order_by(File.client_id, File.hand_id, File.session_id)
          retval += list(q)
  
    return list(set(retval)) # To remove duplicates
    
  def protocol_names(self):
    """Returns all registered protocol names"""

    l = self.protocols()
    retval = [str(k.name) for k in l]
    return retval

  def protocols(self):
    """Returns all registered protocols"""

    return list(self.query(Protocol))

  def has_protocol(self, name):
    """Tells if a certain protocol is available"""

    return self.query(Protocol).filter(Protocol.name==name).count() != 0

  def protocol(self, name):
    """Returns the protocol object in the database given a certain name. Raises
    an error if that does not exist."""

    return self.query(Protocol).filter(Protocol.name==name).one()

  def purposes(self):
    return ('train', 'enroll', 'probe')
