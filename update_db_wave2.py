# -*- coding: UTF-8 -*-

from auth import Auth
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

#---------------------------------------#
#
# 1 - Take the userids of all the users 
#     who filled the form 2 days ago
#
#---------------------------------------#

from datetime import date, datetime, timedelta

today = date.today()

yesterday = today - timedelta(days=1)
yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)

try:
    # python3
    yesterday = int(round(yesterday.timestamp()))
except AttributeError:
    # python2
    dt = yesterday
    timestamp = (dt-datetime(1970, 1, 1)).total_seconds() - 3600
    yesterday = int(round(timestamp))

two_days_ago = today - timedelta(days=2)
two_days_ago = datetime(two_days_ago.year, two_days_ago.month, two_days_ago.day)
try:
    # python3
    two_days_ago = int(round(two_days_ago.timestamp()))
except AttributeError:
    # python2
    dt = two_days_ago 
    timestamp = (dt-datetime(1970, 1, 1)).total_seconds() - 3600
    two_days_ago = int(round(timestamp))

# prepare query string
mySql_insert_query  = "SELECT * FROM logging WHERE (section='rankings_wave1') "
mySql_insert_query += "AND (datetime < {}) AND (datetime >= {});"

mySql_insert_query = mySql_insert_query.format(yesterday,two_days_ago)

print('Date:')
print(today)
print('Submitting query: '+mySql_insert_query)


try:
    connection = mysql.connector.connect(host=Auth.servername,
                                         database=Auth.dbname,
                                         user=Auth.username,
                                         password=Auth.password)
    
    cursor = connection.cursor()
    cursor.execute(mySql_insert_query)

    result = cursor.fetchall()

    print(cursor.rowcount, "Successfully loaded info from logging table")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to load info from logging table {}".format(error))

finally:
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")

# parse loaded userids and emails
users = {}
for i in result:
    user  = i[0]
    email = i[2]
    users[user] = email
    print('users[{}] = {}'.format(user,email))

userids = []
emails  = []
for i,j in users.items():
    userids += [ str(i) ]
    emails  += [ str(j) ]

N = len(users)

#---------------------------------------------------#
#
# 2 - Take the next social information percentages
#
#---------------------------------------------------#

import os.path

# 2a - Get number of hashes already used

print 'Loading used userids...'

infile = 'n_hashes_used.dat' 
if not os.path.isfile(infile):
    n_hashes_used = 0
else:
    with open(infile) as f:
        n_hashes_used = int(f.read())

print(n_hashes_used,'userids used so far')

# 2b - Load next percentages

infile = '../indvol/INDVOL_random_surveys.csv'

with open(infile) as f:
    percentages = [ '['+line.strip()+']' for line in f.readlines()[1:] ]

new_percentages = percentages[n_hashes_used:(n_hashes_used+N)]

userids_to_percentages = { o:n for o,n in zip(userids,new_percentages) }

# 2c - Define next rounds

rounds = [ 'control' if (i%5==0) else 'treatment' for i in range(n_hashes_used, (n_hashes_used+N)) ]

# 2d - Update the number of hashes used

n_hashes_used += N

outfile = 'n_hashes_used.dat'
with open(outfile,'w') as f:
    f.write(str(n_hashes_used))

print('Number of userids used so far updated to', n_hashes_used)

#-----------------------------------------#
#
# 3 - Add prolific ids to the socinfo db
#
#-----------------------------------------#

# prepare query string
mySql_insert_query  = "INSERT INTO socinfo (userid,round,percentages) VALUES (%s,%s,%s);"

for user_id, user_round, user_percentages in zip(userids, rounds, new_percentages):
    try:
        conn   = mysql.connector.connect(host=Auth.servername, database=Auth.dbname, user=Auth.username, password=Auth.password)
        cursor = conn.cursor()
        cursor.execute(mySql_insert_query, (user_id, user_round, user_percentages))
        print("Successfully added to socinfo table:")
        print(user_id + ' / ' + user_round + ' / ' + user_percentages)
        conn.commit()
    except mysql.connector.Error as error:
        print("Failed to add rows to socinfo table: {}".format(error))
    finally:
        if (conn.is_connected()):
            conn.close()
            print("MySQL connection is closed")

