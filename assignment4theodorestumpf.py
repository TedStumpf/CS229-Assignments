# Name:
## Reading database keys
import json
with open('keys.json', 'r') as f:
   account_info = json.loads(f.read())
   vault = account_info['vault']

from datetime import datetime, timedelta
from sqlalchemy import *

# The Status class is used in the enum column that you create in question 3
# enum package documentation: https://docs.python.org/3/library/enum.html
import enum
class Status(enum.Enum):
    Accepted = 1
    Declined = 2
    Maybe = 3

engineString = 'mysql+mysqldb://{username}:{password}@{server}/{schema}'
engineUrl = engineString.format(**vault)

# Establishing a specific database connection
engine = create_engine(engineUrl, echo = True)

metadata = MetaData()
conn = engine.connect()

#   1
tblUsers = Table('ev_users', metadata,
   Column('username', String(20), unique=True, nullable=False, primary_key=True),
   Column('first', String(40)),
   Column('last', String(40)),
   Column('affiliation', String(40), default='None')
)

#2
tblEvents = Table('ev_events', metadata,
   Column('id', Integer, unique=True, nullable=False, primary_key=True),
   Column('title', String(40), nullable=False, default=''),
   Column('longitude', Float(precision=32)),
   Column('latitude', Float(precision=32)),
   Column('owner', String(40), ForeignKey("ev_users.username", ondelete="CASCADE"), nullable=False),
   Column('start', DateTime, nullable=False, default=datetime.now()),
   Column('evend', DateTime, default=None)
)

#3
tblInvites = Table('ev_invites', metadata,
    Column('event_id', Integer, ForeignKey("ev_events.id", ondelete="CASCADE"), nullable=False, primary_key=True),
    Column('username', String(20), ForeignKey("ev_users.username", ondelete="CASCADE"), nullable=False, primary_key=True),
    Column('status', Enum(Status))
)
# Drop existing tables
metadata.drop_all(engine)
# Create these tables if they do not exist
metadata.create_all(engine)

#4
users = [
    { 'username': 'stumpft19', 'first': 'Theodore', 'last': 'Stumpf', 'affiliation': 'Hanover College, Student' },
    { 'username': 'wrynnt19', 'first': 'Theresa', 'last': 'Wrynn', 'affiliation': 'Hanover College, Student' },
    { 'username': 'skiadas', 'first': 'Charilaos', 'last': 'Skiadas', 'affiliation': 'Hanover College, Faculty, Staff' }
]
conn.execute(tblUsers.insert(), users)

#5
event = [{'owner': 'stumpft19', 'title': 'Homecoming get-together', 'start': datetime(2018, 10, 8, hour = 8), 'longitude': -85.462543, 'latitude': 38.714985}]
conn.execute(tblEvents.insert(), event)

#6
events = conn.execute(select([tblEvents]))
new_invites = []
for e in events:
    found = False
    invites = conn.execute(select([tblInvites]))
    for i in invites:
        if (i['event_id'] == e['id']) and (i['username'] == e['owner']):
            found = True
            break
    if not found:
        new_invites.append({'event_id': e['id'], 'username': e['owner'], 'status': Status.Accepted})
    invites.close()

events.close()
conn.execute(tblInvites.insert(), new_invites)


#7
events = conn.execute(select([tblEvents]))
invites = conn.execute(select([tblInvites]))

new_invites = []
for e in events:
    users = conn.execute(select([tblUsers]))
    for u in users:
        found = False
        if ('Homecoming' in e['title']) and ('Hanover College' in u['affiliation']):
            invites = conn.execute(select([tblInvites]))
            for i in invites:
                if (i['event_id'] == e['id']) and (i['username'] == u['username']):
                    found = True
            invites.close()
            if not found:
                new_invites.append({'event_id': e['id'], 'username': u['username']})
    users.close()

events.close()
conn.execute(tblInvites.insert(), new_invites)

#8
update = tblEvents.update().\
            values(evend=(tblEvents.c.start + timedelta(hours=2))).\
            where(and_(
                or_(
                    tblEvents.c.evend == None,
                    tblEvents.c.evend <= tblEvents.c.start
                    ),
                tblEvents.c.id > 0))
conn.execute(update)

#9
#update = tblEvents.update().\
    


# Testing
print("Clear")


invites = conn.execute(select([tblInvites]))
events = conn.execute(select([tblEvents]))
for i in invites:
    print(i)
print("Clear")
for e in events:
    print(e)
invites.close()
events.close()


##9
#UPDATE ev_events AS e
#   SET e.start = e.start + INTERVAL 1 DAY,
#       e.`end`= e.`end` + INTERVAL 1 DAY
#   WHERE e.id IN (
#       SELECT i.event_id
#        FROM ev_invites AS i
#        WHERE i.status = 'Accepted'
#        GROUP BY event_id
#        HAVING COUNT(status) < 5)
#   AND id > 0;
#