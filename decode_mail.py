import imaplib
import email
from constant import user_name, password, host


def login(user, pswd, outlook):

    server = imaplib.IMAP4_SSL(outlook)
    server.login(user, pswd)
    server.select(mailbox='INBOX', readonly=False)
    status, messages = server.search(None, '1:10')
    for msg in messages[0].split():
        status, msg_data = server.fetch(msg, '(RFC822)')
        raw_mail = msg_data[0][1]
        email_msg = email.message_from_bytes(raw_mail)
        if email_msg.is_multipart():
            for part in email_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        print(body.strip())
                except Exception as e:
                    print("Error while decorating content", str(e))
        else:
            body = email_msg.get_payload(decode=True).decode()
            print(body.strip())

if __name__ == "__main__":
    login(user_name, password, host)
