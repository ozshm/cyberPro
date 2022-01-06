# Communication_LTD
A Web Project as part of the computer security course at HIT college.

## Participants
- Oz Shmuel
- Karin Magriso
- Sharon Guy
- Itzik Israeli
- Or Ezra

## Project objectives:
* Establishment of a Python Django infrastructured Web site based on principles of secure development.
* The Web site includes the following screens:
    - Registration for new users.
    - Login.
    - Change password.
    - Forgot Password for existing user.
    - Clients
* Complexity settings and requirements of the login passwords are managed by a configuration file.
* In case the user had forgotten the login password, a resetting email will be sent.
* SQL Injection (SQLi) and XSS techniques are used.

## How to run the project
- This project was created using the Python Django framework.
- Make sure to create a python virtual environment.

1. Clone this repository to your local computer
2. Install python virtual environment using: 
     - On Mac or Linux run - `python3 -m pip install --user virtualenv`
     - On Windows run - `py -m pip install --user virtualenv`
3. Install python-dotenv on your environment: 
     - `pip install python-dotenv`     
4. Run the server using `python manage.py runserver`
5. Open the terminal and you will see a log with the server IP and the port (default is 8000).
6. Open your web browser and go to localhost:8000

**Website Link** - https://github.com/ozshm/cyberPro.git


## STRIDE Document
The STRIDE document which is part of a system for risk-assessment computer security threats, has been added to this repo.
