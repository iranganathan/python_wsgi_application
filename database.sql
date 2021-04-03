CREATE TABLE region(
    id_region INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(80) NOT NULL
);

CREATE TABLE city(
    id_city INTEGER PRIMARY KEY AUTOINCREMENT,
    id_region INT NOT NULL,
    name CHAR(80) NOT NULL,
    FOREIGN KEY (id_region) REFERENCES region(id_region)
);

CREATE TABLE feedback(
    id_feedback INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name CHAR(80) NOT NULL,
    first_name CHAR(80) NOT NULL,
    id_region INT,
    id_city INT,
    phone CHAR(20),
    email CHAR(80),
    message TEXT NOT NULL,
    FOREIGN KEY (id_region) REFERENCES region(id_region),
    FOREIGN KEY (id_city) REFERENCES city(id_city)
);

INSERT INTO region (name) VALUES ('New York');
INSERT INTO region (name) VALUES ('Washington');
INSERT INTO region (name) VALUES ('California');

INSERT INTO city (id_region, name) VALUES (1, 'New York City');
INSERT INTO city (id_region, name) VALUES (1, 'Buffalo');
INSERT INTO city (id_region, name) VALUES (1, 'Yonkers');
INSERT INTO city (id_region, name) VALUES (2, 'Seattle');
INSERT INTO city (id_region, name) VALUES (2, 'Vancouver');
INSERT INTO city (id_region, name) VALUES (2, 'Marysville');
INSERT INTO city (id_region, name) VALUES (3, 'Los Angeles');
INSERT INTO city (id_region, name) VALUES (3, 'San Francisco');
INSERT INTO city (id_region, name) VALUES (3, 'Sacramento');
INSERT INTO city (id_region, name) VALUES (3, 'Oakland');

INSERT INTO feedback (last_name, first_name, id_region, id_city, phone, email, message)
VALUES ('Jones', 'David', 2, 5, '+1-360-555-0133', 'davidjones@example.com', 'Hello world!');

INSERT INTO feedback (last_name, first_name, id_region, id_city, phone, email, message)
VALUES ('Martinez', 'Jack', 2, 4, '+1-206-555-0152', 'jackmartinez@example.com', 'Lorem ipsum');

INSERT INTO feedback (last_name, first_name, id_region, id_city, phone, email, message)
VALUES ('Walker', 'Emma', 2, 4, '+1-206-555-0107', 'emmawalker@example.com', 'Seattle is Amazing!');

INSERT INTO feedback (last_name, first_name, id_region, id_city, phone, email, message)
VALUES ('Rivera', 'Nick', 3, 7, '+1-323-555-0715', 'nickrivera@example.com', 'Buenas tardes!');

INSERT INTO feedback (last_name, first_name, id_region, id_city, phone, email, message)
VALUES ('Turner', 'Kate', 3, 10, '+1-510-555-0112', 'kateturner@example.com', 'Hi!');
