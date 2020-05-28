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
mySql_insert_query  = "SELECT * FROM logging WHERE (SECTION LIKE 'email%') "
mySql_insert_query += "AND (datetime < {}) AND (datetime >= {});"

#mySql_insert_query = mySql_insert_query.format(yesterday,two_days_ago)
mySql_insert_query = mySql_insert_query.format(1589816930,1589811030)

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

# parse loaded userids
userids = set([ i[0] for i in result ])
N = len(userids)

#---------------------------------------#
#
# 2 - Take the next N userids in the
#     control list and in the treatment list,
#     respecting their proportion,
#     and prepare emails to be sent
#
#---------------------------------------#

import os.path
import json

# 2a - Get number of hashes already used

print 'Loading used userids...'

infile = 'n_hashes_used.dat' 
if not os.path.isfile(infile):
    n_hashes_used = 0
else:
    with open(infile) as f:
        n_hashes_used = int(f.read())

print(n_hashes_used,'userids used so far')

# 2b - Read new userids to be sent

infile = 'random_hashes_seed10000.txt'
with open(infile) as f:
    lines = [ line.strip() for line in f.readlines() ]

next_hashes = lines[n_hashes_used:(n_hashes_used+N)]

old_to_new_userids = { o:n for o,n in zip(userids,next_hashes) }

print("old_to_new_userids dictionary:")
print(old_to_new_userids)

# 2c - Save old_to_new_userids dictionary

outfile = 'old_to_new_userids.json'
with open(outfile,'w') as f:
    json.dump(old_to_new_userids, f)

# 2d - Update the number of hashes used

n_hashes_used += N

outfile = 'n_hashes_used.dat'
with open(outfile,'w') as f:
    f.write(str(n_hashes_used))

print('Number of userids used so far updated to', n_hashes_used)

#---------------------------------------#
#
# 3 - Prepare emails and send them
#
#---------------------------------------#

import smtplib
from email.mime.text import MIMEText

email_message = 'Dear Recipient,\n\nI hope you are doing well.\n\nBest wishes,\nSender'
email_subject = 'Testing'
email_from    = "chico.camargo@oii.ox.ac.uk"
email_to      = "chico.camargo@gmail.com"

print('Sending email to '+email_to)

msg = MIMEText(email_message)
msg['Subject'] = email_subject
msg['From']    = email_from 
msg['To']      = email_to

s = smtplib.SMTP("smtp.ox.ac.uk")
s.sendmail(email_from, email_to, msg.as_string())
s.quit()

print('Email sent')

