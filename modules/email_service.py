#!/usr/bin/env python3
"""
Email Service Module
Secure email functionality with proper authentication
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import re
import ssl
from datetime import datetime
try:
    from .secure_email_config import SecureEmailConfig
except ImportError:
    from secure_email_config import SecureEmailConfig

class EmailService:
    def __init__(self):
        """Initialize email service with secure configuration"""
        self.config_manager = SecureEmailConfig()
        self.config = None
        self.is_connected = False
        self._load_configuration()
    
    def _load_configuration(self):
        """Load email configuration"""
        self.config = self.config_manager.load_config()
        if self.config:
            self.is_connected = True
    
    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        return self.config is not None
    
    def setup_email_interactive(self) -> str:
        """Setup email using interactive configuration"""
        if self.config_manager.setup_email_interactive():
            self._load_configuration()
            return "Email configured successfully! You can now use email commands."
        else:
            return "Email configuration failed. Please try again."
    
    def get_email_summary(self) -> str:
        """
        Get a summary of recent emails
        
        Returns:
            str: Email summary or status message
        """
        if not self.is_configured():
            return "Email is not configured. Say 'setup email' to configure your email securely."
        
        try:
            emails = self._fetch_recent_emails(5)
            if not emails:
                return "No recent emails found."
            
            summary = f"You have {len(emails)} recent emails: "
            for i, email_data in enumerate(emails, 1):
                sender = email_data.get('from', 'Unknown')
                subject = email_data.get('subject', 'No subject')
                summary += f"{i}. From {sender}, subject: {subject}. "
            
            return summary
            
        except Exception as e:
            print(f"Error getting email summary: {e}")
            return "I couldn't retrieve your emails right now. Please check your connection."
    
    def check_new_emails(self) -> str:
        """Check for new emails"""
        if not self.is_configured():
            return "Email is not configured. Say 'setup email' to configure your email securely."
        
        try:
            unread_count = self._get_unread_count()
            if unread_count == 0:
                return "No new emails."
            elif unread_count == 1:
                return "You have 1 new email."
            else:
                return f"You have {unread_count} new emails."
                
        except Exception as e:
            print(f"Error checking emails: {e}")
            return "I couldn't check your emails right now. Please check your connection."
    
    def get_email_help(self) -> str:
        """Get help for email setup"""
        help_text = """Email Setup Guide:
        
        For Gmail:
        1. Enable 2-factor authentication
        2. Generate an app-specific password
        3. Use the app password (not your regular password)
        
        For Outlook:
        1. Enable app passwords in security settings
        2. Generate an app password for JARVIS
        
        Security Note: Never use your regular email password with third-party applications.
        Always use app-specific passwords or OAuth2 authentication."""
        
        return help_text
    
    def send_test_email(self, to_address: str, subject: str = "Test from JARVIS") -> str:
        """
        Send a test email (placeholder implementation)
        
        Args:
            to_address: Recipient email address
            subject: Email subject
            
        Returns:
            str: Send status
        """
        if not self.is_configured():
            return "Email is not configured. Please set up your email first."
        
        # This is a placeholder - real implementation would send actual email
        return f"Email sending requires secure authentication. Would send test email to {to_address} with subject '{subject}'."
    
    def _fetch_recent_emails(self, count: int = 5) -> List[Dict]:
        """Fetch recent emails from the server"""
        if not self.config:
            return []
        
        try:
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect to IMAP server
            with imaplib.IMAP4_SSL(self.config['imap_server'], self.config['imap_port'], ssl_context=context) as imap:
                # Login
                imap.login(self.config['email_address'], self.config['app_password'])
                
                # Select inbox
                imap.select('INBOX')
                
                # Search for recent emails
                status, messages = imap.search(None, 'ALL')
                if status != 'OK':
                    return []
                
                # Get message IDs
                message_ids = messages[0].split()
                recent_ids = message_ids[-count:] if len(message_ids) >= count else message_ids
                
                emails = []
                for msg_id in reversed(recent_ids):  # Most recent first
                    try:
                        # Fetch email
                        status, msg_data = imap.fetch(msg_id, '(RFC822)')
                        if status != 'OK':
                            continue
                        
                        # Parse email
                        email_message = email.message_from_bytes(msg_data[0][1])
                        
                        # Extract email data
                        email_data = {
                            'from': email_message.get('From', 'Unknown'),
                            'subject': email_message.get('Subject', 'No subject'),
                            'date': email_message.get('Date', 'Unknown date'),
                            'message_id': msg_id.decode()
                        }
                        
                        # Get email body preview
                        body = self._get_email_body(email_message)
                        if body:
                            email_data['preview'] = body[:100] + '...' if len(body) > 100 else body
                        
                        emails.append(email_data)
                        
                    except Exception as e:
                        print(f"Error parsing email {msg_id}: {e}")
                        continue
                
                return emails
                
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
    
    def _get_unread_count(self) -> int:
        """Get count of unread emails"""
        if not self.config:
            return 0
        
        try:
            context = ssl.create_default_context()
            
            with imaplib.IMAP4_SSL(self.config['imap_server'], self.config['imap_port'], ssl_context=context) as imap:
                imap.login(self.config['email_address'], self.config['app_password'])
                imap.select('INBOX')
                
                # Search for unread emails
                status, messages = imap.search(None, 'UNSEEN')
                if status == 'OK':
                    message_ids = messages[0].split()
                    return len(message_ids)
                
                return 0
                
        except Exception as e:
            print(f"Error getting unread count: {e}")
            return 0
    
    def _get_email_body(self, email_message) -> str:
        """Extract email body text"""
        try:
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        if body:
                            return body.decode('utf-8', errors='ignore')
            else:
                body = email_message.get_payload(decode=True)
                if body:
                    return body.decode('utf-8', errors='ignore')
            
            return ""
            
        except Exception as e:
            print(f"Error extracting email body: {e}")
            return ""
    
    def get_setup_instructions(self) -> str:
        """Get email setup instructions"""
        return self.config_manager.get_setup_instructions()

# Simplified email reader for demonstration
class SimpleEmailReader:
    """Simplified email reader for basic functionality"""
    
    def __init__(self):
        self.mock_emails = [
            {
                'from': 'example@company.com',
                'subject': 'Meeting Reminder',
                'date': '2024-01-15',
                'preview': 'Don\'t forget about our meeting tomorrow at 2 PM...'
            },
            {
                'from': 'newsletter@tech.com',
                'subject': 'Weekly Tech News',
                'date': '2024-01-14',
                'preview': 'This week in technology: AI advances, new frameworks...'
            },
            {
                'from': 'friend@email.com',
                'subject': 'Weekend Plans',
                'date': '2024-01-13',
                'preview': 'Hey! Are we still on for the movie this weekend?...'
            }
        ]
    
    def get_recent_emails(self, count: int = 3) -> str:
        """Get recent emails summary"""
        if not self.mock_emails:
            return "No recent emails found."
        
        email_summary = f"You have {len(self.mock_emails)} recent emails: "
        
        for i, email_data in enumerate(self.mock_emails[:count], 1):
            sender = email_data['from']
            subject = email_data['subject']
            date = email_data['date']
            
            email_summary += f"{i}. From {sender}, subject: {subject}, received {date}. "
        
        return email_summary
    
    def read_email_preview(self, index: int = 1) -> str:
        """Read email preview"""
        try:
            if 1 <= index <= len(self.mock_emails):
                email_data = self.mock_emails[index - 1]
                return f"Email from {email_data['from']}: {email_data['subject']}. {email_data['preview']}"
            else:
                return f"Email {index} not found. You have {len(self.mock_emails)} emails."
        except:
            return "I couldn't read that email."

# Test function
def test_email_service():
    """Test the email service"""
    print("Testing Email Service")
    print("=" * 30)
    
    email_service = EmailService()
    
    print("1. Email summary:")
    summary = email_service.get_email_summary()
    print(f"   {summary}")
    
    print("\n2. Email help:")
    help_text = email_service.get_email_help()
    print(f"   {help_text}")
    
    print("\n3. Simple email reader:")
    reader = SimpleEmailReader()
    recent = reader.get_recent_emails(2)
    print(f"   {recent}")
    
    preview = reader.read_email_preview(1)
    print(f"   {preview}")

if __name__ == "__main__":
    test_email_service()