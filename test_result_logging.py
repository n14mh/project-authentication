import csv
import dns.resolver
import imaplib


# Global Variables
# Test Domain
domain = "projectauthentication.com"

# Test Email Sender
sender = "from-addr@projectauthentication.com"

# Test Email Recipients
recipients = ["thelncproject3@gmail.com", "thelncproject3@outlook.ie", "thelncproject3@yahoo.com"]


def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            if 'v=spf1' in rdata.to_text():
                return "Y"
        return "N"
    except:
        return "N"


def check_dkim(domain, selector="1"):
    try:
        dkim_domain = f"selector{selector}._domainkey.{domain}"
        answers = dns.resolver.resolve(dkim_domain, 'CNAME')
        if answers:
            return "Y"
        return "N"
    except:
        return "N"


def check_dmarc(domain):
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        if answers:
            return "Y"
        return "N"
    except:
        return "N"

# Check Gmail recipient inbox
def check_gmail_recipient_status(recipient, subject):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(recipient,"stlfozipuuzhfugf ")

        # Check Spam folder first
        status, _ = mail.select("[Gmail]/Spam")
        if status == "OK":
            result, data = mail.search(None, f'(FROM "{sender}" SUBJECT "{subject}")')
            if data[0]:
                return "Spam"

        # Check Inbox last
        mail.select("Inbox")
        result, data = mail.search(None, f'(FROM "{sender}" SUBJECT "{subject}")')
        if data[0]:
            return "Inbox"

        return "Not Found"
    except Exception as e:
        return f"Error checking status: {e}"
    finally:
        if mail:
            try:
                mail.logout()
            except:
                pass

# Check Outlook recipient inbox
def check_outlook_recipient_status(recipient, subject):
    mail = None
    try:
        mail = imaplib.IMAP4_SSL("outlook.office365.com",993)
        mail.login(recipient, "wwljxtuejtczrmgq")

        # Check Junk folder first
        status, _ = mail.select("Junk Email")
        if status == "OK":
            result, data = mail.search(None, f'(FROM "{sender}" SUBJECT "{subject}")')
            if data and data[0].strip():
                return "Spam"

        # Check Inbox only if not found in Junk
        status, _ = mail.select("Inbox")
        if status == "OK":
            result, data = mail.search(None, f'(FROM "{sender}" SUBJECT "{subject}")')
            if data and data[0].strip():
                return "Inbox"

        return "Not Found"
    except Exception as e:
        return f"Error checking status: {e}"
    finally:
        if mail:
            try:
                mail.logout()
            except:
                pass

# Log test phase results into cvs file
def log_results(results, filename="email_test_log.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(results)

def test_result_module(test_phase):
    print(f"\n--- Checking Test Recipient Inboxes and Assembling Test Results for Test Phase {test_phase} ---")
    # Create list to store test result for each email sent
    email_results = []

    spf_result = check_spf(domain)
    dkim_result = check_dkim(domain)
    dmarc_result = check_dmarc(domain)

    # Check email status by recipient inbox
    for recipient in recipients:
        # Iterate through test cases 1-4
        for a in range(1, 5):
            # Iterate through email templates 1-3
            for b in range(1, 4):
                # Iterating through test email subjects
                if a % 2 == 0:
                    subject = "Test Phase #" + str(test_phase) + " - Test Case #" + str(a) + " - Phish Email #" + str(b)
                    test_id = "P" + str(test_phase) + "-TC" + str(a) + "-PE" + str(b)
                else:
                    subject = "Test Phase #" + str(test_phase) + " - Test Case #" + str(a) + " - Legit Email #" + str(b)
                    test_id = "P" + str(test_phase) + "-TC" + str(a) + "-LE" + str(b)

                # Choose the appropriate checker based on recipient email provider
                if "gmail.com" in recipient:
                    email_status = check_gmail_recipient_status(recipient, subject)
                elif "outlook.ie" in recipient:
                    email_status = "Manual Check Required"
                elif "yahoo.com" in recipient:
                    email_status = "Manual Check Required"

                # Adding email deposition result to the results list
                #email_results.append([str(test_phase), str(a), recipient, test_id, email_status])

                # Option to include current SPF, DKIM and DMARC configuration verified in DNS records for the domain
                email_results.append([str(test_phase), spf_result, dkim_result, dmarc_result, str(a), recipient, test_id, email_status])

    # Printing list of test results to the console
    print("\n--- Displaying Test Results ---")
    for result in email_results:
        print(result)
        log_results(result)

    print("Results logged to CSV file.\n")

    # Testing complete
    print("\n--- Phase " + str(test_phase) + " Result Logging Complete ---")

def main():

    print("\n--- Beginning Test Result Compilation ---")

    # Compile test results for a specific phase of testing and output to CVS file
    test_result_module(4) # change number to correspond with test phase in question

    # Compile test results for each phase of testing and output to CVS file
    '''for test_phase in range(1,5):
        test_result_module(test_phase)'''

    # Testing complete
    print("\n--- All Result Logging Complete ---")

if __name__ == "__main__":
    main()