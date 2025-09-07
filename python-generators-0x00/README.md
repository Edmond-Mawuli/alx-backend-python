# Python Generators – Task 0

## Objective
Create a generator that streams rows from an SQL database one by one.

## Setup
- Database: `ALX_prodev`
- Table: `user_data`
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)

## Files
- **seed.py**: sets up the database, table, and seeds data from `user_data.csv`.
- **0-main.py**: test script that runs the functions from `seed.py`.

## Steps
1. Connect to MySQL (`connect_db`).
2. Create `ALX_prodev` database (`create_database`).
3. Connect to `ALX_prodev` (`connect_to_prodev`).
4. Create table `user_data` (`create_table`).
5. Insert data from `user_data.csv` (`insert_data`).

## Usage
```bash
$ ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('uuid1', 'Name1', 'Email1', Age1), ...]
