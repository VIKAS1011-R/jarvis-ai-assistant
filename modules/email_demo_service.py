#!/usr/bin/env python3
"""
Email Demo Service
Provides email functionality without requiring real credentials for demonstration
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random

class EmailDemoService:
    def __init__(self):
        """Initialize demo email service"""
        self.is_demo_configured = False
        self.demo_emails = self._generate_demo_emails()
        
    def setup_demo_email(self) -> str:
        """Setup demo email (no real credentials needed)"""
        self.is_demo_configured = True
        return "Demo email configured successfully! You can now use email commands with sample data."
    
    def is_configured(self) -> bool:
        """Check if demo email is configured"""
        return self.is_demo_configured
    
    def get_email_summary(self) -> str:
        """Get a summary of demo emails"""
        if not self.is_configured():
            return "Email is not configured. Say 'setup email' to configure demo email."
        
        if not self.demo_emails:
            return "No recent emails found."
        
        summary = f"You have {len(self.demo_emails)} recent emails: "
        for i, email_data in enumerate(self.demo_emails[:5], 1):
            sender = email_data.get('from', 'Unknown')
            subject = email_data.get('subject', 'No subject')
            summary += f"{i}. From {sender}, subject: {subject}. "
        
        return summary
    
    def check_new_emails(self) -> str:
        """Check for new demo emails"""
        if not self.is_configured():
            return "Email is not configured. Say 'setup email' to configure demo email."
        
        # Simulate random new email count
        new_count = random.randint(0, 3)
        
        if new_count == 0:
            return "No new emails."
        elif new_count == 1:
            return "You have 1 new email."
        else:
            return f"You have {new_count} new emails."
    
    def setup_email_interactive(self) -> str:
        """Interactive setup for demo"""
        print("🎭 Setting up DEMO email service")
        print("This is a demonstration mode with sample email data.")
        print("No real email credentials are required.")
        
        choice = input("Enable demo email? (y/n): ").lower().strip()
        if choice == 'y':
            return self.setup_demo_email()
        else:
            return "Demo email setup cancelled."
    
    def get_setup_instructions(self) -> str:
        """Get demo setup instructions"""
        return """
🎭 JARVIS Demo Email Mode

This is a demonstration mode that provides sample email data
without requiring real email credentials.

Features:
• Sample email summaries
• Simulated new email counts  
• Voice command integration
• No real email access required

To enable: Say 'Jarvis setup email' and choose demo mode.
"""
    
    def _generate_demo_emails(self) -> List[Dict]:
        """Generate realistic demo emails"""
        demo_emails = [
            {
                'from': 'boss@company.com',
                'subject': 'Project Status Update',
                'date': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M'),
                'preview': 'Hi team, please provide an update on the current project status by end of day...'
            },
            {
                'from': 'newsletter@techcrunch.com',
                'subject': 'Daily Tech News Digest',
                'date': (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M'),
                'preview': 'Today in tech: AI breakthrough, new startup funding, and industry updates...'
            },
            {
                'from': 'friend@gmail.com',
                'subject': 'Weekend Plans',
                'date': (datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'),
                'preview': 'Hey! Are we still on for the movie this Saturday? Let me know what time works...'
            },
            {
                'from': 'support@github.com',
                'subject': 'Security Alert: New Login',
                'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M'),
                'preview': 'We detected a new login to your GitHub account from a new device...'
            },
            {
                'from': 'calendar@outlook.com',
                'subject': 'Meeting Reminder: Team Standup',
                'date': (datetime.now() - timedelta(days=1, hours=3)).strftime('%Y-%m-%d %H:%M'),
                'preview': 'Reminder: You have a meeting "Team Standup" scheduled for tomorrow at 9:00 AM...'
            },
            {
                'from': 'noreply@amazon.com',
                'subject': 'Your Order Has Shipped',
                'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M'),
                'preview': 'Good news! Your order #123-4567890 has shipped and is on its way...'
            }
        ]
        
        return demo_emails

# Test function
def test_demo_email():
    """Test the demo email service"""
    print("Testing Demo Email Service")
    print("=" * 30)
    
    demo_service = EmailDemoService()
    
    print("1. Initial state:")
    print(f"   Configured: {demo_service.is_configured()}")
    
    print("\n2. Setup demo email:")
    result = demo_service.setup_demo_email()
    print(f"   {result}")
    
    print("\n3. Email summary:")
    summary = demo_service.get_email_summary()
    print(f"   {summary}")
    
    print("\n4. Check new emails:")
    new_emails = demo_service.check_new_emails()
    print(f"   {new_emails}")
    
    print("\n5. Setup instructions:")
    instructions = demo_service.get_setup_instructions()
    print(f"   {instructions}")

if __name__ == "__main__":
    test_demo_email()