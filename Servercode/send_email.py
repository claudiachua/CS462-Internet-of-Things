import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'amos.lee.2016@sis.smu.edu.sg'
PASSWORD = 'QHJtYTk0U211ODk='

from postgresCRUD import *

import os
current_time = datetime.now()
heartbeat_delta= timedelta(hours=1)

def check_email_validity():
    f = open("emailfile.txt","r")
    line = f.read().strip('\n\r')
    f.close()
    if not line:
        return True
    line_list = line.split(",")
    status = line_list[0]
    time_sent = line_list[1]
    print(time_sent)
    time_sent_datetime = datetime.datetime.strptime(time_sent,'%m/%d/%y %H:%M:%S')
    return status!="sent" or ((current_time + timedelta(hours=8) - time_sent_datetime) >= heartbeat_delta)

def send_motion_email(status,timestamp):
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    to_address = ['randylai.2016@sis.smu.edu.sg', 'chijao.foo.2016@sis.smu.edu.sg', 'amos.lee.2016@sis.smu.edu.sg','yankai.ong.2016@sis.smu.edu.sg']

    name = 'Alert'

    msg = MIMEMultipart()       # create a message

    message = "Hi this happened to your motion sensor Sir" + status + " @ " + timestamp

    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=to_address
    msg['Subject']="Hi something happened!"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()
def decoder():

    message = base64.b64decode(PASSWORD.encode('ascii')).decode('ascii')

    return(message)


def send_email(id,timestamp):
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, decoder())  
    to_address = ['randylai.2016@sis.smu.edu.sg', 'chijao.foo.2016@sis.smu.edu.sg', 'Darren.gan.2017@sis.smu.edu.sg','amos.lee.2016@sis.smu.edu.sg','yankai.ong.2016@sis.smu.edu.sg']
    #to_address = ['amos.lee.2016@sis.smu.edu.sg']
    name = 'Alert'

    msg = MIMEMultipart()       # create a message

    message = "Hi we have an alert for " + id + " @ " + str(timestamp)
    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=",".join(to_address)
    msg['Subject']="Alert for IOT deployed at Robinson 77"

    if 'E' in id:
        place = 'Meeting Room'
    else:
        place = 'Hotdesk'

    f=open("email_template.html", "r")
    if f.mode == 'r':
        contents =f.read()
        contents = contents.replace("[place]", place)
        contents = contents.replace('[id]', id)
        contents = contents.replace('[time]', str(timestamp))
    # add in the message body

    msg.attach(MIMEText(contents, 'html'))

    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,to_address,msg.as_string())
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()

    hb_records = get_hb_status()

is_problem_list = []

for record in hb_records:
    id = record[0]
    timestamp = record[1]
    #timestamp_timedelta = datetime.datetime.strptime(timestamp,'%m/%d/%y %H:%M:%S')
    if (current_time + timedelta(hours=8) - timestamp) >=  heartbeat_delta:
        is_problem_list.append((id,timestamp))

if is_problem_list and check_email_validity():
    print("there is a problem")
    for item in is_problem_list:
        send_email(item[0],item[1])

    f = open("emailfile.txt","w")
    f.write("sent," + str(current_time))
    f.close()