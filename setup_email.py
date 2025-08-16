#!/usr/bin/env python3
"""
JARVIS Email Setup Script
Secure email configuration for JARVIS
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.secure_email_config import SecureEmailConfig

def main():
    """Main email setup function"""
    print("🤖 JARVIS Email Configuration")
    print("=" * 40)
    
    config = SecureEmailConfig()
    
    if config.is_configured():
        print("✅ Email is already configured for JARVIS.")
        print(f"📧 Configuration stored securely in: {config.config_dir}")
        
        choice = input("\nDo you want to reconfigure email? (y/n): ").lower().strip()
        if choice != 'y':
            print("Email configuration unchanged.")
            return
        
        print("Removing existing configuration...")
        config.remove_config()
    
    print("\n📋 Email Setup Instructions")
    print(config.get_setup_instructions())
    
    proceed = input("Ready to configure email for JARVIS? (y/n): ").lower().strip()
    if proceed == 'y':
        success = config.setup_email_interactive()
        if success:
            print("\n🎉 Email configuration complete!")
            print("✅ JARVIS can now access your email securely.")
            print("\n📝 Available email commands:")
            print("   • 'Jarvis check email'")
            print("   • 'Jarvis read my emails'")
            print("   • 'Jarvis email summary'")
            print("   • 'Jarvis how many new emails'")
        else:
            print("\n❌ Email configuration failed.")
            print("Please check the setup instructions and try again.")
    else:
        print("Email configuration cancelled.")
        print("You can run this script again anytime to configure email.")

if __name__ == "__main__":
    main()