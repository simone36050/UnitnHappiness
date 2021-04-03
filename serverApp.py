from flask import Flask, render_template, flash
import re
import os

EMAIL_REGEX = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', warn=os.path.isfile('stop'))

@app.route('/add/<string:email>', methods=['POST'])
def add(email):
    if os.path.isfile('stop'):
        return 'ERR1'
    email = email.lower()

    if re.search(EMAIL_REGEX, email):
        lines = []
        emails = []
        with open('emails.txt', 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '').strip()
            if line != '':
                emails.append(line)
        if not email in emails:
            with open('emails.txt', 'a') as f:
                f.write(email + '\n')
            return "OK"
        else:
            return 'ERR2'
    else:
        return 'ERR3'

if __name__ == "__main__":
        app.run()