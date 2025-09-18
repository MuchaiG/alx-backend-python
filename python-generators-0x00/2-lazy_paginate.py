#!/usr/bin/python3
import mysql.connector


def paginate_users(page_size, offset):
    
    # Fetch a single page of users from user_data table.
   
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         
        password="password", 
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM user_data LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):

    # lazily fetch pages from user_data table.
    # Uses only one loop.

    offset = 0
    while True:  
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Test run
if __name__ == "__main__":
    print("📌 Lazy pagination demo:")
    for page in lazy_paginate(5):   # fetch 5 users per page
        print("Page:")
        for user in page:
            print(user)
