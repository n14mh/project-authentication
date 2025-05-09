import dns.resolver
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Global Variables
# Test Domain
domain = "projectauthentication.com"

# Test Email Sender
sender = "from-addr@projectauthentication.com"

# Test Email Recipients
recipients = ["thelncproject3@gmail.com", "thelncproject3@outlook.ie", "thelncproject3@yahoo.com"]

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
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Secure Connection
            server.starttls()

            # Authenticate with SMTP server if credentials provided with test case
            if smtp_user:
                server.login(smtp_user, smtp_password)

            # Send email to recipient with subject and body template for this test case
            server.sendmail(sender, recipient, msg.as_string())

            # Print message if email was sent successfully
            print(f"Email successfully sent!")

            # Introducing a delay in order to avoid overwhelming the services
            time.sleep(3)

    except Exception as e:
        #Print message if email failed to send
        print(f"Failed to send email: {e}")

# Test Case 1: Outlook SMTP, Legitimate email templates
def send_test_case_1(test_phase):
    for recipient in recipients:
        for i in range(1,4): # Sending three email templates
            subject = "Test Phase #" + str(test_phase) + " - Test Case #1 - Legit Email #" + str(i)
            print("Sending: " + subject + " - TO: " + recipient)
            template = load_email_template(f"emails/legit_email_{i}.html")
            send_email(outlook_smtp_server, outlook_smtp_port, sender, recipient, subject, template, outlook_smtp_user, outlook_smtp_password)

# Test Case 2: Outlook SMTP, Phishing email templates
def send_test_case_2(test_phase):
    for recipient in recipients:
        for i in range(1,4): # Sending three email templates
            subject = "Test Phase #" + str(test_phase) + " - Test Case #2 - Phish Email #" + str(i)
            print("Sending: " + subject + " - TO: " + recipient)
            template = load_email_template(f"emails/phish_email_{i}.html")
            send_email(outlook_smtp_server, outlook_smtp_port, sender, recipient, subject, template, outlook_smtp_user, outlook_smtp_password)

# Test Case 3: Postfix SMTP, Legitimate email templates
def send_test_case_3(test_phase):
    for recipient in recipients:
        for i in range(1,4): # Sending three email templates
            subject = "Test Phase #" + str(test_phase) + " - Test Case #3 - Legit Email #" + str(i)
            print("Sending: " + subject + " - TO: " + recipient)
            template = load_email_template(f"emails/legit_email_{i}.html")
            send_email(postfix_smtp_server, postfix_smtp_port,sender, recipient, subject, template)

# Test Case 4: Postfix SMTP, Phishing email templates
def send_test_case_4(test_phase):
    for recipient in recipients:
        for i in range(1,4): # Sending three email templates
            subject = "Test Phase #" + str(test_phase) + " - Test Case #4 - Phish Email #" + str(i)
            print("Sending: " + subject + " - TO: " + recipient)
            template = load_email_template(f"emails/phish_email_{i}.html")
            send_email(postfix_smtp_server, postfix_smtp_port, sender, recipient, subject, template)

def main():
    # Configure which test phase is to be deployed - change as testing progresses
    test_phase = 4
    print(f"\n--- Test Phase {test_phase} ---\n")

    # Confirming SPF, DKIM and DMARC configured for the domain
    print(f"--- Verifying current SPF, DKIM and DMARC configuration in DNS records for {domain}---\n")
    spf_result = check_spf(domain)
    dkim_result = check_dkim(domain)
    dmarc_result = check_dmarc(domain)

    print("SPF:     " + spf_result)
    print("DKIM:    " + dkim_result)
    print("DMARC:   " + dmarc_result)

    # Deploy emails for each test case
    print(f"\n--- Deploying Test Emails Test Phase {test_phase} ---\n")
    print(f"\n--- Sending Emails for Test Case 1 ---")
    send_test_case_1(test_phase)
    print(f"\n--- Sending Emails for Test Case 2 ---")
    send_test_case_2(test_phase)
    print(f"\n--- Sending Emails for Test Case 3 ---")
    send_test_case_3(test_phase)
    print(f"\n--- Sending Emails for Test Case 4 ---")
    send_test_case_4(test_phase)

    print(f"\n--- All Test Emails Sent for Test Phase {test_phase} ---\n")

if __name__ == "__main__":
    main()