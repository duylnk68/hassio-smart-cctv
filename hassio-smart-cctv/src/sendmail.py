import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

class Email:
    _smtp_host = None
    _smtp_port = None
    _smtp_timeout = 10
    _smtp_tls = False
    _smtp_user = None
    _smtp_pass = None

    def __init__(self, host, port, tls, user, pwd):
        self._smtp_host = host
        self._smtp_port = port
        self._smtp_tls = tls
        self._smtp_user = user
        self._smtp_pass = pwd

    def SendEmail(self, to, subject, body, attachments):
        # Create instance of MIMEMultipart 
        msg = MIMEMultipart() 

        # Set the senders email address   
        msg['From'] = self._smtp_user 
  
        # Set the receivers email address  
        msg['To'] = ','.join(to)

        # Set subject  
        msg['Subject'] = subject

        # Attach the body to the msg instance 
        msg.attach(MIMEText(body, 'plain')) 

        # Attach binary attachments
        for key, value in attachments:
            # Create instance of MIMEBase and named as attachment 
            attachment = MIMEBase('application', 'octet-stream')

            # Set payload
            attachment.set_payload(value)

            # encode into base64 
            encoders.encode_base64(attachment)

            # Set header (attachment name)
            attachment.add_header('Content-Disposition', "attachment; filename= %s" % key)

            # attach the instance 'p' to instance 'msg' 
            msg.attach(attachment)

        # creates SMTP session 
        smtp = smtplib.SMTP(self._smtp_host, self._smtp_port)

        # Start TLS?
        if self._smtp_tls is True:
            smtp.starttls()

        # Authentication 
        smtp.login(self._smtp_user, self._smtp_pass) 

        # sending the mail 
        smtp.sendmail(self._smtp_user, to, msg.as_string()) 

        # Terminating the session
        smtp.quit()
