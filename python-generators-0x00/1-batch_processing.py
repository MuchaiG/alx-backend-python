#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    
    # fetch rows from user_data table in batches.
    # Yields lists of rows (each up to batch_size).
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         
        password="password", 
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:  
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch   

    cursor.close()
    connection.close()
    return   


def batch_processing(batch_size):

    # process batches of users and yield only users older than 25.

    for batch in stream_users_in_batches(batch_size): 
        filtered = [user for user in batch if int(user["age"]) > 25]
        yield filtered

    return


# Test run
if __name__ == "__main__":
    for users in batch_processing(3):
        if users:
            print(users)

