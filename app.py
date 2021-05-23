from flask import Flask, flash, render_template, request, redirect, url_for, session
import json
app = Flask(__name__)


@app.route('/')
@app.route('/login')
def login():
    if userAuth():
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')


@app.route('/validateUser', methods = ['GET', 'POST'])
def validateUser():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        with open('credentials.json') as userFile:
            userCreds = json.load(userFile)

            if check_user_exists(userCreds['username'], username, password):
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect Username / Password")
                return redirect(url_for('login'))
                #return render_template('login.html', msg = msg)  
    else:
        return redirect(url_for('login'))


@app.route('/register')
def register():
    if userAuth():
        return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')


@app.route('/validateNewUser', methods = ['GET', 'POST'])
def validateNewUser():
    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if username == '' or password == '':
            msg = "Username Or Password cannot be Blank!"
            return render_template('register.html', msg = msg)
        with open('credentials.json', 'r+') as userFile:
            userCreds = json.load(userFile)

            if check_user_exists(userCreds['username'], username, password, newuser=True):
                msg = 'User Already Register, Please contact Admin for Login Credentials or Try Login.'
                return render_template('register.html',msg = msg)
            else:
                userDetail = {username: password}
                userCreds['username'].update(userDetail)
                userFile.seek(0)
                json.dump(userCreds, userFile, indent=4)
                flash("You Have Successfully Registered ! Please Login Now...")
                return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if userAuth():
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))    


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


def check_user_exists(userCreds, username, password, newuser=False):
    try:
        if newuser == True:
            if username in userCreds:
                return True
            return False

        elif username in userCreds:
            if password in userCreds[username]:
                return True    
        else:
            return False    
    except Exception as e:
        return False


def userAuth():
    if session.get('loggedin') == True and session.get('username') is not None:
        return True
    return False
    



if __name__ == '__main__':
    app.secret_key = 'DocLogs'
    app.run(debug = True)
