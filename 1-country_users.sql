-- a SQL script that creates a table users following these requirements:

-- 		id, integer, never null, auto increment and primary key
-- 		email, string (255 characters), never null and unique
-- 		name, string (255 characters)
-- 		country, enumeration of countries: US, CO and TN, never null (= default will be the first element of the enumeration, here US)

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users(
	id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(255) UNIQUE NOT NULL,
	name VARCHAR(255),
	country ENUM('US', 'CO', 'TN') DEFAULT 'US'
);