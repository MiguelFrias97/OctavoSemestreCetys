import smtplib
sender = 'seguridad.potencia.ice@gmail.com'
to = ['miguel.frias@cetys.edu.mx']
subject = 'Testing mail'
body = 'I am testing the mail function'

message =  """\
From: %s
To: %s
Subject: %s

%s

""" % (sender,", ".join(to) if len(to)>1 else to[0],subject,body)
server = smtplib.SMTP_SSL('smtp.gmail.com',465)
server.ehlo()
server.login('seguridad.potencia.ice@gmail.com','ElectronicaPotencia')
server.sendmail(sender,to,message)
