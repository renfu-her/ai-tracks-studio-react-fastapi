"""Email service for sending emails."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending emails via SMTP."""
    
    def __init__(self):
        """Initialize email service with settings."""
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USER
        self.from_name = settings.SMTP_FROM_NAME
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """
        Send an email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: Optional HTML email body
            
        Returns:
            True if email sent successfully, False otherwise
        """
        # Skip sending if email is not configured
        if not self.user or not self.password:
            logger.warning("Email not configured. Skipping email send.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_feedback_notification(
        self,
        name: str,
        email: str,
        subject: str | None,
        message: str
    ) -> bool:
        """
        Send feedback notification email.
        
        Args:
            name: Sender name
            email: Sender email
            subject: Feedback subject
            message: Feedback message
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not settings.FEEDBACK_TO_EMAIL:
            logger.warning("FEEDBACK_TO_EMAIL not configured. Skipping email send.")
            return False
        
        email_subject = f"New Feedback: {subject or 'No Subject'}"
        
        # Plain text body
        text_body = f"""
New feedback received from AI-Tracks Studio website:

Name: {name}
Email: {email}
Subject: {subject or 'No Subject'}

Message:
{message}

---
This is an automated message from AI-Tracks Studio.
"""
        
        # HTML body
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .content {{ background-color: #ffffff; padding: 20px; border: 1px solid #dee2e6; border-radius: 5px; }}
        .field {{ margin-bottom: 15px; }}
        .label {{ font-weight: bold; color: #495057; }}
        .value {{ margin-top: 5px; padding: 10px; background-color: #f8f9fa; border-radius: 3px; }}
        .message {{ white-space: pre-wrap; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #dee2e6; font-size: 12px; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>New Feedback Received</h2>
        </div>
        <div class="content">
            <div class="field">
                <div class="label">Name:</div>
                <div class="value">{name}</div>
            </div>
            <div class="field">
                <div class="label">Email:</div>
                <div class="value">{email}</div>
            </div>
            <div class="field">
                <div class="label">Subject:</div>
                <div class="value">{subject or 'No Subject'}</div>
            </div>
            <div class="field">
                <div class="label">Message:</div>
                <div class="value message">{message}</div>
            </div>
        </div>
        <div class="footer">
            This is an automated message from AI-Tracks Studio.
        </div>
    </div>
</body>
</html>
"""
        
        return self.send_email(
            to_email=settings.FEEDBACK_TO_EMAIL,
            subject=email_subject,
            body=text_body,
            html_body=html_body
        )


# Global email service instance
email_service = EmailService()
