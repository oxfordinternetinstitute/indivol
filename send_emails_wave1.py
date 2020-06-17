import cgi

import smtplib
from email.mime.text import MIMEText

form = cgi.FieldStorage()

if (form.has_key("email"):
	print("<p>has email</p>")

    email_to = form["email"].value
	email_from    = "oxlab@oii.ox.ac.uk"
	email_subject = "Public opinion study - First session"
	email_message = """Dear Participant, 

Thank you for completing the first session of our study on public opinion.

As indicated in the survey you just took, this study consists of two sessions (5-10 minutes each). 

In two days, we will e-mail you the link to the second session. 

Once you complete the second session you will receive your £5 Amazon Voucher. 

Once again thank you for your time and participation. 

Myrto Pantazi (on behalf of the research team), 

Oxford Internet Institute
41 St Giles’, OX1 3LW
University tel: 01865 287210
University email: oxlab@oii.ox.ac.uk"""

	msg = MIMEText(email_message)
	msg['Subject'] = email_subject
	msg['From']    = email_from 
	msg['To']      = email_to

	s = smtplib.SMTP("smtp.ox.ac.uk")
	s.sendmail(email_from, email_to, msg.as_string())
	s.quit()

else:
	print("<p>no email</p>")