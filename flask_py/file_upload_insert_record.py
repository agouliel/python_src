# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
# sqlite3 db.sqlite3
# CREATE TABLE employee(id INTEGER PRIMARY KEY, name TEXT NOT NULL, photo BLOB);

import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(empId, name, photo):
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = "INSERT INTO person(id, name, photo) VALUES (?, ?, ?)"

        empPhoto = convertToBinaryData(photo)
        # Convert data into tuple format
        data_tuple = (empId, name, empPhoto)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into SQLite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite connection is closed")

insertBLOB(1, "Smith", "image.jpg")
