import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from interactions import run_scraibe

class MailService:
    def __init__(self,
                 sender_email : str,
                 smtp_server : str, 
                 smtp_port : int = 0,
                 sender_password : str = None,
                 context_kwargs : dict = {},
                 default_subject : str = "SCRAIBE"):
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
        
        self.default_subject = default_subject
        
        self.context = ssl.create_default_context(**context_kwargs)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        
        self.mailserver = self.setup_mailserver()
        
    def setup_message(self, subject : str,
                      receiver_email : str,
                      message : str,
                      received_text_file: str,
                      only_txt: bool=False):
        """Setup the mail message.
        
        Args:
            subject (str): The subject of the mail.
            receiver_email (str): The email address of the receiver.
            message (str): The message of the mail.
            
        Returns:
            MIMEMultipart: The mail message.
        """
        text_file = received_text_file



        html = f"""\ 
       <html>
        <body>
         <p>Thank you for using ScrAIbe.<br>
       Here is your transcripted audio file:<br>
          <br><br><h1> {message} </h1><br>
         </p>
       </body>
      </html>"""

        with open(text_file, "w") as file:
           file.write(message)


        
         
         
        _message = MIMEMultipart("alternative")
        _message["From"] = self.sender_email
        _message["To"] = receiver_email
        
        _message["Subject"] = self.default_subject + " - " + subject

        
        with open(text_file, "r") as file:
            attachment = MIMEText(file.read())
            attachment.add_header('Content_Disposition', 'attachment', filename=text_file)
            _message.attach(attachment)


        if only_txt == False:
           _message.attach(MIMEText(str(message), "plain"))
           _message.attach(MIMEText(html, 'html'))
        
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
                  message : str,
                  received_text_file: str,
                  only_txt: bool=False) -> None:
        """Send a mail.
        
        Args:   
            receiver_email (str): The email address of the receiver.
            subject (str): The subject of the mail.
            message (str): The message of the mail.
        """
        
        _message = self.setup_message(subject, receiver_email, message, received_text_file, only_txt)
        
        if self.mailserver is None:
            # Reconnect to the mail server if it is not connected.
            self.mailserver = self.setup_mailserver()
        
        self.mailserver.sendmail(self.sender_email, receiver_email, _message.as_string())


    def setup_default_message(self,
                                       receiver_email: str,
                                       positive_negativ: True,
                                       Exception: Exception):
        """ Sets up a default Message which can be positive or negative based on the input
         Args:
             receiver_email(str): The email address of the receiver
             positive_negativ (bool):  Decider for a positive or negativ default message, True for positive Message, False for negative Message
             Exception(class): Exception"""
        subject1 = 'ScrAIbe failed'
        subject2 = 'Your transcripted audio file was successfully send!'
        message1 = 'ScrAIbe got succesfully initiated, your audio file is now being processed.'
        message2 = 'E-Mail has not been sent, your audio file needs to be sent again. If the problem persists, please contact us.'
        html1 = f"""\ 
       <html>
        <body>
         <p>Thank you for using ScrAIbe.<br>
       <br>
          <br><br><h1> {message1} </h1><br>
         </p>
       </body>
      </html>"""
        
        html2 = f"""\ 
       <html>
        <body>
         <p>Thank you for using ScrAIbe.<br>
       <br>
          <br><br><h1> {message2}{Exception}  </h1><br>
         </p>
       </body>
      </html>"""
       
        _message = MIMEMultipart("alternative")
        _message["From"] = self.sender_email
        _message["To"] = receiver_email
        if positive_negativ == True:
         _message["Subject"] = self.default_subject + " - " + subject1
         _message.attach(MIMEText(str(message1), "plain"))
         _message.attach(MIMEText(html1, 'html'))
        else:
         _message["Subject"] = self.default_subject + " - " + subject2
         _message.attach(MIMEText(str(message2), "plain"))
         _message.attach(MIMEText(html2, 'html'))   
        return _message
            

    def scraibe_done(self, receiver_email : str,
                     positive_negativ=True,
                        ) -> None:      
        """ Sends a Mail for a successfull initiation of ScrAIbe.

         Args: 
            receiver_email (str): The email address of the receiver.
            positive_negativ(bool): Decider for a positive or negativ default message, True for positive Message, False for negative Message """
        done_message = self.setup_default_message(receiver_email, positive_negativ)    
        if self.mailserver is None:
            # Reconnect to the mail server if it is not connected.
            self.mailserver = self.setup_mailserver()
        self.mailserver.sendmail(self.sender_email, receiver_email, done_message.as_string())


    def scraibe_failed(self, receiver_email : str,
                       Exception: Exception,
                       positive_negativ=False,
                       ) -> None:       
        """ Sends a Mail for a failed initiation of ScrAIbe.

         Args: 
            receiver_email (str): The email address of the receiver.
            positive_negativ (bool): Decider for a positive or negativ default message, True for positive Message, False for negative Message
            Exception(class): Exception """
        failed_message = self.setup_default_message(receiver_email, positive_negativ, Exception)       
        if self.mailserver is None:
            # Reconnect to the mail server if it is not connected.
            self.mailserver = self.setup_mailserver()
      
        self.mailserver.sendmail(self.sender_email, receiver_email, failed_message.as_string())    
            

        

        


        
              
    
    @classmethod
    def from_config(cls, config : dict):
        """Create a MAIL_SETUP object from a configuration dictionary.
        
        Args:
            config (dict): The configuration dictionary.
            
        Returns:
            MAIL_SETUP: The MAIL_SETUP object.
        """
        
        return cls(sender_email = config['sender_email'],
                   smtp_server = config['smtp_server'],
                   smtp_port = config['smtp_port'],
                   sender_password = config['sender_password'],
                   context_kwargs = config['context_kwargs'],
                   default_subject = config['default_subject'])
    
    
    


    
    def __repr__(self) -> str:
        """Representation of the object.
        
        Returns:
            str: The representation of the object.
        """
        
        return f"MailService(sender_email = {self.sender_email}, smtp_server = {self.smtp_server}, smtp_port = {self.smtp_port}, default_subject = {self.default_subject})"
