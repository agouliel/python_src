import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

me = "postman@ionia.gr"
you = "it.goulielmos@ioniaman.gr"

msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = me
msg['To'] = you

text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)

s = smtplib.SMTP('192.168.0.197')
s.sendmail(me, you, msg.as_string())
s.quit()
