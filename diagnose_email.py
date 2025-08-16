#!/usr/bin/env python3
"""
Email Connection Diagnostic Tool
Helps troubleshoot email connection issues
"""

import imaplib
import ssl
import getpass

def test_outlook_connection():
    """Test Outlook connection with detailed diagnostics"""
    print("🔍 Outlook Email Connection Diagnostics")
    print("=" * 50)
    
    email = input("Enter your Outlook email address: ").strip()
    print("Enter your app-specific password (remove spaces/dashes):")
    password = getpass.getpass("App Password: ")
    
    # Test different Outlook server configurations
    outlook_configs = [
        {
            'name': 'Outlook.com (Primary)',
            'server': 'outlook.office365.com',
            'port': 993
        },
        {
            'name': 'Outlook.com (Alternative)',
            'server': 'imap-mail.outlook.com',
            'port': 993
        },
        {
            'name': 'Office365 (Business)',
            'server': 'outlook.office365.com',
            'port': 993
        }
    ]
    
    for config in outlook_configs:
        print(f"\n🔄 Testing {config['name']}...")
        print(f"   Server: {config['server']}:{config['port']}")
        
        try:
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect to IMAP server
            with imaplib.IMAP4_SSL(config['server'], config['port'], ssl_context=context) as imap:
                print("   ✓ SSL connection established")
                
                # Try to login
                result = imap.login(email, password)
                print(f"   ✓ Login successful: {result}")
                
                # Try to select inbox
                imap.select('INBOX')
                print("   ✓ Inbox access successful")
                
                # Get email count
                status, messages = imap.search(None, 'ALL')
                if status == 'OK':
                    count = len(messages[0].split()) if messages[0] else 0
                    print(f"   ✓ Found {count} emails in inbox")
                
                print(f"   🎉 SUCCESS with {config['name']}!")
                return config
                
        except imaplib.IMAP4.error as e:
            print(f"   ❌ IMAP Error: {e}")
        except ssl.SSLError as e:
            print(f"   ❌ SSL Error: {e}")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
    
    print("\n❌ All connection attempts failed.")
    print("\n🔧 Troubleshooting Tips:")
    print("1. Verify 2-factor authentication is enabled")
    print("2. Generate a new app-specific password")
    print("3. Remove all spaces/dashes from the password")
    print("4. Try using your full email address")
    print("5. Check if your account is a personal or business account")
    
    return None

def test_gmail_connection():
    """Test Gmail connection"""
    print("🔍 Gmail Email Connection Diagnostics")
    print("=" * 50)
    
    email = input("Enter your Gmail address: ").strip()
    print("Enter your app-specific password:")
    password = getpass.getpass("App Password: ")
    
    try:
        context = ssl.create_default_context()
        
        with imaplib.IMAP4_SSL('imap.gmail.com', 993, ssl_context=context) as imap:
            print("   ✓ SSL connection established")
            
            result = imap.login(email, password)
            print(f"   ✓ Login successful: {result}")
            
            imap.select('INBOX')
            print("   ✓ Inbox access successful")
            
            status, messages = imap.search(None, 'ALL')
            if status == 'OK':
                count = len(messages[0].split()) if messages[0] else 0
                print(f"   ✓ Found {count} emails in inbox")
            
            print("   🎉 Gmail connection successful!")
            return True
            
    except Exception as e:
        print(f"   ❌ Gmail connection failed: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("📧 JARVIS Email Connection Diagnostics")
    print("=" * 40)
    
    provider = input("Which provider are you testing? (1=Outlook, 2=Gmail): ").strip()
    
    if provider == '1':
        config = test_outlook_connection()
        if config:
            print(f"\n✅ Use these settings in JARVIS:")
            print(f"   Server: {config['server']}")
            print(f"   Port: {config['port']}")
    elif provider == '2':
        success = test_gmail_connection()
        if success:
            print("\n✅ Gmail settings are correct for JARVIS")
    else:
        print("Invalid choice. Please run again and select 1 or 2.")

if __name__ == "__main__":
    main()