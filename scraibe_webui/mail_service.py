import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MAIL_SETUP:
    def __init__(self,
                 sender_email : str,
                 smtp_server : str, 
                 smtp_port : int = 0,
                 sender_password : str = None,
                 context_kwargs : dict = {}):
        """ Class to setup Mail Server.
        
        Args:
            sender_email (str): The email address of the sender.
            smtp_server (str): The SMTP server.
            smtp_port (int, optional): The SMTP port. Defaults to 0.
            sender_password (str, optional): The password of the sender. Defaults to None.
            context_kwargs (dict, optional): The context keyword arguments. Defaults to {}.
        """
        
        self.sender_email = sender_email
        self.password = sender_password
        
        self.context = ssl.create_default_context(**context_kwargs)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        
        self.mailserver = self.setup_mailserver()
        
    def setup_message(self, subject : str,
                      receiver_email : str,
                      message : str):
        """Setup the mail message.
        
        Args:
            subject (str): The subject of the mail.
            receiver_email (str): The email address of the receiver.
            message (str): The message of the mail.
            
        Returns:
            MIMEMultipart: The mail message.
        """
        
        _message = MIMEMultipart()
        _message["From"] = self.sender_email
        _message["To"] = receiver_email
        _message["Subject"] = subject
        _message.attach(MIMEText(message, "plain"))
        
        return _message
    
    def test_login(self) -> bool:
        """Test if login is possible.
        
        Returns:
            bool: True if login is successful, False otherwise.
        """
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=self.context)
                server.login(self.sender_email, self.password)
            return True
        except smtplib.SMTPNotSupportedError:
            Warning("SMTP AUTH extension not supported by server. Try without login.")
            return False
    
    def setup_mailserver(self) -> smtplib.SMTP:
        """Setup the mail server.	
        
        Returns:
            smtplib.SMTP: The mail server.
        """
        
        if self.password is not None:
            
            login = self.test_login()
            
        else:
            login = False
        
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        
        if login:
            server.starttls(context=self.context)
            server.login(self.sender_email, self.password)
        else:
          Warning("TLS and/or login failed. Try without TLS and/or login.")
        
        return server   
    
    def close_mailserver(self) -> None:
        """Close the mail server."""
        
        self.mailserver.quit()
        
        self.mailserver = None
        
    def send_mail(self, receiver_email : str,
                  subject : str,
                  message : str) -> None:
        """Send a mail.
        
        Args:
            receiver_email (str): The email address of the receiver.
            subject (str): The subject of the mail.
            message (str): The message of the mail.
        """
        
        _message = self.setup_message(subject, receiver_email, message)
        
        if self.mailserver is None:
            # Reconnect to the mail server if it is not connected.
            self.mailserver = self.setup_mailserver()
        
        self.mailserver.sendmail(self.sender_email, receiver_email, _message.as_string())

if __name__ == "__main__":
    port = 0 # For SSL
    smtp_server = "smtp.leipzig.dbfz.de"
    sender_email = "scraibe@dbfz.de"
    
    mailer = MAIL_SETUP(sender_email, smtp_server, port)
    
    mailer.send_mail("Jacob.Schmieder@dbfz.de", "Test", "Test")
    