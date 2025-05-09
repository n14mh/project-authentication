import smtplib
import dns.resolver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Global Variables
# Test Domain
domain = "projectauthentication.com"

# Test Email Sender
sender = "from-addr@projectauthentication.com"

# Test Email Recipient
recipient = "kennedy.niamh@live.ie"

# Authenticated Outlook SMTP
outlook_smtp_server = "smtp-mail.outlook.com"
outlook_smtp_port = 587
outlook_smtp_user = sender
outlook_smtp_password = "kpdwppzfjyhswhxn"

# Postfix SMTP
postfix_smtp_server = "localhost"
postfix_smtp_port = 25

# Check DNS records for the provided domain to verify TXT record exists for SPF
def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            if 'v=spf1' in rdata.to_text():
                return "Y"
        return "N"
    except:
        return "N"

# Check DNS records for the provided domain to verify CNAME record exists for DKIM
def check_dkim(domain, selector="1"):
    try:
        dkim_domain = f"selector{selector}._domainkey.{domain}"
        answers = dns.resolver.resolve(dkim_domain, 'CNAME')
        if answers:
            return "Y"
        return "N"
    except:
        return "N"

# Check DNS records for the provided domain to verify TXT record exists for DMARC
def check_dmarc(domain):
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        if answers:
            return "Y"
        return "N"
    except:
        return "N"

# Load Email Templates
def load_email_template(template_file):
    with open(template_file, "r") as f:
        return f.read()

# Send Emails by Test Case and Email Template
def send_email(smtp_server, smtp_port, sender, recipient, subject, body, smtp_user=None, smtp_password=None):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Secure Connection
            server.starttls()

            # Authenticate with SMTP server if credentials provided
            if smtp_user:
                server.login(smtp_user, smtp_password)

            # Send email to recipient with subject and body template for this test case
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()

            # Print message if email sent successfully from the SMTP server
            if smtp_user:
                print(f"Test Email Sent to {recipient} from Outlook SMTP Server ---")
            else:
                print(f"Test Email Sent to {recipient} from Postfix SMTP Server ---\n")

    except Exception as e:
        #Print message if email failed to send
        if smtp_user:
            print(f"Failed to send email using Outlook SMTP: {e}")
        else:
            print(f"Failed to send email using Postfix SMTP: {e}\n")

def main():

    # Confirming SPF, DKIM and DMARC configured for the domain
    print(f"--- Verifying current SPF, DKIM and DMARC configuration in DNS records for {domain} ---")
    spf_result = check_spf(domain)
    dkim_result = check_dkim(domain)
    dmarc_result = check_dmarc(domain)

    print("SPF:     " + spf_result)
    print("DKIM:    " + dkim_result)
    print("DMARC:   " + dmarc_result)

    # Email content
    subject = "Testing"
    body = f"Test email sent from {sender}.\nSPF: {spf_result}\nDKIM: {dkim_result}\nDMARC: {dmarc_result}"

    print(f"\n--- Sending Test Emails ---")
    # Testing the ability to send an email from Outlook SMTP with authentication
    send_email(outlook_smtp_server, outlook_smtp_port, sender, recipient, subject, body, outlook_smtp_user, outlook_smtp_password)

    # Testing the ability to send
    send_email(postfix_smtp_server, postfix_smtp_port, sender, recipient, subject, body)

if __name__ == "__main__":
    main()