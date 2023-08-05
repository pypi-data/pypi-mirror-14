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

"""Table models and functionality for the VERA Palm database.
"""

import os, numpy
import bob.db.base.utils
from sqlalchemy import Table, Column, Integer, String, ForeignKey, or_, and_, not_
from bob.db.base.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

import bob.db.verification.utils

Base = declarative_base()

protocol_model_association = Table('protocol_model_association', Base.metadata,
  Column('protocol_id', Integer, ForeignKey('protocol.id')),
  Column('model_id', Integer, ForeignKey('model.id')))

protocol_trainfiles_association = Table('protocol_trainfiles_association', Base.metadata,
  Column('protocol_id', Integer, ForeignKey('protocol.id')),
  Column('file_id', Integer, ForeignKey('file.id')))

model_probefile_association = Table('model_probefile_association', Base.metadata,
  Column('model_id', Integer, ForeignKey('model.id')),
  Column('file_id', Integer, ForeignKey('file.id')))
  
model_enrollmentfile_association = Table('model_enrollmentfile_association', Base.metadata,
  Column('model_id', Integer, ForeignKey('model.id')),
  Column('file_id', Integer, ForeignKey('file.id')))



class Client(Base):
  """Database clients, marked by an integer identifier and the group they belong to"""

  __tablename__ = 'client'

  # Key identifier for the client
  id = Column(String(20), primary_key=True)
  subclient_id = Column(Integer)

  def __init__(self, id, subclient_id):
    self.id = id
    self.subclient_id = subclient_id

  def __repr__(self):
    return "Client(%s)" % (self.id,) 

class Model(Base):
  """Database models, marked by an integer identifier and the group they belong to"""

  __tablename__ = 'model'

  # Key identifier for the client
  id = Column(Integer, primary_key=True)
  # Name of the protocol associated with this object
  name = Column(String(20))
  # Group associated with this protocol purpose object
  group_choices = ('dev', 'eval')
  sgroup = Column(Enum(*group_choices))
  # Key identifier of the client associated with this model
  client_id = Column(String(20), ForeignKey('client.id')) # for SQL
  # For Python: A direct link to the enrollment File objects associated with this Model
  enrollment_files = relationship("File", secondary=model_enrollmentfile_association, backref=backref("models_enroll", order_by=id))
  # For Python: A direct link to the probe File objects associated with this Model
  probe_files = relationship("File", secondary=model_probefile_association, backref=backref("models_probe", order_by=id))

  # For Python: A direct link to the client object that this model belongs to
  client = relationship("Client", backref=backref("models", order_by=id))

  def __init__(self, name, client_id, sgroup):
    self.name = name
    self.client_id = client_id
    self.sgroup = sgroup

  def __repr__(self):
    return "Model(%s, %s)" % (self.name, self.sgroup) 

class File(Base, bob.db.verification.utils.File):
  """Generic file container"""

  __tablename__ = 'file'

  # Key identifier for the file
  id = Column(Integer, primary_key=True)
  # Key identifier of the client associated with this file
  client_id = Column(String(20), ForeignKey('client.id')) # for SQL
  # Unique path to this file inside the database
  path = Column(String(100), unique=True)
  # Identifier of the palm id associated with this file
  hand_id = Column(String(10)) 
  # Identifier of the session (the wavelenght in VERA palm vein database)
  session_id = Column(Integer)
  # Identifier of the sample
  sample_id = Column(Integer)
  # Identifier wheter is is a real or attack sample
  type_choices = ('real', 'attack')
  stype = Column(Enum(*type_choices))

  # For Python: A direct link to the client object that this file belongs to
  client = relationship("Client", backref=backref("files", order_by=id))

  def __init__(self, client_id, path, hand_id,  session_id, sample_id, stype):
    # call base class constructor
    bob.db.verification.utils.File.__init__(self, client_id = client_id, path = path)
    self.hand_id = hand_id
    self.session_id = session_id
    self.sample_id = sample_id
    self.stype = stype
  
class Protocol(Base):
  """VERA Palm protocols"""
  
  __tablename__ = 'protocol'
  
  # Unique identifier for this protocol object
  id = Column(Integer, primary_key=True)
  # Name of the protocol associated with this object
  name = Column(String(20), unique=True)
  
  # For Python: A direct link to the DevModel objects associated with this Protcol
  train_files = relationship("File", secondary=protocol_trainfiles_association, backref=backref("protocols_train", order_by=id))
  models = relationship("Model", secondary=protocol_model_association, backref=backref("protocol", uselist=False, order_by=id))
  
  def __init__(self, name):
    self.name = name
  
  def __repr__(self):
    return "Protocol('%s')" % (self.name,)
