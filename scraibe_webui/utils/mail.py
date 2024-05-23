import ssl
import smtplib
from typing import Union
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class MailService:
    def __init__(self,
                 sender_email: str,
                 smtp_server: str, 
                 smtp_port: int = 0,
                 sender_password: str = None,
                 context_kwargs: dict = {},
                 default_subject: str = "SCRAIBE",
                 success_template: str = None,
                 error_template: str = None,
                 final_template: str = None,
                 css_template_path: str = None,) -> None:
        """Class to setup Mail Server.

        Args:
            sender_email (str): The email address of the sender.
            smtp_server (str): The SMTP server.
            smtp_port (int, optional): The SMTP port. Defaults to 0.
            sender_password (str, optional): The password of the sender. Defaults to None.
            context_kwargs (dict, optional): The context keyword arguments. Defaults to {}.
            default_subject (str, optional): The default subject for emails. Defaults to "SCRAIBE".
            success_template (str, optional): The HTML template for success upload notification. Defaults to None.
            error_template (str, optional): The HTML template for error notification. Defaults to None.
            final_template (str, optional): The HTML template for final product notification. Defaults to None.
            css_template_path (str, optional): The path to the CSS template. Defaults to None.
            args: Additional arguments. Herte only used to aviod to many arguments.
            kwargs: Additional keyword arguments. Herte only used to aviod to many arguments.
        """
        
        self.sender_email = sender_email
        self.password = sender_password
        self.default_subject = default_subject
        self.context = ssl.create_default_context(**context_kwargs)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.success_template = success_template
        self.error_template = error_template
        self.final_template = final_template
        self.css_template_path = css_template_path
        self.mailserver = self.setup_mailserver()
        
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
    
    def setup_message(self, subject: str, receiver_email: str, message: str, text_type: str, attachments: list = []) -> MIMEMultipart:
        """Setup the mail message with optional attachments.

        Args:
            subject (str): The subject of the mail.
            receiver_email (str): The email address of the receiver.
            message (str): The message of the mail.
            attachments (list, optional): List of file paths to attach. Defaults to [].
            text_type (str): The text type of the message.

        Returns:
            MIMEMultipart: The mail message.
        """
        _message = MIMEMultipart("alternative")
        _message["From"] = self.sender_email
        _message["To"] = receiver_email
        _message["Subject"] = self.default_subject + " - " + subject

        # _message.attach(MIMEText(message, text_type))
        _message.attach(MIMEText(message, 'html'))

        for file_path in attachments:
            
            with open(file_path, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {file_path.split('/')[-1]}")
                _message.attach(part)

        return _message
    
    def send_mail(self, receiver_email: str, subject: str, message: str, attachments: list = [], text_type: str ='html') -> None:
        """Send a mail with optional attachments.

        Args:   
            receiver_email (str): The email address of the receiver.
            subject (str): The subject of the mail.
            message (str): The message of the mail.
            attachments (list, optional): List of file paths to attach. Defaults to [].
            text_type (str, optional): The text type of the message. Defaults to 'html'.
        """
        
        _message = self.setup_message(subject, receiver_email, message, text_type, attachments)
        
        if self.mailserver is None:
            # Reconnect to the mail server if it is not connected.
            self.mailserver = self.setup_mailserver()
        
        self.mailserver.sendmail(self.sender_email, receiver_email, _message.as_string())
    
    def send_success_upload_notification(self, receiver_email: str, **format_options) -> None:
        """Send a success upload notification email.

        Args:
            receiver_email (str): The email address of the receiver.
            queue_position (int): The position in the processing queue.
            format_options (dict): The format options for the email. default is the queue_position.
        """
        message = self.success_template.format(css_path=self.css_template_path, **format_options)
        self.send_mail(receiver_email, "Upload Successful", message)

    def send_error_notification(self, receiver_email: str, exception_message, **format_options ) -> None:
        """Send an error notification email.

        Args:
            receiver_email (str): The email address of the receiver.
            exception_message (str): The exception message to include in the email.
            format_options (dict): The format options for the email.
        """
    
        message = self.error_template.format(css_path=self.css_template_path, exception=exception_message, **format_options)
        self.send_mail(receiver_email, "Error Notification", message)
    
    def send_transcript(self, receiver_email: str, transcript_path: Union[str,list] = [], **format_options ) -> None:
        """Send a final product notification email with transcript attachment.

        Args:
            receiver_email (str): The email address of the receiver.
            transcript_path (Union[str, list], optional): Path to the transcript file or list of paths to attach.
            format_options (dict): The format options for the transcript. can be used to format the final template.
        """
        if isinstance(transcript_path, str):
            transcript_path = [transcript_path]
            
        message = self.final_template.format(css_path=self.css_template_path, **format_options)
        self.send_mail(receiver_email, "Transcript Ready", message, transcript_path)
    
    @classmethod
    def from_config(cls, config: dict):
        """Create a MailService object from a configuration dictionary.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            MailService: The MailService object.
        """
        
        return cls(sender_email=config['sender_email'],
                   smtp_server=config['smtp_server'],
                   smtp_port=config['smtp_port'],
                   sender_password=config['sender_password'],
                   context_kwargs=config['context_kwargs'],
                   default_subject=config['default_subject'],
                   success_template=config.get('success_template'),
                   error_template=config.get('error_template'),
                   final_template=config.get('final_template'))

    def __repr__(self) -> str:
        """Representation of the object.

        Returns:
            str: The representation of the object.
        """
        
        return f"MailService(sender_email={self.sender_email}, smtp_server={self.smtp_server}, smtp_port={self.smtp_port}, default_subject={self.default_subject})"

if __name__ == '__main__':
    
    from os.path import dirname, realpath
    
    ROOT_PATH = dirname(realpath(__file__)).split('scraibe_webui')[0]
    reciever = 'test@example.com'
    
    css_path = ROOT_PATH + 'scraibe_webui/misc/mail_style.css'
    
    # Example usage
    with open(ROOT_PATH +'scraibe_webui/misc/upload_notification_template.html', 'r') as file:
        upload_html_template = file.read()


    # Define the dynamic content
    queue_position = 5  # Example queue position
    contact_email = "example@support.com"

    # Format the HTML template with the dynamic content
    uplaod_html_content = upload_html_template.format(css_path=css_path,queue_position=queue_position, contact_email=contact_email)


    ## Error Notification
    with open(ROOT_PATH +'scraibe_webui/misc/error_notification_template.html', 'r') as file:
        error_html_template = file.read()
    
    error_html_template = error_html_template.format(css_path=css_path,contact_email=contact_email, exception = 'My Test Exception')
    
    
    # final product
    
    with open(ROOT_PATH +'scraibe_webui/misc/success_template.html', 'r') as file:
        final_html_template = file.read()

    # Format the HTML template with the dynamic content
    final_html_content = final_html_template.format(css_path=css_path,contact_email=contact_email)
    
    # Create example "Hello World" text files TODO: make them Temporary files
    
    file1_path = "hello1.txt"
    file2_path = "hello2.txt"
    with open(file1_path, "w") as f:
        f.write("Hello World from file 1!")
    with open(file2_path, "w") as f:
        f.write("Hello World from file 2!")
    attachments = [file1_path, file2_path]
    
    mail_service = MailService(sender_email = "scraibe@example.de",
                                 smtp_server = "my.smtp.server",
                                 success_template=upload_html_template,
                                 error_template=error_html_template,
                                 final_template=final_html_template)
    
    
    mail_service.send_success_upload_notification(receiver_email=reciever, queue_position=queue_position, contact_email=contact_email)
    mail_service.send_error_notification(receiver_email=reciever, exception_message='My Test Exception')
    mail_service.send_transcript(receiver_email=reciever, contact_email=contact_email, transcript_path= attachments)