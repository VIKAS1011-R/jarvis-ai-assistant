#!/usr/bin/env python3
"""
Secure Email Configuration
Handles email setup with proper security practices
"""

import os
import json
import getpass
from cryptography.fernet import Fernet
from typing import Dict, Optional, Tuple
import base64

class SecureEmailConfig:
    def __init__(self):
        """Initialize secure email configuration"""
        self.config_dir = ".kiro/email"
        self.config_file = os.path.join(self.config_dir, "email_config.enc")
        self.key_file = os.path.join(self.config_dir, "email.key")
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Email provider configurations
        self.email_providers = {
            'gmail': {
                'imap_server': 'imap.gmail.com',
                'imap_port': 993,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'requires_app_password': True,
                'setup_url': 'https://support.google.com/accounts/answer/185833'
            },
            'outlook': {
                'imap_server': 'outlook.office365.com',
                'imap_port': 993,
                'smtp_server': 'smtp-mail.outlook.com',
                'smtp_port': 587,
                'requires_app_password': True,
                'setup_url': 'https://support.microsoft.com/en-us/account-billing/using-app-passwords-with-apps-that-don-t-support-two-step-verification-5896ed9b-4263-e681-128a-a6f2979a7944'
            },
            'yahoo': {
                'imap_server': 'imap.mail.yahoo.com',
                'imap_port': 993,
                'smtp_server': 'smtp.mail.yahoo.com',
                'smtp_port': 587,
                'requires_app_password': True,
                'setup_url': 'https://help.yahoo.com/kb/generate-third-party-passwords-sln15241.html'
            }
        }
    
    def _generate_key(self) -> bytes:
        """Generate encryption key"""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(key)
        return key
    
    def _load_key(self) -> bytes:
        """Load encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            return self._generate_key()
    
    def _encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        key = self._load_key()
        fernet = Fernet(key)
        return fernet.encrypt(data.encode())
    
    def _decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        key = self._load_key()
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data).decode()
    
    def setup_email_interactive(self) -> bool:
        """Interactive email setup with security guidance"""
        print("🔐 JARVIS Email Configuration")
        print("=" * 40)
        print("For security, JARVIS uses app-specific passwords, not your regular email password.")
        print()
        
        # Show provider options
        print("Supported email providers:")
        for i, (provider, config) in enumerate(self.email_providers.items(), 1):
            print(f"{i}. {provider.title()}")
        
        # Get provider choice
        while True:
            try:
                choice = input("\nSelect your email provider (1-3): ").strip()
                provider_index = int(choice) - 1
                provider_names = list(self.email_providers.keys())
                
                if 0 <= provider_index < len(provider_names):
                    selected_provider = provider_names[provider_index]
                    break
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            except ValueError:
                print("Please enter a number.")
        
        provider_config = self.email_providers[selected_provider]
        
        print(f"\n📧 Setting up {selected_provider.title()} email")
        print("=" * 30)
        
        if provider_config['requires_app_password']:
            print("⚠️  IMPORTANT: You need an app-specific password!")
            print(f"Setup guide: {provider_config['setup_url']}")
            print()
            print("Steps:")
            print("1. Enable 2-factor authentication on your account")
            print("2. Generate an app-specific password for JARVIS")
            print("3. Use the app password below (NOT your regular password)")
            print()
            
            proceed = input("Have you created an app-specific password? (y/n): ").lower().strip()
            if proceed != 'y':
                print("Please create an app-specific password first, then run this setup again.")
                return False
        
        # Get email credentials
        email_address = input("Enter your email address: ").strip()
        
        if not self._validate_email(email_address):
            print("Invalid email address format.")
            return False
        
        print("Enter your app-specific password (input will be hidden):")
        app_password = getpass.getpass("App Password: ")
        
        if not app_password:
            print("Password cannot be empty.")
            return False
        
        # Test connection
        print("\n🔄 Testing email connection...")
        if self._test_connection(email_address, app_password, provider_config):
            # Save encrypted configuration
            config_data = {
                'email_address': email_address,
                'app_password': app_password,
                'provider': selected_provider,
                'imap_server': provider_config['imap_server'],
                'imap_port': provider_config['imap_port'],
                'smtp_server': provider_config['smtp_server'],
                'smtp_port': provider_config['smtp_port']
            }
            
            if self._save_config(config_data):
                print("✅ Email configuration saved successfully!")
                print("🔒 Your credentials are encrypted and stored securely.")
                return True
            else:
                print("❌ Failed to save email configuration.")
                return False
        else:
            print("❌ Email connection test failed.")
            print("Please check your credentials and try again.")
            return False
    
    def _validate_email(self, email: str) -> bool:
        """Validate email address format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _test_connection(self, email: str, password: str, config: Dict) -> bool:
        """Test email connection"""
        try:
            import imaplib
            import ssl
            
            # Test IMAP connection
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'], ssl_context=context) as imap:
                imap.login(email, password)
                imap.select('INBOX')
                return True
                
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def _save_config(self, config_data: Dict) -> bool:
        """Save encrypted email configuration"""
        try:
            config_json = json.dumps(config_data)
            encrypted_config = self._encrypt_data(config_json)
            
            with open(self.config_file, 'wb') as f:
                f.write(encrypted_config)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self) -> Optional[Dict]:
        """Load and decrypt email configuration"""
        try:
            if not os.path.exists(self.config_file):
                return None
            
            with open(self.config_file, 'rb') as f:
                encrypted_config = f.read()
            
            config_json = self._decrypt_data(encrypted_config)
            return json.loads(config_json)
            
        except Exception as e:
            print(f"Error loading config: {e}")
            return None
    
    def is_configured(self) -> bool:
        """Check if email is configured"""
        return os.path.exists(self.config_file) and os.path.exists(self.key_file)
    
    def remove_config(self) -> bool:
        """Remove email configuration (for security)"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            if os.path.exists(self.key_file):
                os.remove(self.key_file)
            return True
        except Exception as e:
            print(f"Error removing config: {e}")
            return False
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions for email configuration"""
        instructions = """
📧 JARVIS Email Setup Instructions

For security, JARVIS requires app-specific passwords:

🔐 Gmail Setup:
1. Go to Google Account settings
2. Enable 2-factor authentication
3. Go to Security → App passwords
4. Generate password for "JARVIS"
5. Use this app password (not your Gmail password)

🔐 Outlook Setup:
1. Go to Microsoft Account security
2. Enable 2-factor authentication
3. Go to Security → App passwords
4. Generate password for "JARVIS"
5. Use this app password (not your Outlook password)

🔐 Yahoo Setup:
1. Go to Yahoo Account security
2. Enable 2-factor authentication
3. Generate app password for "JARVIS"
4. Use this app password (not your Yahoo password)

⚠️  NEVER use your regular email password with third-party apps!

To configure: Run 'python modules/secure_email_config.py'
"""
        return instructions

def main():
    """Main setup function"""
    config = SecureEmailConfig()
    
    if config.is_configured():
        print("Email is already configured.")
        choice = input("Do you want to reconfigure? (y/n): ").lower().strip()
        if choice == 'y':
            config.remove_config()
        else:
            return
    
    print(config.get_setup_instructions())
    
    proceed = input("Ready to configure email? (y/n): ").lower().strip()
    if proceed == 'y':
        success = config.setup_email_interactive()
        if success:
            print("\n🎉 Email configuration complete!")
            print("You can now use email commands with JARVIS.")
        else:
            print("\n❌ Email configuration failed.")
            print("Please try again or check the setup instructions.")
    else:
        print("Email configuration cancelled.")

if __name__ == "__main__":
    main()