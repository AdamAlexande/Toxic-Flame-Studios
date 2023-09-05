from flask import Flask, render_template, request
from flask_session import Session
import csv
# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Create a list to store messages and emails
messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        email = request.form.get('email')

        # Save the message and email to the list
        messages.append({'message': message, 'email': email})
        with open('messages.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([message])

        
        return render_template('index.html', messages=messages)
    else:
        return render_template('index.html', messages=messages)

@app.route('/vews')
def vews():

    global messages
    # Read messages from the CSV file
    with open('messages.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        messages = [row[0] for row in reader]

    return render_template('vews.html', messages=messages)

