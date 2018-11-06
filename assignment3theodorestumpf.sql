# Working with databases
#
# This script will delete and then remake the tables for this assignment.
# Load the script when you need to "reset" things.
# You will also add your solutions at the bottom.

DROP TABLE IF EXISTS acquaintances;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS profiles;

# Add your answers here

# 1
CREATE TABLE profiles (
	username VARCHAR(20) UNIQUE NOT NULL,
    first	 VARCHAR(40),
    last	 VARCHAR(40) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE messages (
	id			INT UNIQUE NOT NULL AUTO_INCREMENT,
    sender		VARCHAR(20) NOT NULL,
    recipient	VARCHAR(20) NOT NULL,
    message		VARCHAR(400) NOT NULL DEFAULT "",
    is_read		BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    in_reply_to INT DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (sender) REFERENCES profiles(username) ON DELETE CASCADE,
    FOREIGN KEY (recipient)  REFERENCES profiles(username) ON DELETE CASCADE,
    FOREIGN KEY (in_reply_to)  REFERENCES messages(id) ON DELETE SET NULL
);

CREATE TABLE acquaintances (
    source	VARCHAR(20) NOT NULL,
    target	VARCHAR(20) NOT NULL,
    PRIMARY KEY (source, target),
    FOREIGN KEY (source) REFERENCES profiles(username) ON DELETE CASCADE,
    FOREIGN KEY (target) REFERENCES profiles(username) ON DELETE CASCADE
);


#2
INSERT INTO profiles (username, first, last) VALUES
	('admin', NULL, 'Admin'),
    ('stumpft19', 'Theodore', 'Stumpf'),
    ('FCS', 'Alan', 'Turing');

#3
INSERT INTO acquaintances (source, target) VALUES
	('stumpft19', 'FCS');

#4
INSERT INTO acquaintances (source, target)
	SELECT 'admin', username FROM profiles
		WHERE username != 'admin';

#5
INSERT INTO messages(sender, recipient, message) VALUES
	('stumpft19', 'FCS', 'Congratulations on publishing "On Computable Numbers, with an Application to the Entscheidungsproblem."!');

#6
INSERT INTO messages (sender, recipient, message, is_read)
	SELECT 'admin', target, 'Welcome to our messaging service', TRUE FROM acquaintances
		WHERE source = 'admin';

#7
INSERT INTO messages (sender, recipient, message, in_reply_to)
	SELECT 'FCS', sender, 'I am sorry but I am unable to reply to all of my fans at the current time.', id FROM messages
		WHERE recipient = 'FCS'
		AND is_read = FALSE;

UPDATE messages as m
SET m.is_read = TRUE
WHERE m.recipient = 'FCS'
AND m.is_read = FALSE
AND m.id > 0;

#8
SELECT m.sender, m.recipient
FROM messages AS m
WHERE NOT EXISTS (SELECT TRUE
	FROM acquaintances AS a
    WHERE a.source = m.sender
    
    AND a.target = m.recipient);

#SELECT * FROM profiles;
#SELECT * FROM acquaintances;
#SELECT * FROM messages;