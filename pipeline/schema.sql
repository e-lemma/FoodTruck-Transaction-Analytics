-- remove any existing tables
DROP TABLE IF EXISTS eyuale_schema.transaction;
DROP TABLE IF EXISTS eyuale_schema.truck;
DROP TABLE IF EXISTS eyuale_schema.payment_method;
-- create payment method table
CREATE TABLE eyuale_schema.payment_method(
    id INT IDENTITY(1,1),
    name VARCHAR(16) UNIQUE NOT NULL,
    PRIMARY KEY(id)
);
-- create food truck table
CREATE TABLE eyuale_schema.truck(
    id INT IDENTITY(1,1),
    name VARCHAR(32) UNIQUE NOT NULL,
    description VARCHAR(128) UNIQUE NOT NULL,
    card_reader BOOLEAN NOT NULL,
    fsa_rating INT NOT NULL,
    PRIMARY KEY(id)
);
-- create food truck customer transaction table
CREATE TABLE eyuale_schema.transaction(
    id INT IDENTITY(1,1),
    truck_id INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    payment_method_id INT NOT NULL,
    total DECIMAL(5,2) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(truck_id) REFERENCES eyuale_schema.truck(id),
    FOREIGN KEY(payment_method_id) REFERENCES eyuale_schema.payment_method(id),
    CONSTRAINT duplicate_transactions UNIQUE (timestamp, truck_id)
);
-- seed data into payment_method table
INSERT INTO eyuale_schema.payment_method(name)
VALUES
    ('cash'),
    ('card');
-- seed data into truck table
INSERT INTO eyuale_schema.truck(name, description, card_reader, fsa_rating)
VALUES
    ('Burrito Madness',
    'An authentic taste of Mexico.',
    'true', 4),
    ('Kings of Kebabs',
    'Locally-sourced meat cooked over a charcoal grill.',
    'true', 2),
    ('Cupcakes by Michelle',
    'Handcrafted cupcakes made with high-quality, organic ingredients.',
    'true', 5),
    ('Hartmann''s Jellied Eels',
    'A taste of history with this classic English dish.',
    'true', 4),
    ('Yoghurt Heaven',
    'All the great tastes, but only some of the calories!',
    'true', 4),
    ('SuperSmoothie',
    'Pick any fruit or vegetable, and we''ll make you a delicious, healthy, multi-vitamin shake. Live well; live wild.',
    'false', 3);