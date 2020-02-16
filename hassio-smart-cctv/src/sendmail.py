import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import threading
import queue

class Email(threading.Thread):
    class _Message:
        To = None
        Subject = None
        Body = None
        Attachments = None

        def __init__(self, to, subject, body, attachments):
            self.To = to
            self.Subject = subject
            self.Body = body
            self.Attachments = attachments

    # Declare class member
    _smtp_host = None
    _smtp_port = None
    _smtp_timeout = 10
    _smtp_tls = False
    _smtp_user = None
    _smtp_pass = None
    _event = threading.Event()
    _keep_running = True
    _queue = queue.Queue()

    # Constructor
    def __init__(self, host, port, tls, user, pwd):
        threading.Thread.__init__(self)
        self._smtp_host = host
        self._smtp_port = port
        self._smtp_tls = tls
        self._smtp_user = user
        self._smtp_pass = pwd

    def run(self):
        while self._keep_running:
            # Wait!
            if self._queue.empty():
                self._event.wait(1)
                continue
            
            # Send mail!
            self._SendEmail(self._queue.get())

    def SendMail(self, to, subject, body, attachments):
        _message = Email._Message(to, subject, body, attachments)
        self._queue.put(_message)

    def _SendEmail(self, _message : _Message):
        # Create instance of MIMEMultipart 
        msg = MIMEMultipart() 

        # Set the senders email address   
        msg['From'] = self._smtp_user 
  
        # Set the receivers email address  
        msg['To'] = ','.join(_message.To)

        # Set subject  
        msg['Subject'] = _message.Subject

        # Attach the body to the msg instance 
        msg.attach(MIMEText(_message.Body, 'plain')) 

        # Attach binary attachments
        if _message.Attachments is not None:
            for key, value in _message.Attachments:
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
        smtp.sendmail(self._smtp_user, _message.To, msg.as_string()) 

        # Terminating the session
        smtp.quit()
