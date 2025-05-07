-- Czyść dane z bazy
-- TRUNCATE TABLE messages RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE chats RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE users CASCADE;

-- Dodaj użytkowników
INSERT INTO users (sub, email, first_name, last_name) VALUES
('test-sub-123', 'test1@example.com', 'Test', 'User1'),
('test-sub-456', 'test2@example.com', 'Test', 'User2'),
('test-sub-nochats', 'nochats@example.com', 'NoChat', 'User'),
('test-sub-multi', 'multi@example.com', 'Multi', 'User'),
('test-sub-empty', 'empty@example.com', 'Empty', 'User'),
('chatmate-1', 'chatmate1@example.com', 'Mate', 'One'),
('chatmate-2', 'chatmate2@example.com', 'Mate', 'Two');

-- Dodaj czaty
-- Chat 1: test-sub-123 <-> test-sub-456
INSERT INTO chats (id, user1_sub, user2_sub) VALUES
(1, 'test-sub-123', 'test-sub-456');

-- Chat 2: test-sub-multi <-> chatmate-1
INSERT INTO chats (id, user1_sub, user2_sub) VALUES
(2, 'test-sub-multi', 'chatmate-1');

-- Chat 3: chatmate-2 <-> test-sub-multi
INSERT INTO chats (id, user1_sub, user2_sub) VALUES
(3, 'chatmate-2', 'test-sub-multi');

-- Chat 4: test-sub-123 <-> test-sub-empty
INSERT INTO chats (id, user1_sub, user2_sub) VALUES
(4,'test-sub-123', 'test-sub-empty');

-- Dodaj wiadomości do czatu 1
INSERT INTO messages (chat_id, sender_sub, content, media_url, media_id) VALUES
(1, 'test-sub-123', 'Hello from 123!', NULL, NULL),
(1, 'test-sub-456', 'Hello from 456!', NULL, NULL),
(1, 'test-sub-123', 'Check this image', 'http://example.com/image1.jpg', gen_random_uuid());

-- Dodaj wiadomości do czatu 2
INSERT INTO messages (chat_id, sender_sub, content, media_url, media_id) VALUES
(2, 'test-sub-multi', 'Multi here!', NULL, NULL),
(2, 'chatmate-1', 'Responding...', NULL, NULL),
(2, 'test-sub-multi', NULL, 'http://example.com/media2.jpg', gen_random_uuid());

-- Dodaj wiadomości do czatu 3
INSERT INTO messages (chat_id, sender_sub, content, media_url, media_id) VALUES
(3, 'chatmate-2', 'Yo!', NULL, NULL),
(3, 'test-sub-multi', 'Sup?', NULL, NULL),
(3, 'chatmate-2', NULL, 'http://example.com/video.mp4', gen_random_uuid());