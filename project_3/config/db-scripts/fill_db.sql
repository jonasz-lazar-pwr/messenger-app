-- === Reset existing tables ===

DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS chats;
DROP TABLE IF EXISTS users;

-- === Create tables ===

CREATE TABLE users (
    sub TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    user1_sub TEXT NOT NULL REFERENCES users(sub),
    user2_sub TEXT NOT NULL REFERENCES users(sub),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    chat_id INTEGER REFERENCES chats(id) ON DELETE CASCADE,
    sender_sub TEXT NOT NULL REFERENCES users(sub),
    content TEXT,
    media_url TEXT,
    media_id UUID,
    sent_at TIMESTAMP DEFAULT NOW()
);

-- === Seed sample users ===

INSERT INTO users (sub, email, first_name, last_name) VALUES
('user-sub-0', 'me@example.com', 'Alice', 'Main'),
('user-sub-1', 'anna@example.com', 'Anna', 'Smith'),
('user-sub-2', 'john@example.com', 'John', 'Doe'),
('user-sub-3', 'peter@example.com', 'Peter', 'Johnson'),
('user-sub-4', 'adam@example.com', 'Adam', 'Brown'),
('user-sub-5', 'marry@example.com', 'Marry', 'White'),
('user-sub-6', 'randy@example.com', 'Randy', 'Black');

-- === Seed sample chats ===

INSERT INTO chats (id, user1_sub, user2_sub) VALUES
(1, 'user-sub-6', 'user-sub-0'),
(2, 'user-sub-6', 'user-sub-2'),
(3, 'user-sub-6', 'user-sub-3');

-- === Seed messages for each chat ===

INSERT INTO messages (chat_id, sender_sub, content) VALUES
(1, 'user-sub-6', 'Hi Alice!'),
(1, 'user-sub-0', 'Hey!'),
(1, 'user-sub-6', 'How is your day?'),
(1, 'user-sub-0', 'Busy, as always!'),
(1, 'user-sub-6', 'Let me know if you need help.');

INSERT INTO messages (chat_id, sender_sub, content) VALUES
(2, 'user-sub-6', 'Hey John!'),
(2, 'user-sub-2', 'Yo!'),
(2, 'user-sub-6', 'Wanna catch up later?'),
(2, 'user-sub-2', 'Sure, ping me after 6.'),
(2, 'user-sub-6', 'Cool, see ya!');

INSERT INTO messages (chat_id, sender_sub, content) VALUES
(3, 'user-sub-6', 'Hi Peter!'),
(3, 'user-sub-3', 'Hi!'),
(3, 'user-sub-6', 'Let’s play later?'),
(3, 'user-sub-3', 'Sure thing. 9pm?'),
(3, 'user-sub-6', 'Perfect.');

-- === Reset auto-increment counters for SERIAL IDs ===

SELECT setval(pg_get_serial_sequence('chats', 'id'), (SELECT MAX(id) FROM chats));
SELECT setval(pg_get_serial_sequence('messages', 'id'), (SELECT MAX(id) FROM messages));
