-- Tabela użytkowników
CREATE TABLE users (
    sub VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

-- Tabela konwersacji
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user1_sub VARCHAR(255) NOT NULL REFERENCES users(sub),
    user2_sub VARCHAR(255) NOT NULL REFERENCES users(sub),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela wiadomości
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_sub VARCHAR(255) NOT NULL REFERENCES users(sub),
    content TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);