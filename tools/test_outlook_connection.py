#!/usr/bin/env python3
"""
Quick test for Outlook connection with provided credentials
"""

import imaplib
import ssl

def test_outlook_credentials():
    """Test the provided Outlook credentials"""
    email = "vikas0528@outlook.com"
    password = "jjypinnaebhsfzcw"
    
    print("🔍 Testing Outlook Connection")
    print("=" * 30)
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}")
    
    # Test different Outlook server configurations
    configs = [
        ('outlook.office365.com', 993),
        ('imap-mail.outlook.com', 993)
    ]
    
    for server, port in configs:
        print(f"\n🔄 Testing {server}:{port}")
        
        try:
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect to IMAP server
            with imaplib.IMAP4_SSL(server, port, ssl_context=context) as imap:
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
                
                print(f"   🎉 SUCCESS with {server}!")
                return server, port
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n❌ All connection attempts failed.")
    return None, None

if __name__ == "__main__":
    server, port = test_outlook_credentials()
    if server:
        print(f"\n✅ Connection successful!")
        print(f"Use server: {server}, port: {port}")
    else:
        print(f"\n❌ Connection failed. Please check:")
        print("1. App password is correct")
        print("2. 2-factor authentication is enabled")
        print("3. App password was generated recently")