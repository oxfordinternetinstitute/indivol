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

userids = []
emails  = []
for i,j in users.items():
    userids += [ str(i) ]
    emails  += [ str(j) ]

N = len(users)

#---------------------------------------#
#
# 2 - Take the next N userids in the
#     control list and in the treatment list,
#     respecting their proportion,
#     and prepare emails to be sent
#
#---------------------------------------#

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

# 2b - Read new userids to be sent

infile = 'random_hashes_seed10000.txt'
with open(infile) as f:
    lines = [ line.strip() for line in f.readlines() ]

next_hashes = lines[n_hashes_used:(n_hashes_used+N)]

old_to_new_userids = { o:n for o,n in zip(userids,next_hashes) }

print("old_to_new_userids dictionary:")
print(old_to_new_userids)

# 2c - Save old_to_new_userids dictionary

output_str = ''
for old_id in userids:
    new_id = old_to_new_userids[old_id]
    output_str += str(old_id)+','+str(new_id)+'\n'

outfile = 'old_to_new_userids.csv'
with open(outfile,'a') as f:
    f.write(s)

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

email_message = """Dear Participant, 

Thank you again for participating in our study on public opinion. We very much appreciate your time!

Today is the time to complete the second session of our study (5-10 minutes long). Please follow the link below to do so:

https://surveys.oii.ox.ac.uk/?id={}

Once you complete this second session you will receive your £5 Amazon Voucher. 

Once again thank you for your time and participation. 

Myrto Pantazi (on behalf of the research team), 

Oxford Internet Institute
41 St Giles’, OX1 3LW
University tel: 01865 287210
University email: oxlab@oii.ox.ac.uk"""

for userid,email in zip(userids,emails):
    userid2 = str(old_to_new_userids[userid])
    print 'Send email to '+userid+' at email '+email+' with link containing '+userid2

print('Sending email to '+email_to)

email_text = email_message.format(userid2)
msg = MIMEText(email_text)
msg['To']      = email_to
msg['From']    = "oxlab@oii.ox.ac.uk" 
msg['Subject'] = "Public opinion study - second session"

s = smtplib.SMTP("smtp.ox.ac.uk")
s.sendmail(email_from, email_to, msg.as_string())
s.quit()

print('Email sent')

