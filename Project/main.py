from flask import Flask, render_template, request, redirect, url_for, session
# import mysql.connector
import re
from flask_mysqldb import MySQL
import MySQLdb.cursors

from project.src.Table.Exercise.AnswerTable import AnswerTable
from project.src.Table.Exercise.ListExoTable import ListExoTable
from project.src.Table.Exercise.ExerciseTable import ExerciseTable
from project.src.Table.Account.AccountTable import AccountTable
from src.Table.Admin.ClassTable import ClassTable
from src.Table.Admin.SchoolTable import SchoolTable

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = "it's a not funny project"

# Enter your database connection details below
app.config['MYSQL_HOST'] = '192.168.19.9'
app.config['MYSQL_USER'] = 'mamp'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'l3_gpb_web_project_lefebvre_antoine'
# Intialize MySQL
mysql = MySQL(app)


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================


# http://localhost:5000/logout - this will be the logout page
@app.route('/')
def init():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/login - this will be the login page, we need to use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['law'] = account['id']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Login ou mot de passe incorrect'
    # Show the login form with message (if any)
    return render_template('/login/login.html', msg=msg)


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register_<string:val>', methods=['GET', 'POST'])
def register(val):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Output message if something goes wrong...
    msg = ''
    listing = []
    form = {}

    if val == "début":
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Check if account exists using MySQL
            cursor.execute('SELECT * FROM account WHERE username = %s', (request.form['username'],))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', request.form['username']):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', request.form['firstname']):
                msg = 'Username must contain only characters and numbers!'
            elif not request.form['username'] or not request.form['password']:
                msg = 'Please fill out the form!'
            else:
                form['username'] = request.form['username']
                form['password'] = request.form['password']
                form['firstname'] = request.form['firstname']
                form['surname'] = request.form['surname']
                form['law'] = "student"
                session['n_a'] = form
                return redirect(url_for('register', val='école'))
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'

    elif val == "école":
        school = SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all()
        [listing.append(i) for i in school]
        if request.method == 'POST' and 'école' in request.form:
            session['n_a'] = {**session['n_a'], **{'école': request.form["école"]}}
            return redirect(url_for('register', val='classe'))
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'

    elif val == "classe":
        classes = ClassTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).allBySchool(session['n_a']['école'])
        [listing.append(i) for i in classes]

        # ==============================================================================================================
        # ==============================================================================================================
        # ====================================== TOUT METTRE DANS LA VAR SESSION =======================================
        # ==============================================================================================================
        # ==============================================================================================================
        if request.method == 'POST' and 'classe' in request.form:
            cursor.execute('INSERT INTO account (`username`, `password`, `firstname`, `surname`, `law`, `id_class`) '
                           'VALUES (%s, %s, %s, %s, %s, %s) ',
                           (session['n_a']['username'], session['n_a']['password'], session['n_a']['firstname'],
                            session['n_a']['surname'], session['n_a']['law'], int(request.form["classe"])))
            mysql.connection.commit()
            del session['n_a']
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    return render_template('/login/register.html', msg=msg, val=val, listing=listing, form=form)


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================


# http://localhost:5000/accueil - this will be the home page, only accessible for loggedin users
@app.route('/accueil')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        results = AnswerTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).answerTable()
        return render_template('home.html', account=account, result=results)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        classes = ClassTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(account['id_class'])
        school = SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(classes['id_school'])
        return render_template('profile.html', account=account, classes=classes, school=school)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================


@app.route('/admin/list_class')
def list_class():
    # Check if user is loggedin
    if 'loggedin' in session:
        msg = ""
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        school_name = SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).name(account['id_class'])
        classes = ClassTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all()
        return render_template('admin/list_class/index.html', account=account, classes=classes, school_name=school_name, msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_class_new', methods=['GET', 'POST'])
def list_class_new():
    # Check if user is loggedin
    if 'loggedin' in session:
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        msg = ''
        if request.method == 'POST' and 'name' in request.form:
            # Create variables for easy access
            classes = ClassTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info_by_name(request.form['name'])
            # If account exists show error and validation checks
            if classes:
                msg = 'Cette école existe déja !'
            else:
                ClassTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).add(request, mysql, account['id_class'])
                return redirect(url_for('list_class'))
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
        return render_template('admin/list_class/new.html', account=account, msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_class_edit/<int:id>', methods=['GET', 'POST'])
def list_class_edit(id):
    # Check if user is loggedin
    if 'loggedin' in session:
        classes = ClassTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(id)
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        if request.method == 'POST' and 'name' in request.form:
            ClassTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).edit(request, mysql, id)
            return redirect(url_for('list_class'))
        return render_template('admin/list_class/edit.html', account=account, classes=classes, id=id)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_class_delete/<int:id>')
def list_class_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:
        ClassTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).delete(mysql, id)
        return redirect(url_for('list_class'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# ======================================================================================================================


@app.route('/admin/list_school')
def list_school():
    # Check if user is loggedin
    if 'loggedin' in session:
        msg = ""
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        school = SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all()
        return render_template('admin/list_school/index.html', account=account, schools=school, msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_school_new', methods=['GET', 'POST'])
def list_school_new():
    # Check if user is loggedin
    if 'loggedin' in session:
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        msg = ''
        if request.method == 'POST' and 'name' in request.form:
            # Create variables for easy access
            school = SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info_by_name(request.form['name'])
            # If account exists show error and validation checks
            if school:
                msg = 'Cette école existe déja !'
            else:
                SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).add(request, mysql)
                return redirect(url_for('list_school'))
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
        return render_template('admin/list_school/new.html', account=account, msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_school_edit/<int:id>', methods=['GET', 'POST'])
def list_school_edit(id):
    # Check if user is loggedin
    if 'loggedin' in session:
        school = SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(id)
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        if request.method == 'POST' and 'name' in request.form:
            SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).edit(request, mysql, id)
            return redirect(url_for('list_school'))
        return render_template('admin/list_school/edit.html', account=account, school=school, id=id)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_school_delete/<int:id>')
def list_school_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:
        SchoolTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).delete(mysql, id)
        return redirect(url_for('list_school'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# ======================================================================================================================


@app.route('/admin/list_exo')
def list_exo():
    # Check if user is loggedin
    if 'loggedin' in session:
        msg = ""
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        list_exo = ListExoTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info_by_prof(session['id'])
        return render_template('admin/list_exo/index.html', account=account, list_exos=list_exo, msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_exo_new', methods=['GET', 'POST'])
def list_exo_new():
    # Check if user is loggedin
    if 'loggedin' in session:
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        msg = ''
        if request.method == 'POST':
            ListExoTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).add(request, mysql)
            return redirect(url_for('list_exo'))

        # Show registration form with message (if any)
        return render_template('admin/list_exo/new.html', account=account, msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_exo_edit/<int:id>', methods=['GET', 'POST'])
def list_exo_edit(id):
    # Check if user is loggedin
    if 'loggedin' in session:
        school = ListExoTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(id)
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        if request.method == 'POST' and 'name' in request.form:
            ListExoTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).edit(request, mysql, id)
            return redirect(url_for('list_exo'))
        return render_template('admin/list_exo/edit.html', account=account, school=school, id=id)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/list_exo_delete/<int:id>')
def list_exo_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:
        ListExoTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).delete(mysql, id)
        return redirect(url_for('list_exo'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================


@app.route('/exercices_<string:operator>/<string:pos>', methods=['GET', 'POST'])
def exercise(operator, pos):
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        account = AccountTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_info(session['id'])
        if operator == "prof" and pos == "début":
            # list prof exo
            list_exo = ListExoTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor)).all_list_by_prof(account['id_class'])
            return render_template('exo/list_exo.html', account=account, operator=operator, pos=pos, list_exos=list_exo)
        else:
            title = operator if operator in ListExoTable(None).operator().keys() else ExerciseTable(
                mysql.connection.cursor(MySQLdb.cursors.DictCursor), mysql).exo_title(operator[5:])
            if "prof_" in operator and pos == "début":
                # launcher exo
                info_exo = ExerciseTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor), mysql).place(operator, pos, request)
                return render_template('exo/index.html', account=account, operator=operator, pos=pos, info=info_exo, title=title)
            else:
                # aleatory exo
                info_exo = ExerciseTable(mysql.connection.cursor(MySQLdb.cursors.DictCursor), mysql).place(operator, pos, request)
                return render_template('exo/index.html', account=account, operator=operator, pos=pos, info=info_exo, title=title)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================


if __name__ == "__main__":
    app.run(debug=True)