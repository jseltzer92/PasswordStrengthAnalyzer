import re
import hashlib
import requests
import datetime
from colorama import Fore, Style

def analyze_password(password):
    """Evaluate the strength of a password and provide suggestions."""
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Your password is too short. Use at least 12 characters.")

    # Uppercase check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # Digital Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include at least one number.")

    # Special Character Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Use special characters like @, #, $, etc.")

    # Common Patterns Check
    common_patterns = ["123456", "password", "qwerty", "abc123", "letmein", "admin"]
    if any(pattern in password.lower() for pattern in common_patterns):
        feedback.append("Avoid common patterns like '123456', 'password', etc.")
        score -= 1

    # Display Results
    print("\nPassword Strength Evaluation")
    print("_" * 30)
    if score >= 6:
        print(Fore.GREEN + "Strong password!" + Style.RESET_ALL)
    elif score >= 4:
        print(Fore.YELLOW + "Moderate password. Consider improving it." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Weak password. You need tto improve it." + Style.RESET_ALL)

    if feedback:
        print("\nSuggestions for Improvements:")
        for suggestion in feedback:
            print(Fore.CYAN + f"- {suggestion}" + Style.RESET_ALL)

    print("\nScore:", score, "/ 6")

    # Save to File
    save_to_file(password, feedback, score)

def save_to_file(password, feedback, score):
    """Save password evaluation results to a text file."""
    with open("password_analysis.txt", "a") as file:
        # Add a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%d %H:%M:%S")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Password: {password}\n")
        file.write(f"Score: {score}/6\n")
        
        # Include feedback
        if feedback:
            file.write("Suggestions:\n")
            for suggestion in feedback:
                file.write(f"- {suggestion}\n")
        
        # Add a seperator
        file.write("-" * 50 + "\n\n")

def check_breach(password):
    """Check if the password has been part of a data breach."""
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[:5]
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if suffix in response.text:
        print("⚠️ Your password has been found in a data breach! Avoid using it.")
    else:
        print("✅ Your password has not been found in any known breaches.")
    
def real_time_evaluation():
    """Evaluate password strength in real-time as the user types."""
    print("Start typing your password (press Enter when done):")
    password = ""
    while True:
        char = input("Add character (press Enter to finish):")
        if char == "":
            break
        password += char
        print(f"Current Password: {password}")
        analyze_password(password)
        check_breach(password)

if __name__ == "__main__":
    real_time_evaluation()  