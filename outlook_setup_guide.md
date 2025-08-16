# Microsoft Outlook App Password Setup Guide

## 🔐 **Step-by-Step Outlook Setup for JARVIS**

### **Method 1: Modern Microsoft Account (Recommended)**

1. **Go to Microsoft Account Security**
   - Visit: https://account.microsoft.com/security
   - Sign in with your Outlook account

2. **Enable Two-Step Verification**
   - Click "Two-step verification"
   - Turn it ON if not already enabled
   - Complete the setup process

3. **Generate App Password**
   - Go back to Security page
   - Click "App passwords" 
   - Click "Create a new app password"
   - Enter name: "JARVIS" or "Email Client"
   - Copy the generated password (it will look like: abcd-efgh-ijkl-mnop)

4. **Important Notes:**
   - Remove ALL spaces and dashes from the password
   - Use only letters and numbers: abcdefghijklmnop
   - Don't use your regular Outlook password

### **Method 2: If App Passwords Option is Missing**

Some Microsoft accounts don't show "App passwords". Try this:

1. **Check Account Type**
   - Personal accounts: Usually support app passwords
   - Work/School accounts: May be restricted by admin

2. **Alternative: Use OAuth2 (Advanced)**
   - This requires more complex setup
   - Not recommended for basic users

3. **Try Different Security Settings**
   - Go to Security → Sign-in options
   - Look for "App passwords" or "Security defaults"

### **Method 3: Gmail Alternative (Easier)**

If Outlook continues to have issues, Gmail is often easier:

1. **Gmail Setup:**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification
   - Go to Security → App passwords
   - Generate password for "JARVIS"
   - Use the 16-character password (remove spaces)

## 🔍 **Common Issues & Solutions**

### **Issue: "App passwords" option missing**
**Solution:** 
- Ensure 2FA is fully enabled and verified
- Wait 24 hours after enabling 2FA
- Try signing out and back in

### **Issue: Password has spaces/dashes**
**Solution:**
- Remove ALL spaces and dashes
- Example: "abcd-efgh-ijkl" becomes "abcdefghijkl"

### **Issue: Still getting "LOGIN failed"**
**Solution:**
- Try generating a new app password
- Use your full email address
- Check if account is personal vs business

## 🎯 **Quick Test**

After generating the app password:
1. Run: `python diagnose_email.py`
2. Select Outlook (1)
3. Enter your email and the app password (no spaces)
4. See if connection succeeds

## 📧 **Alternative: Use Gmail**

If Outlook continues to be problematic, Gmail is often more reliable:
- Gmail's app password system is more straightforward
- Better compatibility with IMAP clients
- Clearer error messages

Would you like to try Gmail instead, or continue troubleshooting Outlook?