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
#use your hostname, username, password, databasename
import_data("127.0.0.1", "root", "pass", "barikoi", "users.csv", query_1)

##inserting data to area_map table
query_2 = "INSERT INTO `area_map` (`id`, `area_name`, `polygon`) VALUES (%s, %s, ST_GeomFromText(%s))"
import_data("127.0.0.1", "root", "pass", "barikoi", "area_map.csv", query_2)

##inserting data to load_shedding_schedule table
query_3 = "INSERT INTO `load_shedding_schedule` (`area_id`, `time`) VALUES (%s, %s)"
import_data("127.0.0.1", "root", "pass", "barikoi", "load_shedding_schedule.csv", query_3)
