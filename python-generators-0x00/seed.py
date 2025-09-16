#!/usr/bin/env python3
import csv
import uuid
import mysql.connector
from mysql.connector import Error


def connect_db():
    """Connect to MySQL server (no database selected yet)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",       
            password="@Abc.123@!" 
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    print("Database 'ALX_prodev' is ready.")
    cursor.close()


def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="@Abc.123@!", 
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create user_data table if not exists."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX (user_id)
        )
    """)
    print("Table 'user_data' is ready.")
    cursor.close()


def insert_data(connection, data):
    """
    Insert a row into user_data if it does not already exist (check by email).
    Data is expected as (name, email, age).
    """
    cursor = connection.cursor()
    # check existence
    cursor.execute("SELECT * FROM user_data WHERE email = %s", (data[1],))
    existing = cursor.fetchone()
    if existing:
        print(f" Skipping duplicate: {data[1]}")
    else:
        cursor.execute(
            "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
            (str(uuid.uuid4()), data[0], data[1], data[2])
        )
        connection.commit()
        print(f"Inserted {data[1]}")
    cursor.close()


def stream_rows(connection):
    """Generator: stream rows one by one from user_data table."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()


def seed_from_csv(csv_file, connection):
    """Read CSV and insert data."""
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            insert_data(connection, row)


if __name__ == "__main__":
    
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)

        seed_from_csv("user_data.csv", db_conn)

        print("\n Streaming rows one by one:")
        for row in stream_rows(db_conn):
            print(row)

        db_conn.close()
