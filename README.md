After completing the Task 2 I have updated the users table with the new users csv file in the database using the following code:
```python
import mysql.connector
import csv

#defining function
def import_data(host_nm, user_nm, pass_word, db_nm, csv_file_nm, query):
    try:
        #connecting to database
        mydb = mysql.connector.connect(
        host=host_nm,
        user=user_nm,
        password=pass_word,
        database=db_nm
        )

        #reading the csv file
        with open(csv_file_nm) as csv_file:
            csvfile = csv.reader(csv_file, delimiter=',')
            next(csvfile)
            values=[]
            for value in csvfile:
                values.append(value)

        #inserting values to database
        cursor = mydb.cursor()
        cursor.executemany(query, values)
        mydb.commit()
        print(cursor.rowcount, "Record inserted successfully into table")

    #show the errors of sql if occurs
    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))
    
    #closing the database conncetion
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
            print("MySQL connection is closed")

#inserting data to users table
query_1 = "INSERT INTO `users` (`id`, `name`, `email`, `location`, `created_at`) VALUES (%s, %s, %s, ST_GeomFromText(%s), %s)"
import_data("127.0.0.1", "root", "Hello@8920", "barikoi", "unique_users.csv", query_1)
```
