#!/usr/bin/env python3
"""
Outlook Setup Troubleshooting Guide
"""

def check_outlook_setup():
    """Guide user through Outlook setup verification"""
    print("🔧 Outlook Email Setup Troubleshooting")
    print("=" * 50)
    
    print("\n📋 Let's verify your Microsoft account setup:")
    print()
    
    print("1. ✅ Two-Factor Authentication Check:")
    print("   - Go to: https://account.microsoft.com/security")
    print("   - Sign in with vikas0528@outlook.com")
    print("   - Look for 'Two-step verification' - should be ON")
    
    tfa_enabled = input("   Is Two-step verification enabled? (y/n): ").lower().strip()
    
    if tfa_enabled != 'y':
        print("   ❌ You need to enable Two-step verification first!")
        print("   📝 Steps:")
        print("      1. Go to https://account.microsoft.com/security")
        print("      2. Click 'Two-step verification'")
        print("      3. Turn it ON and complete setup")
        print("      4. Wait 10-15 minutes after enabling")
        return False
    
    print("\n2. ✅ App Password Generation:")
    print("   - On the same security page")
    print("   - Look for 'App passwords' section")
    print("   - Click 'Create a new app password'")
    
    app_password_visible = input("   Can you see 'App passwords' option? (y/n): ").lower().strip()
    
    if app_password_visible != 'y':
        print("   ❌ App passwords option is missing!")
        print("   📝 Common causes:")
        print("      1. Two-step verification was just enabled (wait 24 hours)")
        print("      2. Work/School account (admin restrictions)")
        print("      3. Security defaults enabled (contact Microsoft)")
        print()
        print("   🔄 Alternative solutions:")
        print("      1. Try using Gmail instead (easier setup)")
        print("      2. Contact Microsoft support")
        print("      3. Use a different email account")
        return False
    
    print("\n3. ✅ App Password Format:")
    print("   Your app password: jjypinnaebhsfzcw")
    print("   - Length: 16 characters ✅")
    print("   - No spaces/dashes ✅")
    print("   - All lowercase ✅")
    
    print("\n4. ✅ Account Type Check:")
    account_type = input("   Is this a personal Microsoft account or work/school? (personal/work): ").lower().strip()
    
    if account_type == 'work':
        print("   ⚠️  Work/School accounts often have restrictions!")
        print("   📝 Your IT admin may have disabled app passwords")
        print("   💡 Try using a personal email account instead")
    
    print("\n5. 🔄 Alternative Solutions:")
    print("   If Outlook continues to fail, try:")
    print("   A. Generate a NEW app password")
    print("   B. Use Gmail instead (more reliable)")
    print("   C. Wait 24 hours after enabling 2FA")
    
    return True

def suggest_gmail_alternative():
    """Suggest using Gmail as alternative"""
    print("\n📧 Gmail Alternative (Recommended)")
    print("=" * 40)
    print("Gmail is often easier to set up with JARVIS:")
    print()
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Enable 2-Step Verification")
    print("3. Go to Security → App passwords")
    print("4. Generate password for 'JARVIS'")
    print("5. Use the 16-character password")
    print()
    print("Gmail typically has fewer authentication issues.")
    
    use_gmail = input("Would you like to try Gmail instead? (y/n): ").lower().strip()
    return use_gmail == 'y'

def main():
    """Main troubleshooting function"""
    setup_ok = check_outlook_setup()
    
    if not setup_ok:
        if suggest_gmail_alternative():
            print("\n✅ Let's set up Gmail instead!")
            print("Run: python setup_email.py")
            print("Select Gmail (option 1)")
        else:
            print("\n🔧 Continue troubleshooting Outlook:")
            print("1. Generate a new app password")
            print("2. Wait 24 hours after enabling 2FA")
            print("3. Contact Microsoft support if issues persist")

if __name__ == "__main__":
    main()