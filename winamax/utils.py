import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from . import config
def get_last_n_lines(file_name, N):
    # Create an empty list to keep the track of last N lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location -1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches N, then return the reversed list
                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)
        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])
    # return the reversed list
    return list(list_of_lines)

def send_mail(subject, body, mode):
    port = 465 
    
    # Create a secure SSL context
    sender_email = config.smtp_sender_email
    attr = f"receiver_email_{mode}"
    if hasattr(config, attr):
        receivers_email = getattr(config, attr)
    else:
        raise(Exception(f"mail: Unknown mode: {mode}"))

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receivers_email

    part1 = MIMEText(body, "html")
    message.attach(part1)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(config.smtp_server, port, context=context) as server:
        server.login(config.smtp_api_key, config.smtp_api_secret)
        server.sendmail(
            sender_email, receivers_email.split(","), message.as_string()
        )
   