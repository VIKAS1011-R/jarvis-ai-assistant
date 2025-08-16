#!/usr/bin/env python3
"""
Manual Email Setup for Outlook
Bypasses interactive setup and configures directly
"""

import os
import json
from cryptography.fernet import Fernet
import imaplib
import ssl

def manual_outlook_setup():
    """Manually configure Outlook email with provided credentials"""
    print("🔧 Manual Outlook Email Setup")
    print("=" * 40)
    
    # Your credentials
    email_address = "vikas0528@outlook.com"
    app_password = "jjypinnaebhsfzcw"
    
    print(f"Email: {email_address}")
    print(f"Password: {'*' * len(app_password)}")
    
    # Try different Outlook configurations
    outlook_configs = [
        {
            'name': 'Outlook Office365',
            'imap_server': 'outlook.office365.com',
            'imap_port': 993,
            'smtp_server': 'smtp.office365.com',
            'smtp_port': 587
        },
        {
            'name': 'Outlook Alternative',
            'imap_server': 'imap-mail.outlook.com',
            'imap_port': 993,
            'smtp_server': 'smtp-mail.outlook.com',
            'smtp_port': 587
        }
    ]
    
    working_config = None
    
    for config in outlook_configs:
        print(f"\n🔄 Testing {config['name']}...")
        
        try:
            # Test IMAP connection
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'], ssl_context=context) as imap:
                print("   ✓ SSL connection established")
                
                # Try login
                result = imap.login(email_address, app_password)
                print(f"   ✓ Login successful: {result}")
                
                # Test inbox access
                imap.select('INBOX')
                print("   ✓ Inbox access successful")
                
                # Count emails
                status, messages = imap.search(None, 'ALL')
                if status == 'OK':
                    count = len(messages[0].split()) if messages[0] else 0
                    print(f"   ✓ Found {count} emails")
                
                working_config = config
                print(f"   🎉 SUCCESS with {config['name']}!")
                break
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    if working_config:
        # Save the configuration
        save_config(email_address, app_password, working_config)
        return True
    else:
        print("\n❌ All configurations failed.")
        print("Possible solutions:")
        print("1. Generate a new app password")
        print("2. Wait 24 hours after enabling 2FA")
        print("3. Try using Gmail instead")
        return False

def save_config(email_address, app_password, config):
    """Save the working configuration"""
    print(f"\n💾 Saving configuration...")
    
    # Create config directory
    config_dir = ".kiro/email"
    os.makedirs(config_dir, exist_ok=True)
    
    # Generate encryption key
    key = Fernet.generate_key()
    key_file = os.path.join(config_dir, "email.key")
    with open(key_file, 'wb') as f:
        f.write(key)
    
    # Prepare config data
    config_data = {
        'email_address': email_address,
        'app_password': app_password,
        'provider': 'outlook',
        'imap_server': config['imap_server'],
        'imap_port': config['imap_port'],
        'smtp_server': config['smtp_server'],
        'smtp_port': config['smtp_port']
    }
    
    # Encrypt and save config
    fernet = Fernet(key)
    config_json = json.dumps(config_data)
    encrypted_config = fernet.encrypt(config_json.encode())
    
    config_file = os.path.join(config_dir, "email_config.enc")
    with open(config_file, 'wb') as f:
        f.write(encrypted_config)
    
    print("   ✅ Configuration saved successfully!")
    print(f"   📁 Stored in: {config_dir}")
    print("   🔒 Credentials are encrypted")

def test_saved_config():
    """Test if the saved configuration works with JARVIS"""
    print(f"\n🧪 Testing JARVIS Email Integration...")
    
    try:
        from modules.email_service import EmailService
        
        email_service = EmailService()
        
        if email_service.is_configured():
            print("   ✅ Email service detects configuration")
            
            # Test email summary
            summary = email_service.get_email_summary()
            print(f"   ✅ Email summary: {summary[:100]}...")
            
            # Test new email check
            new_emails = email_service.check_new_emails()
            print(f"   ✅ New emails: {new_emails}")
            
            print("   🎉 JARVIS email integration working!")
            return True
        else:
            print("   ❌ Email service doesn't detect configuration")
            return False
            
    except Exception as e:
        print(f"   ❌ JARVIS integration error: {e}")
        return False

def main():
    """Main setup function"""
    print("🤖 JARVIS Manual Email Setup")
    print("=" * 30)
    
    success = manual_outlook_setup()
    
    if success:
        print("\n✅ Email setup completed!")
        
        # Test JARVIS integration
        jarvis_works = test_saved_config()
        
        if jarvis_works:
            print("\n🎉 Ready to use!")
            print("Try these voice commands:")
            print("   • 'Jarvis check email'")
            print("   • 'Jarvis read my emails'")
            print("   • 'Jarvis email summary'")
        else:
            print("\n⚠️  Configuration saved but JARVIS integration needs work")
    else:
        print("\n❌ Setup failed. Consider using Gmail instead.")

if __name__ == "__main__":
    main()