# Name: Theodore Stumpf

import random
from datetime import datetime, timedelta
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# The Status class is used in the enum column that you create in question 3
# enum package documentation: https://docs.python.org/3/library/enum.html
import enum
class Status(enum.Enum):
    Accepted = 1
    Declined = 2
    Maybe = 3

engine = create_engine('sqlite:///:memory:', echo=True)


###### CLASS AND TABLE DEFINITIONS GO HERE
#1
class User(Base):
    __tablename__ = 'ev_users'

    username    = Column(String(20), unique = False, nullable = False, primary_key = True)
    first       = Column(String(40))
    last        = Column(String(40))
    affiliation = Column(String(40), default='None')

    ownededEvents = relationship('Event', back_populates='ownedBy')
    invites = relationship('Invite', back_populates='user')

#2
class Event(Base):
    __tablename__ = 'ev_events'

    id         = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    title      = Column(String(40), nullable=False, default='')
    longitude  = Column(Float(precision=32))
    latitude   = Column(Float(precision=32))
    owner_name = Column(String(20), ForeignKey("ev_users.username", ondelete="CASCADE"), nullable=False)
    start      = Column(DateTime, nullable=False, default=datetime.now())
    evend      = Column(DateTime, default=None)

    ownedBy = relationship('User', back_populates='ownededEvents')
    invites = relationship('Invite', back_populates='event')

#4
class Invite(Base):
    __tablename__ = 'ev_invites'

    event_id = Column(Integer, ForeignKey('ev_events.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    username = Column(String(20), ForeignKey('ev_users.username', ondelete='CASCADE'), nullable=False, primary_key=True)
    status   = Column(Enum(Status))

    user = relationship('User', back_populates='invites')
    event = relationship('Event', back_populates='invites')


###### END OF CLASS AND TABLE DEFINITIONS

# Drop existing tables and recreate them
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

###### WRITE YOUR ANSWERS TO OTHER QUESTIONS HERE

def random_choice(entries):
    pop = [val for val, cnt in entries for i in range(cnt)]
    return random.choice(pop)

#6
student = User(username = 'stumpft19', first = 'Theodore', last = 'Stumpf', affiliation = 'Hanover College, Student')
professor = User(username = 'skiadas', first = 'Charilaos', last = 'Skiadas', affiliation = 'Hanover College, Faculty, Staff')
session.add(student)
session.add(professor)

#7
student_list = [User(username = 'student' + str(i), first = 'Number' + str(i), last = 'Student', affiliation = 'Hanover College, Student') for i in range(1, 101)]
session.add_all(student_list)
session.commit()

#8
get_together = Event(owner_name = 'stumpft19', title = 'Homecoming get-together', start = datetime(2018, 10, 8, hour = 8), longitude = -85.462543, latitude = 38.714985)
session.add(get_together)
session.commit()

#9
invites = [Invite(event_id = get_together.id, username = student_list[i].username) for i in range(len(student_list))]
session.add_all(invites)
session.commit()

#10
invite_statuses = [random_choice([(Status.Accepted, 3),  (Status.Declined, 3), (Status.Maybe, 4)]) for i in range(len(student_list))]

pairs = zip(invites, invite_statuses)
for invite, new_status in pairs:
    invite.status = new_status
session.commit()

#11
accepted = [invite.user.first + " " + invite.user.last for invite in get_together.invites if invite.status == Status.Accepted]
print()
[print(accepted[i]) for i in range(len(accepted))]

###### BELOW THIS LINE YOU CAN ADD ANY CODE YOU WANT TO HAVE FOR TESTING
