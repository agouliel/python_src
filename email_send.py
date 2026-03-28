import smtplib
from email.mime.text import MIMEText

sender = 'alex@goulielmos.org'  # your sending address
recipients = 'bracts.teacups-09@icloud.com'  # comma separated list of recipients
msg = MIMEText("""Hello""")

msg['Subject'] = 'Test email'
msg['From'] = sender
msg['To'] = recipients.replace(',', ';')

s = smtplib.SMTP('localhost', 1587)
s.sendmail(sender, recipients.split(','), msg.as_string())
s.quit()

