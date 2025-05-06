-- Add other users
INSERT INTO users (sub, email, first_name, last_name) VALUES
('user-sub-1', 'anna@example.com', 'Anna', 'Smith'),
('user-sub-2', 'john@example.com', 'John', 'Doe'),
('user-sub-3', 'peter@example.com', 'Peter', 'Johnson');

-- Conversations
INSERT INTO conversations (user1_sub, user2_sub) VALUES
('84c8a458-f061-70e2-30cf-d1a71b1f04fb', 'user-sub-1'),
('user-sub-2', '84c8a458-f061-70e2-30cf-d1a71b1f04fb'),
('84c8a458-f061-70e2-30cf-d1a71b1f04fb', 'user-sub-3');

-- Conversation 1
INSERT INTO messages (conversation_id, sender_sub, content) VALUES
(1, '84c8a458-f061-70e2-30cf-d1a71b1f04fb', 'Hi Anna!'),
(1, 'user-sub-1', 'Hey, how are you?');

-- Conversation 2
INSERT INTO messages (conversation_id, sender_sub, content) VALUES
(2, 'user-sub-2', 'Did you see that assignment?'),
(2, '84c8a458-f061-70e2-30cf-d1a71b1f04fb', 'Yeah, it looks tough.');

-- Conversation 3
INSERT INTO messages (conversation_id, sender_sub, content) VALUES
(3, '84c8a458-f061-70e2-30cf-d1a71b1f04fb', 'Hey Peter!'),
(3, 'user-sub-3', 'Yo!');