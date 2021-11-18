# https://twitter.com/python_engineer/status/1460528063351980034

import smtplib, ssl

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "test@gmail.com" # Less secure apps have to be enabled
receiver_email = "test@icloud.com"
password = ""

message = "Testing"

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
  try:
    server.login(sender_email, password)
    res = server.sendmail(sender_email, receiver_email, message)
    print('email sent')
  except:
    print('error')
