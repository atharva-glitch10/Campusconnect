-- =============================================================
-- Interest Matching Database Schema
-- =============================================================

CREATE DATABASE IF NOT EXISTS interest_matching;
USE interest_matching;

-- Drop tables in reverse dependency order (safe re-runs)
DROP TABLE IF EXISTS user_availability;
DROP TABLE IF EXISTS user_interests;
DROP TABLE IF EXISTS interests;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Interests table
CREATE TABLE interests (
    interest_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Many-to-many relationship between users and interests
CREATE TABLE user_interests (
    user_id INT NOT NULL,
    interest_id INT NOT NULL,
    PRIMARY KEY (user_id, interest_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (interest_id) REFERENCES interests(interest_id) ON DELETE CASCADE
);

-- User availability slots
CREATE TABLE user_availability (
    user_id INT NOT NULL,
    slot INT NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id, slot),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);