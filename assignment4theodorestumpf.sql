-- Dropping existing tables
DROP TABLE IF EXISTS ev_invites;
DROP TABLE IF EXISTS ev_events;
DROP TABLE IF EXISTS ev_users;

-- Your code goes here
-- Use comments to separate each section

# 1
CREATE TABLE ev_users (
    username VARCHAR(20) UNIQUE NOT NULL,
    first VARCHAR(40),
    last VARCHAR(40),
    affiliation VARCHAR(40) DEFAULT 'None',
    PRIMARY KEY (username)
);

#2
CREATE TABLE ev_events (
    id INT AUTO_INCREMENT NOT NULL,
    title VARCHAR(40) NOT NULL DEFAULT '',
    longitude FLOAT,
    latitude FLOAT,
    owner VARCHAR(20) NOT NULL,
    start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `end` TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (owner) REFERENCES ev_users (username)
);

#3
CREATE TABLE ev_invites (
    event_id INT NOT NULL,
    username VARCHAR(20) NOT NULL,
    status ENUM ('Accepted', 'Declined', 'Maybe'),
    PRIMARY KEY (event_id, username),
    FOREIGN KEY (event_id) REFERENCES ev_events (id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES ev_users (username) ON DELETE CASCADE
);

#4
INSERT INTO ev_users (username, first, last, affiliation) VALUES
	('stumpft19', 'Theodore', 'Stumpf', 'Hanover College, Student'),
	('wrynnt19', 'Theresa', 'Wrynn', 'Hanover College, Student'),
	('skiadas', 'Charilaos', 'Skiadas', 'Hanover College, Faculty, Staff');

#5
INSERT INTO ev_events (owner, title, start, longitude, latitude) VALUES
	('stumpft19', 'Homecoming get-together', TIMESTAMP('2018-10-8 8:00:00'), -85.462543, 38.714985);

#6
INSERT INTO ev_invites(event_id, username, status)
	SELECT id, owner, 'Accepted' FROM ev_events AS e
		WHERE NOT EXISTS(
			SELECT TRUE FROM ev_invites AS i
			WHERE i.event_id = e.id
			AND i.username = e.owner);

#7
INSERT INTO ev_invites(event_id, username)
	SELECT e.id, u.username FROM ev_events AS e, ev_users AS u
		WHERE e.title LIKE '%Homecoming%'
		AND u.affiliation LIKE '%Hanover College%'
		AND NOT EXISTS (
			SELECT TRUE FROM ev_invites as i
				WHERE i.event_id = e.id
				AND i.username = u.username);

#8
UPDATE ev_events AS e
	SET e.`end` = e.start + INTERVAL 2 HOUR
    WHERE (e.`end` IS NULL
    OR e.start >= e.`end`)
    AND e.id > 0;


#9
UPDATE ev_events AS e
	SET e.start = e.start + INTERVAL 1 DAY,
		e.`end`= e.`end` + INTERVAL 1 DAY
	WHERE e.id IN (
		SELECT i.event_id
        FROM ev_invites AS i
        WHERE i.status = 'Accepted'
        GROUP BY event_id
        HAVING COUNT(status) < 5)
	AND id > 0;

# TEST
#SELECT * FROM ev_events;
#SELECT * FROM ev_invites;