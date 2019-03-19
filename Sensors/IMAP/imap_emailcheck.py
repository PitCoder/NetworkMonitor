import time
from itertools import  chain
import email
import imaplib

#Code extracted from: https://gist.github.com/nickoala/569a9d191d088d82a5ef5c03c0690a02#file-2_sendattach-py-L22

imap_ssl_host = "imap.gmail.com" #Also can be imap.mail.yahoo.com
imap_ssl_port = 993

username = "overlord.lae@gmail.com"
password = "EALAS3KOQ"

#Restrict mail search. So it must be very specific
criteria = {
    "FROM": "overlord.lae@gmail.com",
    "SUBJECT": "SMTP TESTING",
    "BODY": "This is a SMTP testing...",
}

uid_max = 0

def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_max + 1))]
    return '(%s)' % ' '.join(chain(*c))
    # Produce search string in IMAP format:
    #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" UID 9999:*)


def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()


server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
server.login(username, password)
server.select("INBOX")

result, data = server.uid('search', None, search_string(uid_max, criteria))

uids = [int(s) for s in data[0].split()]
if uids:
    uid_max = max(uids)
    # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

print(data)

server.logout()

# Keep checking messages ...
while 1:
    # Have to login/logout each time because that's the only way to get fresh results.
    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(username, password)
    server.select('INBOX')

    result, data = server.uid('search', None, search_string(uid_max, criteria))
    uids = [int(s) for s in data[0].split()]
    print(uids)

    for uid in uids:
        print(uid)
        print(uid_max)
        # Have to check again because Gmail sometimes does not obey UID criterion.
        if uid > uid_max:
            result_fetch, data_fetch = server.uid('fetch', str(uid), '(RFC822)')  # fetch entire message
            #print(data_fetch)
            #print(str(data_fetch, encoding="UTF-8"))
            msg = email.message_from_bytes(data_fetch[0][1])
            #msg = email.message_from_string()

            uid_max = uid

            text = get_first_text_block(msg)
            print('New message :::::::::::::::::::::')
            print(text)

    server.logout()
    time.sleep(1)