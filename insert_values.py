from auth import Auth
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

# prepare query string

infile = 'INDVOL_random_surveys.csv'
with open(infile) as f:
    socinfos = [ '['+line.strip()+']' for line in f.readlines() ][1:]

infile = 'random_hashes_seed10000.txt'
with open(infile) as f:
    userids = [ line.strip() for line in f.readlines() ]

# 20/80 split
rounds = ( ['control']*20 + ['treatment']*80 )*100

query_string = ','.join([ '("{}", "{}", "{}")'.format(userid, rd, percentages)
			  for userid, rd, percentages in zip(userids, rounds, socinfos) ])
 
mySql_insert_query_prefix = "INSERT INTO socinfo (userid, round, percentages) VALUES "
mySql_insert_query = mySql_insert_query_prefix + query_string + ';'


try:
    connection = mysql.connector.connect(host=Auth.servername,
                                         database=Auth.dbname,
                                         user=Auth.username,
                                         password=Auth.password)
    
    cursor = connection.cursor()
    cursor.execute(mySql_insert_query)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into socinfo table")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into socinfo table {}".format(error))

finally:
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")
