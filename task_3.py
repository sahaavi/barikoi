import mysql.connector

try:
    #connecting to database
    #use your hostname, username, password, databasename
    connection = mysql.connector.connect(host='127.0.0.1',
                                         user='root',
                                         password='pass',
                                         database='barikoi')
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

    #taking user's name and email as user input
    name = input("Enter Name: ")
    email = input("Enter E-mail: ")
    
    #getting the user location from the users table
    user_loc = []
    cursor = connection.cursor()
    cursor.execute("SELECT ST_X(location) as longitude, ST_Y(location) as latitude FROM users WHERE name=%s AND email=%s", (name,email))
    user_loc = cursor.fetchall()

    #cheking wheter the user exists or not
    if len(user_loc):
        long = user_loc[0][0]
        lat = user_loc[0][1]
        #creating the location point as string using the longtitude and latitude
        loc = "POINT ({} {})".format(long, lat)

        #finding the area of that location from area_map table
        user_area = []
        cursor.execute("SELECT id FROM area_map WHERE ST_Contains(polygon, ST_GeomFromText(%s))", (loc,))
        user_area = cursor.fetchone()

        #finding load shedding schedule of that user's area
        cursor.execute("SELECT time FROM load_shedding_schedule WHERE area_id=%s", (user_area[0],))
        load_shedding_schedule = cursor.fetchall()
        print("Load Shedding Schedule: {}".format(load_shedding_schedule[0][0]))

    #if the user input name or email do not exist in users table    
    else:
        print("No such user found")

#show the errors of sql if occurs
except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)

#closing the database conncetion
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
