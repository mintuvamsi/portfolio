-- CREATE DATABASE casino;


-- CREATE TABLE employees (
--     employee_id SERIAL PRIMARY KEY,
--     name VARCHAR(100),
--     position VARCHAR(100),
--     salary NUMERIC(10, 2),
--     hire_date DATE,
--     logged_in_time TIMESTAMP
-- );


-- CREATE TABLE customers (
--     customer_id SERIAL PRIMARY KEY,
--     name VARCHAR(100),
--     email VARCHAR(100),
--     phone VARCHAR(20),
--     birth_date DATE,
--     amount NUMERIC(10, 2),
--     membership_type VARCHAR(50),
--     timestamp TIMESTAMP
-- );

-- CREATE TABLE game_tables (
--     table_id SERIAL PRIMARY KEY,
--     game_type VARCHAR(50),
--     table_number INTEGER,
--     status VARCHAR(20)
-- );

-- INSERT INTO game_tables (game_type, table_number, status) VALUES
--     ('roulette', 1, 'available'),
--     ('roulette', 2, 'available'),
--     ('roulette', 3, 'available'),
--     ('roulette', 4, 'available'),
--     ('roulette', 5, 'available'),
--     ('roulette', 6, 'available'),
--     ('roulette', 7, 'available'),
--     ('roulette', 8, 'available'),
--     ('roulette', 9, 'available'),
--     ('roulette', 10, 'available'),

--     ('TCP', 1, 'available'),
--     ('TCP', 2, 'available'),
--     ('TCP', 3, 'available'),
--     ('TCP', 4, 'available'),

--     ('baccarat', 1, 'available'),
--     ('baccarat', 2, 'available'),
--     ('baccarat', 3, 'available'),
--     ('baccarat', 4, 'available'),
--     ('baccarat', 5, 'available'),
--     ('baccarat', 6, 'available'),

--     ('blackjack', 1, 'available'),
--     ('blackjack', 2, 'available'),
--     ('blackjack', 3, 'available'),
--     ('blackjack', 4, 'available'),
--     ('blackjack', 5, 'available'),
--     ('blackjack', 6, 'available'),
--     ('blackjack', 7, 'available'),
--     ('blackjack', 8, 'available'),
--     ('blackjack', 9, 'available'),
--     ('blackjack', 10, 'available');


-- ALTER TABLE game_tables
-- ADD COLUMN open_timestamp TIMESTAMP,
-- ADD COLUMN close_timestamp TIMESTAMP;

-- CREATE TABLE memberships (
--     membership_id SERIAL PRIMARY KEY,
--     membership_name VARCHAR(50) UNIQUE,
--     description TEXT
-- );

-- INSERT INTO memberships (membership_name, description) VALUES
--     ('silver', 'Basic membership level with standard benefits.'),
--     ('gold', 'Mid-tier membership level with enhanced benefits.'),
--     ('platinum', 'High-tier membership level with premium benefits.'),
--     ('black', 'Exclusive membership level with VIP treatment.'),
--     ('tribune', 'Elite membership level with unparalleled privileges.');

-- ALTER TABLE customers
-- ADD COLUMN gender VARCHAR(10);


-- SELECT column_name
-- FROM information_schema.columns
-- WHERE table_schema = 'public'
--   AND table_name = 'customers';


-- ALTER TABLE customers
-- ALTER COLUMN phone TYPE VARCHAR(30);  -- Adjust the length as needed

-- ALTER TABLE game_tables
-- ADD COLUMN inspector VARCHAR(100),
-- ADD COLUMN inspector_login_time TIMESTAMP,
-- ADD COLUMN dealer VARCHAR(100),
-- ADD COLUMN dealer_login_time TIMESTAMP;


-- ALTER TABLE game_tables
-- ADD COLUMN inspector_change_to VARCHAR(100),
-- ADD COLUMN inspector_change_time TIMESTAMP,
-- ADD COLUMN dealer_change_to VARCHAR(100),
-- ADD COLUMN dealer_change_time TIMESTAMP;


-- ALTER TABLE game_tables
-- ADD CONSTRAINT unique_game_table_info UNIQUE (table_id, game_type, table_number);

-- CREATE TABLE live_tables (
--     table_id INTEGER,
--     game_type VARCHAR(50),
--     table_number INTEGER,
--     status VARCHAR(20),
--     open_timestamp TIMESTAMP,
--     close_timestamp TIMESTAMP,
--     inspector VARCHAR(100),
--     inspector_login_time TIMESTAMP,
--     dealer VARCHAR(100),
--     dealer_login_time TIMESTAMP,
--     inspector_change_to VARCHAR(100),
--     inspector_change_time TIMESTAMP,
--     dealer_change_to VARCHAR(100),
--     dealer_change_time TIMESTAMP,
--     CONSTRAINT fk_game_table_info
--     FOREIGN KEY (table_id, game_type, table_number)
--     REFERENCES game_tables(table_id, game_type, table_number)
-- );


-- -- Add the new column
-- ALTER TABLE employees
-- ADD COLUMN logged_out_time TIMESTAMP;

-- -- Remove the salary column
-- ALTER TABLE employees
-- DROP COLUMN hire_date;

-- Drop foreign key constraints if they exist
ALTER TABLE live_tables DROP CONSTRAINT IF EXISTS fk_inspector_employee;
ALTER TABLE live_tables DROP CONSTRAINT IF EXISTS fk_dealer_employee;

-- Create foreign key constraints for inspector_id and dealer_id
ALTER TABLE live_tables
ADD CONSTRAINT fk_inspector_employee
FOREIGN KEY (inspector_id)
REFERENCES employees(employee_id);

ALTER TABLE live_tables
ADD CONSTRAINT fk_dealer_employee
FOREIGN KEY (dealer_id)
REFERENCES employees(employee_id);
