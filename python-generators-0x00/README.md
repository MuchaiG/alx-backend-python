# ALX_prodev Database Seeder

This project contains a Python script (`seed.py`) that sets up and populates a MySQL database (`ALX_prodev`) with sample user data.

## Features
- Creates a MySQL database `ALX_prodev` if it does not exist
- Creates a `user_data` table with the following fields:
  - `user_id` (UUID, Primary Key)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populates the table with data from `user_data.csv`
- Provides a generator to stream rows one by one from the database

## Requirements
- Python 3
- `mysql-connector-python` library  
  Install it with:
  ```bash
  pip install mysql-connector-python
