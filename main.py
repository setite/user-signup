from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

# separate functins for validations

def empty_value(x):
    if x:
        return True
    else:
        return False

def char_length(x):
    if len(x) > 2 and len(x) < 21:
        return True
    else:
        return False

def email_at_symbol(x):
    if x.count('@') >= 1:
        return True
    else:
        return False

def email_at_symbol_more_than_one(x):
    if x.count('@') <= 1:
        return True
    else:
        return False

def email_period(x):
    if x.count('.') >= 1:
        return True
    else:
        return False

def email_period_more_than_one(x):
    if x.count('.') <= 1:
        return True
    else:
        return False

# THIS CREATES ROUTE TO PROCESS AND VALIDATE THE FORM

@app.route("/")
def index():
    # encoded_error = request.args.get("error")
    return render_template('index.html')

# signup landing page
@app.route('/signup')
def signup_form():
    return render_template('index.html')
    
# POST version of signup page
@app.route("/signup", methods=['POST'])
def signup_complete():

    # empty strings for error placeholders

    username_error          = ""
    password_error          = ""
    password_verify_error = ""
    email_error             = ""

    # creating string variales for repetitive errors

    error_required      = "This is a required field"
    error_pw_reenter    = "Please re-enter password"
    error_char_count    = "must be between 3 and 20 characters"
    error_spaces        = "must contain NO spaces"
    
    # create variables from the forms

    username            = request.form['username']
    password            = request.form['password']
    password_verify     = request.form['password_verify']
    email               = request.form['email']

    # password validation nested conditionals

    if not empty_value(password):
        password_error = error_required
        password = ''
        password_verify = ''
    elif not char_length(password):
        password_error = "Password " + error_char_count
        password = ''
        password_verify = ''
        password_verify_error = error_pw_reenter
    else:
        if " " in password:
            password_error = "Password " + error_spaces
            password = ''
            password_verify = ''
            password_verify_error = error_pw_reenter

    # retyped password validation, a simple one

    if password_verify != password:
        password_verify_error = "Passwords must match"
        password = ''
        password_verify = ''
        password_error = 'Passwords must match'
            
    # username validation nested conditionals

    if not empty_value(username):
        username_error = error_required
        password = ''
        password_verify = ''
        password_error = error_pw_reenter
        password_verify_error = error_pw_reenter
    elif not char_length(username):
        username_error = "Username " + error_char_count
        password = ''
        password_verify = ''
        password_error = error_pw_reenter
        password_verify_error = error_pw_reenter
    else:
        if " " in username:
            username_error = "Username " + error_spaces
            password = ''
            password_verify = ''
            password_error = error_pw_reenter
            password_verify_error = error_pw_reenter

    # email validation nested conditionals

    # checks to see if email contains text prior to running validations

    if empty_value(email):
        if not char_length(email):
            email_error = "Email " + error_char_count
            password = ''
            password_verify = ''
            password_error = error_pw_reenter
            password_verify_error = error_pw_reenter
        elif not email_at_symbol(email):
            email_error = "Email must contain the @ symbol"
            password = ''
            password_verify = ''
            password_error = error_pw_reenter
            password_verify_error = error_pw_reenter
        elif not email_at_symbol_more_than_one(email):
            email_error = "Email must contain only one @ symbol"
            password = ''
            password_verify = ''
            password_error = error_pw_reenter
            password_verify_error = error_pw_reenter
        elif not email_period(email):
            email_error = "Email must contain . (period)"
            password = ''
            password_verify = ''
            password_error = error_pw_reenter
            password_verify_error = error_pw_reenter
        elif not email_period_more_than_one(email):
            email_error = "Email must contain only one . (period)"
            password = ''
            password_verify = ''
            password_error = error_pw_reenter
            password_verify_error = error_pw_reenter
        else:
            if " " in email:
                email_error = "Email " + error_spaces
                password = ''
                password_verify = ''
                password_error = error_pw_reenter
                password_verify_error = error_pw_reenter

    # if the entries are clean, you get a welcoming page
    # otherwise you get a reconstituted page with errors

    if not username_error and not password_error and not password_verify_error and not email_error:
        username = username
        return redirect('/welcome?username={0}'.format(username))
    else:
        return render_template('index.html', username=username, password=password, password_verify=password_verify, email=email, username_error=username_error, password_error=password_error, password_verify_error=password_verify_error, email_error=email_error)

    # return render_template('add-confirmation.html')

@app.route('/welcome')
def valid_signup():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)
    
# , username=username, password=password, password_verify=password_verify, email=email,
#     username_error=username_error, password_error=password_error, password_verify_error=password_verify_error, email_error=email_error
app.run()
