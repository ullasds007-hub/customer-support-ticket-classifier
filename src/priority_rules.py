def assign_priority(text):
    text = str(text).lower()

    # --------------------------------------------------
    # HIGH PRIORITY
    # --------------------------------------------------

    high_keywords = [
        "server is down",
        "system is down",
        "network is down",
        "service is down",
        "cannot connect",
        "can't connect",
        "unable to connect",
        "server down",
        "system down",
        "service unavailable",
        "cannot login",
        "can't login",
        "unable to login",
        "account locked",
        "security breach",
        "hacked",
        "malware",
        "virus",
        "data loss",
        "critical",
        "emergency",
        "production issue",
        "network down",
        "cannot access system",
        "system failure"
    ]

    # --------------------------------------------------
    # MEDIUM PRIORITY
    # --------------------------------------------------

    medium_keywords = [
        "shared folder",
        "shared company folder",
        "folder access",
        "access to shared folder",
        "password reset",
        "reset password",
        "reset my password",
        "forgot password",
        "forgot my password",
        "software installation",
        "install software",
        "access request",
        "permission request",
        "shared folder",
        "storage issue",
        "slow system",
        "hardware issue",
        "printer issue",
        "email issue",
        "application error",
        "configuration",
        "update software"
        "purchase",
        "buy",
        "new laptop",
        "new computer",
        "procurement",
    ]

    # --------------------------------------------------
    # CHECK HIGH FIRST
    # --------------------------------------------------

    for keyword in high_keywords:
        if keyword in text:
            return "High"

    # --------------------------------------------------
    # THEN MEDIUM
    # --------------------------------------------------

    for keyword in medium_keywords:
        if keyword in text:
            return "Medium"

    # --------------------------------------------------
    # EVERYTHING ELSE
    # --------------------------------------------------

    return "Low"


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_tickets = [
        "Production server is down and users cannot access system",
        "Please reset my password",
        "I need access to the shared folder",
        "Please provide information about the new software"
    ]

    for ticket in test_tickets:
        priority = assign_priority(ticket)

        print("\nTicket:", ticket)
        print("Priority:", priority)