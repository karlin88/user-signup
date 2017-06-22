from flask import Flask, request, redirect, render_template, url_for
import re

app = Flask(__name__)
app.config['DEBUG'] = True

def lengthnotvalid(string):
    if len(string) < 3 or len(string) > 20:
        return True
    else:
        return False

def doesnotexist(string):
    if not string or string.strip() == "":
        return True
    else:
        return False

def emailnotvalid(string):
    print(string.count('@'))
    print(string.count('.'))
    if string.count('@') == 1 and string.count('.') == 1:
        return False
    else:
        return True

def convertstrtoblank(string):
    if string is None:
        return ''
    else:
        return string


@app.route("/", methods = ['POST'])
def signup():
    Username = request.form['Username']
    Password = request.form['Password']
    VerifyPass = request.form['VerifyPass']
    Email = request.form['EmailOptional']
    error = 0
    username_error = ""
    pass_error = ""
    vpass_error = ""
    email_error = ""

    #Username validation
    if lengthnotvalid(Username) or doesnotexist(Username):
        error = 1
        username_error = "Username is not valid.\n"

    #Password Validation
    if doesnotexist(Password):
        error = 1
        pass_error = "Password has not been set."
    elif lengthnotvalid(Password):
        error = 1
        pass_error = "Password is not long enough."

    #Verify Passwords Match
    if Password != VerifyPass:
        error = 1
        vpass_error = "Passwords do not match."

    #Verify Email
    if doesnotexist(Email):
        error = 0
    elif lengthnotvalid(Email) or emailnotvalid(Email):
        error = 1
        email_error = "Email is not valid."
    
    if error != 1:
        return redirect(url_for('confirmed', Username = Username))
    else:
        return redirect(url_for('index', 
            Username = Username,
            Email = Email,
            username_error = username_error,
            pass_error = pass_error,
            vpass_error = vpass_error,
            email_error = email_error            
        ))


@app.route("/")
def index():
    er = request.args.get('error')
    username = request.args.get('Username')
    email = request.args.get('Email')
    username_error = request.args.get('username_error')
    pass_error = request.args.get('pass_error')
    vpass_error = request.args.get('vpass_error')
    email_error = request.args.get('email_error')
    return render_template('form.html', 
        error = convertstrtoblank(er), 
        Username = convertstrtoblank(username), 
        Email = convertstrtoblank(email),
        username_error = convertstrtoblank(username_error),
        pass_error = convertstrtoblank(pass_error),
        vpass_error = convertstrtoblank(vpass_error),
        email_error = convertstrtoblank(email_error) 
        )


@app.route("/confirmed/")
def confirmed():
    return render_template('confirmed.html', Username = request.args.get('Username'))


app.run()