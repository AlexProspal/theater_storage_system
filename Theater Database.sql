SET client_min_messages TO WARNING;

DROP TABLE IF EXISTS Checkout CASCADE;
DROP TABLE IF EXISTS ItemProduction CASCADE;
DROP TABLE IF EXISTS Item CASCADE;
DROP TABLE IF EXISTS StorageLocation CASCADE;
DROP TABLE IF EXISTS Category CASCADE;
DROP TABLE IF EXISTS Production CASCADE;
DROP TABLE IF EXISTS Member CASCADE;

CREATE TABLE Member (
    member_id   SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT UNIQUE,
    phone       TEXT,
    role        TEXT           
);

CREATE TABLE Production (
    production_id SERIAL PRIMARY KEY,
    title         TEXT NOT NULL,
    season        TEXT,          
    open_date     DATE,
    close_date    DATE
);

CREATE TABLE Category (
    category_id  SERIAL PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,  
    description  TEXT
);

CREATE TABLE StorageLocation (
    location_id  SERIAL PRIMARY KEY,
    code         TEXT NOT NULL UNIQUE,  
    description  TEXT
);

CREATE TABLE Item (
    item_id      SERIAL PRIMARY KEY,
    tag_code     TEXT NOT NULL UNIQUE,  
    name         TEXT NOT NULL,      
    category_id  INT REFERENCES Category(category_id),
    size         TEXT,              
    color        TEXT,              
    notes        TEXT,
    location_id  INT REFERENCES StorageLocation(location_id)
);

CREATE TABLE ItemProduction (
    item_production_id SERIAL PRIMARY KEY,
    item_id            INT NOT NULL REFERENCES Item(item_id) ON DELETE CASCADE,
    production_id      INT NOT NULL REFERENCES Production(production_id) ON DELETE CASCADE,
    character_name     TEXT,        
    notes              TEXT,
    UNIQUE (item_id, production_id, character_name)
);

CREATE TABLE Checkout (
    checkout_id   SERIAL PRIMARY KEY,
    item_id       INT NOT NULL REFERENCES Item(item_id) ON DELETE CASCADE,
    member_id     INT REFERENCES Member(member_id) ON DELETE SET NULL,
    production_id INT REFERENCES Production(production_id) ON DELETE SET NULL,
    checkout_date DATE NOT NULL DEFAULT CURRENT_DATE,
    notes         TEXT
);
