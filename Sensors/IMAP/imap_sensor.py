import imaplib
import email
import time
from itertools import chain

def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))
    # Produce search string in IMAP format:
    # e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)

def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
     return msg.get_payload()

def open_connection(verbose):
    # Stablish configuration parameters
    username = "servidorimap@mailserver.asr"
    password = "123456"
    hostname = "10.10.10.3"

    # Connect to the server
    if verbose: print('Connecting to', hostname)
    connection = imaplib.IMAP4(hostname)

    # Login to our account
    username = username
    password = password
    if verbose: print('Logging in as', username)
    connection.login(username, password)
    return connection


if __name__ == '__main__':
    conn = open_connection(verbose=False)
    try:
        print(conn)

        # Restrict mail search. Be very specific.
        # Machine should be very selective to receive messages.
        criteria = {
            'FROM': 'administrador@mailserver.asr'#,
            #'SUBJECT': 'Correo de prueba del equipo # del grupo 4CM1',
            #'BODY': 'Eric Alejandro Lopez Ayala\nJoel Lopez Romero',
        }

        #We stablish the max uid from mailbox
        uid_max = 0

        #We select the objects that are ar inbox
        conn.select('INBOX')
        result, data = conn.uid('search', None, search_string(uid_max, criteria))

        uids = [int(s) for s in data[0].split()]
        if uids:
            uid_max = max(uids)
        # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

        #print(uids)
        #print(uid_max)

        #We close the connection
        conn.logout()

        # Keep checking messages ...
        while True:
            start = time.time()
            end = 0
            # Have to login/logout each time because that's the only way to get fresh results.
            conn = open_connection(verbose=False)
            conn.select('INBOX')

            result, data = conn.uid('search', None, search_string(uid_max, criteria))

            uids = [int(s) for s in data[0].split()]

            for uid in uids:
                # Have to check again in case the UID criterion is not obeyed
                if uid > uid_max:
                    result, data = conn.uid('fetch', str(uid), '(RFC822)')  # Fetch entire message
                    msg = email.message_from_string(str(data[0][1], encoding="utf-8"))

                    uid_max = uid
                    #print(uid_max)

                    text = get_first_text_block(msg)
                    print('New message :::::::::::::::::::::')
                    print(text)
                    end = time.time()
                    print("IMAP response time took: (%.8f seconds passed): " % (end - start))
            conn.logout()
            time.sleep(1)
    finally:
        conn.logout()