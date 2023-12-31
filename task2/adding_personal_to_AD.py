import logging
import pyad.adquery
from pyad import aduser, group, ou
import re
import hashlib
import secrets
import string
import smtplib
from email.mime.text import MIMEText


# Logging setup
logging.basicConfig(filename='logfile.txt', level=logging.INFO,
                    filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')


# Set the AD domain and domain controller
try: 
    pyad.set_defaults(ldap_server="your_domain_controller", username="your_username", password="your_password")
except Exception as e: 
    logging.error(f"Failed to set AD defaults: {e}")
    print("Unexcepted error occured. Please try again. If the problem still exists contact an admin.")

# Initializing global variables.
user_input_username = "";
user_input_email = "";
user_input_password = "";
user_input_department = "";
user_input_job_title = "";
department = None;
group = None;


# Define a function to search for a user by their username
def search_user_by_username(username):
    try:
        q = pyad.adquery.ADQuery()

        # Query, searching for entries with a specific username. 
        q.execute_query(
            attributes=["displayName"],
            where_clause=f'sAMAccountName = "{username}"'
        )
    except pyad.pyadexceptions.ADException as e:
        logging.error(f"Error while searching for user by username: {e}")
        print("Unexcepted error occured. Please try again. If the problem still exists contact an admin.")
        return None
    

    # Checking if username gets found.
    if q.get_row_count() == 0:
        return None
    else:
        user_info = q.get_results()[0]
        return user_info


# Handles user name input. Asks again for input if username already exists.
def handle_input_username(): 
    user_input_username = input("Enter a username to search in Active Directory: ")

    logging.info(f"Given username is: {user_input_username}")


    # Search for the user
    user_info = search_user_by_username(user_input_username)

    # User already exists
    if user_info != None:
        print("User already exists. Choose another username or get in contact with an admin.")
        logging.error("Given username already exists.")
        handle_input_username()

# Checks if email has correct format.
def check_email_format(email): 
    email_pattern = r"^[A-Za-z0-9+_.-]+@(.+)$"
    return bool(re.match(email_pattern, email)) 

# Checks if email has valid format, if not, asks for another email.
def handle_email_input(): 
    user_input_email = input("Enter the email: ")
    logging.info(f"Given Email is: {user_input_email}")
    email_has_correct_format = check_email_format(user_input_email);
    # Checking if email has correct format. If not, as again.
    if not email_has_correct_format: 
        print("Email has wrong format, please check again.")
        logging.info(f"Given email has wrong format.")
        handle_email_input()

# Creates secure and random password.
def create_random_password():
    logging.info("Create random password.")
    alphabet = string.ascii_letters + string.digits
    # Creates 20-character password and returns it.
    random_password = ''.join(secrets.choice(alphabet) for i in range(20))
    return random_password

# Sending the email via gmail smtp server.
def send_mail(subject, body, sender ,recipients, password):
    try: 
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        logging.info("Password got sent")
        print("Password sent!")
    # Error handling of errors while sending the mail.    
    except Exception as e:
        logging.error(f"Error while sending an email: {e}")
        print("Unexcepted error occured. Please restart the script. If the problem still exists contact an admin.")


# Manages the sending of the password by email, given by the user.
def manage_sending_password_mail(): 
    logging.info(f"Sending randomly generated password to the address: {user_input_email}")
    # Setting up email by generating password and assigning attributes.
    password = create_random_password()
    subject = "Automatically generated Password"
    body = f"The automatically set password for your active directory user {user_input_username} is: {user_input_password}. You can change the password any times."
    sender = "sendermail@gmail.com"
    recipients = [user_input_email]
    password = "password"
    send_mail(subject, body, sender, recipients, password)


# Handles the password input. Sets given password, if none is given a new one will be generated and sent by email.
def handle_input_password():
    user_input_password = input("Create new Password or leave empty and  an securely generated password will be send to the email given: ")
    if (user_input_password == ""):
        logging.info("No password given. Email will be sent.")
        manage_sending_password_mail()     

    # Hashing the password with SHA-256.
    sha256 = hashlib.sha256()
    sha256.update(user_input_password.encode('utf-8'))
    
    user_input_password = sha256.hexdigest()




def department_exists(department):
    try: 
        query = pyad.adquery.ADQuery()

        #Filter by the OU's name
        query.execute_query(
            attributes=["name"],
            where_clause="name='{}'".format(department)
        )
    except pyad.pyadexceptions.ADException as e:
        logging.error(f"Error while searching for department: {e}")
        print("Unexcepted error occured. Please try again. If the problem still exists contact an admin.")
        return None

    if query.get_count() > 0: 
        department = query[0]
        return True
    else:
        return False
        

# Handles department input by checking if department exists. If not, asks the user again.
def handle_input_department(): 
    user_input_department = input("Enter your Department: ")
    logging.info(f"The given department is: {user_input_department}")

    # If job does not exist the user is prompted to try again by recalling the function.
    if not department_exists(user_input_department):
        logging.error("Given department does not exist.")
        print(f"Given departement {user_input_department} does not exists. Please try again.")
        handle_input_department()


# Function checking if a given job title exists and can be used for registration.
def job_title_exists(group_name):
    try:
        query = pyad.adquery.ADQuery()

        # Filter by the group's by the given name.
        query.execute_query(
        attributes=["name"],
        where_clause="name='{}'".format(group_name)
        )
    # Error handling if AD is not accessible.
    except pyad.pyadexceptions.ADException as e:
        logging.error(f"Error while searching for job title: {e}")
        print("Unexcepted error occured. Please try again. If the problem still exists contact an admin.")
        return None

    if query.get_count() > 0: 
        group = query[0]
        return True
    else:
        return False

# Handles department input by checking if job exists. If not, asks the user again.
def handle_input_job_title():
    user_input_job_title = input("Enter your Job Title: ")
    logging.info(f"The given Job Title is: {user_input_job_title}")

    # If job does not exist the user is prompted to try again by recalling the function.
    if not job_title_exists(user_input_job_title): 
        print("The given job title does not exist. Please try again.")
        logging.error("Given job title was wrong.")
        handle_input_job_title()


# Sequence of functions, running the script. 
handle_input_username()

handle_email_input()

user_input_address = input("Enter your Address: ")
logging.info(f"Given address is: {user_input_address}")

handle_input_password()

handle_input_department()

handle_input_job_title()

new_user = aduser.ADUser.create(user_input_username, user_input_password, user_input_address, user_input_email)

group.add_member(new_user)

department.parent_container = department

new_user.commit_changes()
