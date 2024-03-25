import mysql.connector

def get_database_row():
    try:
        # Establishing a connection to the MySQL server
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="jelly0612",
            database="Python"
        )

        if mydb.is_connected():
            print("Connected to MySQL database")

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM Games")
        myResult = mycursor.fetchall()

        return myResult  # Return the result

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

    # finally:
    #     if 'mydb' in locals() and mydb.is_connected():
    #         mydb.close()
    #         print("MySQL database connection closed")
