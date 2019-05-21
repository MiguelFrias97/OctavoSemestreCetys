import email
import imaplib
import os
import subprocess
import time


class FetchEmail():

    connection = None
    error = None

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False) # so we can mark mails as read

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()

    def save_attachment(self, msg, download_folder):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)

        return: file path to attachment
        """
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            att_path = os.path.join(download_folder, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        return att_path

    def fetch_unread_messages(self):
        """
        Retrieve unread messages
        """
        emails = []
        (result, messages) = self.connection.search(None, 'UnSeen')
        if result == "OK":
            for message in messages[0].split(' '):
                try:
                    ret, data = self.connection.fetch(message,'(RFC822)')
                except:
                    #print ("No new emails to read.")
                    self.close_connection()
                    exit()

                msg = email.message_from_string(data[0][1])
                if isinstance(msg, str) == False:
                    emails.append(msg)
                response, data = self.connection.store(message, '+FLAGS','\\Seen')

            return emails

if __name__=="__main__":
    mail = FetchEmail('imap.gmail.com','seguridad.potencia.ice@gmail.com','ElectronicaPotencia')
    mails = mail.fetch_unread_messages()
    print(mails)

    responses = {}
    index = 1
    for m in mails:
	r = []
	if m.is_multipart():
	    for payload in m.get_payload():
		r.append(payload.get_payload())
	else:
	    r.append(payload.get_payload())
	responses['correo'+str(index)] = r
	index += 1

    for key in responses:
	body = responses[key][0]
	print(body)

