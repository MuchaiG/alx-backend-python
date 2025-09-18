#!/usr/bin/python3
import mysql.connector


def stream_user_ages():

    # yield ages one by one from user_data table.
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:   
        yield int(age)

    cursor.close()
    connection.close()


def compute_average_age():

    # Compute the average age without loading all rows into memory.
    total, count = 0, 0
    for age in stream_user_ages():   
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")


# Run when executed directly
if __name__ == "__main__":
    compute_average_age()
