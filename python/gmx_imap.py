#!/usr/bin/env python
#
# Very basic example of using Python 3 and IMAP to iterate over emails in a
# gmx folder/label.  This code is released into the public domain.
#
# This script is example code from this blog post:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
# This is an updated version of the original -- modified to work with Python 3.6.
#
import sys
import imaplib
import getpass
import email
import email.header
import datetime


EMAIL_ACCOUNT = "yourname@gmx.us"

# Use 'INBOX' to read inbox.  Note that whatever folder is specified, 
# after successfully running this script all emails in that folder 
# will be marked as read.
EMAIL_FOLDER = "inbox"


def process_mailbox(M, filter='All'):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """

    # rv, data = M.search(None, "ALL")
    rv, data = M.search(None, filter)
    # 查找从support@alidage.org发来的邮件
    # rv, data = M.search(None, "(From support@alidage.org)")

    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
        print('Message %s: %s' % (num, subject))
        print('Raw Date:', msg['Date'])
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print ("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))

        processMsg(data)


def move_to_trash_before_date(m, folder, days_before):
    '''
     deleting emails before days
    :param m:
    :param folder:
    :param days_before:
    :return:
    '''
    no_of_msgs = int(m.select(folder)[1][0])  # required to perform search, m.list() for all lables, '[Gmail]/Sent Mail'
    print("- Found a total of {1} messages in '{0}'.".format(folder, no_of_msgs))

    before_date = (datetime.date.today() - datetime.timedelta(days_before)).strftime("%d-%b-%Y")  # date string, 04-Jan-2013
    typ, data = m.search(None, '(BEFORE {0})'.format(before_date))  # search pointer for msgs before before_date

    if data != ['']:  # if not empty list means messages exist
        no_msgs_del = data[0].split()[-1].decode("utf-8")  # last msg id in the list
        print("- Marked {0} messages for removal with dates before {1} in '{2}'.".format(no_msgs_del, before_date, folder))
        # m.store("1:{0}".format(no_msgs_del), '+X-GM-LABELS', '\\Trash')  # move to trash
        m.store("1:{0}".format(no_msgs_del), '+FLAGS', '\\Deleted')  # move to trash
        # print("Deleted {0} messages.".format(no_msgs_del))
        m.expunge()
    else:
        print("- Nothing to remove.")

    return

def processMsg(data):
    # 查找邮件正文
    for m in data[0][1].decode("utf-8").split(':'):
        if m.find("用户名：") > 0:
            print(m, m.find("用户名："))
            break


imap = imaplib.IMAP4_SSL('imap.gmx.com')

try:
    rv, data = imap.login(EMAIL_ACCOUNT, getpass.getpass())
except imaplib.IMAP4.error:
    print ("LOGIN FAILED!!! ")
    sys.exit(1)

print(rv, data)

rv, mailboxes = imap.list()
if rv == 'OK':
    print("Mailboxes:")
    print(mailboxes)

# 
rv, data = imap.select(EMAIL_FOLDER)
if rv == 'OK':
    print("Processing mailbox...\n")
    process_mailbox(imap)
    imap.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

imap.logout()

