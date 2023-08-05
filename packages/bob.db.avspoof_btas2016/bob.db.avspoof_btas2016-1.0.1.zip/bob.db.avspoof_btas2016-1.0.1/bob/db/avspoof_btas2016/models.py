#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Wed 19 Aug 13:43:50 2015

"""Table models and functionality for the AVSpoof DB.
"""

import os
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from bob.db.base.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base
import bob

Base = declarative_base()


class Client(Base):
    """Database clients, marked by an integer identifier and the set they belong
    to"""

    __tablename__ = 'client'

    gender_choices = ('male', 'female', 'unknown')
    """Male or female speech"""

    set_choices = ('train', 'devel', 'test')
    """Possible groups to which clients may belong to"""

    id = Column(Integer, primary_key=True)
    """Key identifier for clients"""

    gender = Column(Enum(*gender_choices))
    """The gender of the subject"""

    set = Column(Enum(*set_choices))
    """Set to which this client belongs to"""

    def __init__(self, id, gender, set):
        self.id = id
        self.gender = gender
        self.set = set

    def __repr__(self):
        return "Client('%d', '%s', '%s')" % (self.id, self.gender, self.set)


class File(Base):
    """Generic file container"""

    __tablename__ = 'file'

    gender_choices = ('male', 'female', 'unknown')
    """Male or female speech"""

    device_choices = ('laptop', 'phone1', 'phone2', 'unknown')
    """List of devices used to record audio samples"""

    session_choices = ('sess1', 'sess2', 'sess3', 'sess4', 'unknown')
    """List of sessions during which audio samples were recorded"""

    speech_choices = ('pass', 'read', 'free', 'unknown')
    """Types of speech subjects were asked to say,
    pass - password, read - short text, free - 2-5 mints free speech"""

    id = Column(Integer, primary_key=True)
    """Key identifier for files"""

    client_id = Column(Integer, ForeignKey('client.id'))  # for SQL
    """The client identifier to which this file is bound to"""

    gender = Column(Enum(*gender_choices))
    """The gender of the subject"""

    path = Column(String(200), unique=True)
    """The (unique) path to this file inside the database"""

    device = Column(Enum(*device_choices))
    """The device using which the data for this file was taken"""

    session = Column(Enum(*session_choices))
    """The session during which the data for this file was taken"""

    speech = Column(Enum(*speech_choices))
    """The speech type of the data for this file was taken"""

    # for Python
    client = relationship(Client, backref=backref('files', order_by=id))
    """A direct link to the client object that this file belongs to"""

    def __init__(self, client, gender, path, device, session, speech):
        self.client = client
        self.path = path
        self.gender = gender
        self.device = device
        self.session = session
        self.speech = speech

    def __repr__(self):
        return "File('%s')" % self.path

    def make_path(self, directory=None, extension=None):
        """Wraps the current path so that a complete path is formed

        Keyword parameters:

        directory
            An optional directory name that will be prefixed to the returned result.

        extension
            An optional extension that will be suffixed to the returned filename. The
            extension normally includes the leading ``.`` character as in ``.wav`` or
            ``.hdf5``.

        Returns a string containing the newly generated file path.
        """

        if not directory: directory = ''
        if not extension: extension = ''

        return str(os.path.join(directory, self.path + extension))

    def audiofile(self, directory=None):
        """Returns the path to the database audio file for this object

        Keyword parameters:

        directory
            An optional directory name that will be prefixed to the returned result.

        Returns a string containing the video file path.
        """

        return self.make_path(directory, '.wav')

    def is_real(self):
        """Returns True if this file belongs to a real access, False otherwise"""

        return bool(self.realaccess)

    def get_realaccess(self):
        """Returns the real-access object equivalent to this file or raise"""
        if len(self.realaccess) == 0:
            raise RuntimeError("%s is not a real-access" % self)
        return self.realaccess[0]

    def get_attack(self):
        """Returns the attack object equivalent to this file or raise"""
        if len(self.attack) == 0:
            raise RuntimeError("%s is not an attack" % self)
        return self.attack[0]

    def load(self, directory=None, extension='.hdf5'):
        """Loads the data at the specified location and using the given extension.

        Keyword parameters:

        data
            The data blob to be saved (normally a :py:class:`numpy.ndarray`).

        directory
            [optional] If not empty or None, this directory is prefixed to the final
            file destination

        extension
            [optional] The extension of the filename - this will control the type of
            output and the codec for saving the input blob.
        """
        return bob.io.base.load(self.make_path(directory, extension))

    def save(self, data, directory=None, extension='.hdf5'):
        """Saves the input data at the specified location and using the given
        extension.

        Keyword parameters:

        data
            The data blob to be saved (normally a :py:class:`numpy.ndarray`).

        directory
            [optional] If not empty or None, this directory is prefixed to the final
            file destination

        extension
            [optional] The extension of the filename - this will control the type of
            output and the codec for saving the input blob.
        """

        path = self.make_path(directory, extension)
        bob.io.base.create_directories_safe(os.path.dirname(path))
        bob.io.base.save(data, path)


# Intermediate mapping from RealAccess's to Protocol's
realaccesses_protocols = Table('realaccesses_protocols', Base.metadata,
                               Column('realaccess_id', Integer, ForeignKey('realaccess.id')),
                               Column('protocol_id', Integer, ForeignKey('protocol.id')),
                               )

# Intermediate mapping from Attack's to Protocol's
attacks_protocols = Table('attacks_protocols', Base.metadata,
                          Column('attack_id', Integer, ForeignKey('attack.id')),
                          Column('protocol_id', Integer, ForeignKey('protocol.id')),
                          )


# create column type of the protocol - verefication of spoofing
# so when query, you dont get all protocols
# another cross-reference table or two linking file with protocol id and the purpose (enrollment or probing)
#

class Protocol(Base):
    """AVSpoof general protocol"""

    __tablename__ = 'protocol'

    #    purpose_choices = ('antispoofing', 'verification')
    #    """What kind of protocol is it? It's true purpose"""

    id = Column(Integer, primary_key=True)
    """Unique identifier for the protocol (integer)"""

    name = Column(String(20), unique=True)
    """Protocol name"""

    #    purpose = Column(Enum(*purpose_choices))
    #    """It can one of two purposes"""


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Protocol('%s')" % self.name


class RealAccess(Base):
    """Defines Real-Accesses (licit attempts to authenticate)"""

    __tablename__ = 'realaccess'

    id = Column(Integer, primary_key=True)
    """Unique identifier for this real-access object"""

    file_id = Column(Integer, ForeignKey('file.id'))  # for SQL
    """The file identifier the current real-access is bound to"""

    # for Python
    file = relationship(File, backref=backref('realaccess', order_by=id))
    """A direct link to the :py:class:`.File` object this real-access belongs to"""

    protocols = relationship("Protocol", secondary=realaccesses_protocols,
                             backref='realaccess')
    """A direct link to the protocols this file is linked to"""

    def __init__(self, file):
        self.file = file

    def __repr__(self):
        return "RealAccess('%s')" % self.file.path


class Attack(Base):
    """Defines Spoofing Attacks (illicit attempts to authenticate)"""

    __tablename__ = 'attack'

    attack_support_choices = ('replay', 'voice_conversion', 'speech_synthesis', 'unknown')
    """Types of attacks support"""

    attack_device_choices = ('laptop', 'laptop_HQ_speaker', 'phone1', 'phone2', 'logical_access',
                             'physical_access', 'physical_access_HQ_speaker', 'unknown')
    """Types of devices and types of access used for spoofing"""

    id = Column(Integer, primary_key=True)
    """Unique identifier for this attack"""

    file_id = Column(Integer, ForeignKey('file.id'))  # for SQL
    """The file identifier this attack is linked to"""

    attack_support = Column(Enum(*attack_support_choices))
    """The attack support"""

    attack_device = Column(Enum(*attack_device_choices))
    """The attack device"""

    # for Python
    file = relationship(File, backref=backref('attack', order_by=id))
    """A direct link to the :py:class:`.File` object bound to this attack"""

    protocols = relationship("Protocol", secondary=attacks_protocols,
                             backref='attack')
    """A direct link to the protocols this file is linked to"""

    def __init__(self, file, attack_support, attack_device):
        self.file = file
        self.attack_support = attack_support
        self.attack_device = attack_device

    def __repr__(self):
        return "Attack('%s')" % self.file.path
