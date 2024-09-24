import ssl
import smtplib
from typing import Union
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import warnings

class MailService:
    def __init__(self,
                 sender_email: str,
                 smtp_server: str,
                 smtp_port: int = None,
                 sender_password: str = None,
                 context_kwargs: dict = {},
                 default_subject: str = "SCRAIBE",
                 connection_type: str = 'TLS',  # 'SSL', 'TLS', or 'NONE'
                 upload_notification_template: str = None,
                 upload_subject: str = "Upload Successful",
                 error_template: str = None,
                 error_subject: str = "An error occurred during processing.",
                 success_template: str = None,
                 success_subject: str = "Your transcript is ready.",
                 css_template_path: str = None) -> None:
        """
        Initializes the Mail Service class.

        Args:
            sender_email (str): The email address of the sender.
            smtp_server (str): The SMTP server to use for sending emails.
            smtp_port (int, optional): The port to use for the SMTP server.
            sender_password (str, optional): The password for the sender's email account.
            context_kwargs (dict, optional): Keyword arguments for ssl.create_default_context.
            default_subject (str, optional): The default subject line for emails.
            connection_type (str, optional): Connection type: 'SSL', 'TLS', or 'NONE'.
            upload_notification_template (str, optional): HTML template for upload notifications.
            upload_subject (str, optional): Subject line for upload notifications.
            error_template (str, optional): HTML template for error notifications.
            error_subject (str, optional): Subject line for error notifications.
            success_template (str, optional): HTML template for success notifications.
            success_subject (str, optional): Subject line for success notifications.
            css_template_path (str, optional): Path to a CSS file for email styling.

        Returns:
            None
        """

        self.sender_email = sender_email
        self.password = sender_password
        self.default_subject = default_subject
        self.context = ssl.create_default_context(**context_kwargs)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.connection_type = connection_type.upper()

        self.upload_notification_template = upload_notification_template
        self.upload_subject = upload_subject

        self.error_template = error_template
        self.error_subject = error_subject

        self.success_template = success_template
        self.success_subject = success_subject

        self.css_template_path = css_template_path

        # Delay mail server setup until needed
        self.mailserver = None

        # Test the connection and login during initialization
        self.test_login()

    def setup_mailserver(self) -> smtplib.SMTP:
        """Setup the mail server based on the connection type.

        Returns:
            smtplib.SMTP: The configured mail server.
        """
        try:
            if self.connection_type == 'SSL':
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=self.context)
                if self.password:
                    server.login(self.sender_email, self.password)
            elif self.connection_type == 'TLS':
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls(context=self.context)
                if self.password:
                    server.login(self.sender_email, self.password)
            elif self.connection_type == 'NONE':
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                if self.password:
                    server.login(self.sender_email, self.password)
            else:
                raise ValueError(f"Invalid connection_type: {self.connection_type}. Must be 'SSL', 'TLS', or 'NONE'.")

            return server
        except smtplib.SMTPAuthenticationError as e:
            warnings.warn(f"Authentication failed: {e}")
            return None
        except Exception as e:
            warnings.warn(f"An error occurred during SMTP connection: {e}")
            return None

    def send_mail(self, receiver_email: str, subject: str, message: str, attachments: list = None) -> None:
        """Send an email with optional attachments.

        Args:
            receiver_email (str): The receiver's email address.
            subject (str): The email subject.
            message (str): The email body.
            attachments (list, optional): List of file paths to attach.
        """
        _message = self.setup_message(subject, receiver_email, message, attachments)
        if not self.mailserver:
            self.mailserver = self.setup_mailserver()
        self.mailserver.sendmail(self.sender_email, receiver_email, _message.as_string())

    def setup_message(self, subject: str, receiver_email: str, message: str, attachments: list = None) -> MIMEMultipart:
        """Prepare the email message.

        Args:
            subject (str): The email subject.
            receiver_email (str): The receiver's email address.
            message (str): The email body.
            attachments (list, optional): List of file paths to attach.

        Returns:
            MIMEMultipart: The email message object.
        """
        attachments = attachments or []
        _message = MIMEMultipart("alternative")
        _message["From"] = self.sender_email
        _message["To"] = receiver_email
        _message["Subject"] = f"{self.default_subject} - {subject}"
        _message.attach(MIMEText(message, "html"))

        for file_path in attachments:
            with open(file_path, "rb") as file:
                mime_part = MIMEBase("application", "octet-stream")
                mime_part.set_payload(file.read())
                encoders.encode_base64(mime_part)
                mime_part.add_header("Content-Disposition", f"attachment; filename={file_path.split('/')[-1]}")
                _message.attach(mime_part)

        return _message

    def send_upload_notification(self, receiver_email: str, **format_options) -> None:
        """Send an upload notification email.

        Args:
            receiver_email (str): The receiver's email address.
            format_options (dict): Additional formatting options for the email.
        """
        _message = (self.upload_notification_template or "Your upload was successful.").format(
            css_path=self.css_template_path, **format_options
        )
        self.send_mail(receiver_email, self.upload_subject, _message)

    def send_error_notification(self, receiver_email: str, exception_message: str, **format_options) -> None:
        """Send an error notification email.

        Args:
            receiver_email (str): The receiver's email address.
            exception_message (str): The error message to include.
            format_options (dict): Additional formatting options for the email.
        """
        _message = (self.error_template or "An error occurred during processing: {exception}").format(
            css_path=self.css_template_path, exception=exception_message, **format_options
        )
        self.send_mail(receiver_email, self.error_subject, _message)

    def send_transcript(self, receiver_email: str, transcript_paths: Union[str, list] = None, **format_options) -> None:
        """Send a success email with transcript attachments.

        Args:
            receiver_email (str): The receiver's email address.
            transcript_paths (Union[str, list], optional): Paths to transcript files to attach.
            format_options (dict): Additional formatting options for the email.
        """
        if not transcript_paths:
            transcript_paths = []
        elif isinstance(transcript_paths, str):
            transcript_paths = [transcript_paths]

        _message = (self.success_template or "Your transcript is ready.").format(
            css_path=self.css_template_path, **format_options
        )
        self.send_mail(receiver_email, self.success_subject, _message, attachments=transcript_paths)

    @classmethod
    def from_config(cls, config: dict):
        """Initialize the MailService from a configuration dictionary.

        Args:
            config (dict): Configuration parameters.

        Returns:
            MailService: An instance of MailService.
        """
        return cls(
            sender_email=config.get('sender_email'),
            smtp_server=config.get('smtp_server'),
            smtp_port=config.get('smtp_port'),
            sender_password=config.get('sender_password'),
            context_kwargs=config.get('context_kwargs', {}),
            default_subject=config.get('default_subject', "SCRAIBE"),
            connection_type=config.get('connection_type', 'TLS'),
            upload_notification_template=config.get('upload_notification_template'),
            upload_subject=config.get('upload_subject', "Upload Successful"),
            error_template=config.get('error_template'),
            error_subject=config.get('error_subject', "An error occurred during processing."),
            success_template=config.get('success_template'),
            success_subject=config.get('success_subject', "Your transcript is ready."),
            css_template_path=config.get('css_template_path'),
        )

    def __repr__(self) -> str:
        """String representation of the MailService object.

        Returns:
            str: String representation.
        """
        return (f"MailService(sender_email={self.sender_email}, smtp_server={self.smtp_server}, "
                f"smtp_port={self.smtp_port}, default_subject={self.default_subject}, "
                f"connection_type={self.connection_type})")
