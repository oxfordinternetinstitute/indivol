# -*- coding: UTF-8 -*-

from auth import Auth
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

#---------------------------------------#
#
# 1 - Take the userids of all the users 
#     who filled the 2nd wave of the form
#
#---------------------------------------#


# prepare query string
mySql_insert_query  = "SELECT DISTINCT userid FROM logging WHERE (userid!='e3cyu6jgUxtMy8T7i5fQ') AND (section LIKE 'questions_personality_wave2_% );"

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

users_who_completed = list(result)


# prepare next query string
mySql_insert_query  = "SELECT userid,payload FROM logging WHERE (userid!='e3cyu6jgUxtMy8T7i5fQ') AND (section='email_wave1') and (payload!='');"

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

users = {}
for i in result:
    user  = i[0]
    email = i[1]
    if user in users_who_completed:
        print('users[{}] = {}'.format(user,email))
        users[user] = email

userids = []
emails  = []
for i,j in users.items():
    userids += [ str(i) ]
    emails  += [ str(j) ]

N = len(users)

#---------------------------------------#
#
# 2 - Load voucher links
#
#---------------------------------------#

with open('voucherlinks.txt') as f:
    voucherlinks = [ line[:-1] for l in f.readlines ]

userid2voucherlink = { u:l for u,l in zip(userids, voucherlinks) ]

#---------------------------------------#
#
# 3 - Prepare emails and send them
#
#---------------------------------------#

import smtplib
from email.mime.text import MIMEText

email_message = """Dear Participant, 

Thank you again for participating in our study on public opinion. We very much appreciate your time!

As promised, here's the £5 Amazon Voucher:
{}

Once again thank you for your time and participation. 

Myrto Pantazi (on behalf of the research team),
Oxford Internet Institute"""

s = smtplib.SMTP("smtp.ox.ac.uk")
email_from = "oxlab@oii.ox.ac.uk" 

for userid,email_to in zip(userids,emails):
    voucherlink = str(userid2voucherlink[userid])
    print 'Sending email to '+userid+' at email '+email_to+' with voucherlink '+voucherlink

    email_text = email_message.format(userid2)
    msg = MIMEText(email_text, 'plain', 'utf-8')
    msg['To']      = email_to
    msg['From']    = email_from
    msg['Subject'] = "Public opinion study - link to voucher"
    s.sendmail(email_from, email_to, msg.as_string())

    print("Email sent")

s.quit()


