from twilio.rest import Client  # josef, aden
import json  # josef
import datetime  # joseph, jayden
import ssl  # josef
import stripe  # josef
import sys  # josef
from flask_limiter.util import get_remote_address  # Aden
from flask_limiter import Limiter  # Aden
from wtforms.fields.html5 import EmailField
import os
import hashlib
import binascii
import timeit
import re
from flask_uploads import UploadSet, configure_uploads, IMAGES
from functools import wraps
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, abort
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm, RecaptchaField, recaptcha  # josef
from flask_wtf.csrf import CSRFProtect  # josef
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, FloatField, SubmitField
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# jayden
app.permanent_session_lifetime = datetime.timedelta(hours=1)

# Config MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# josef: https
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain("rootCA.pem", "rootCA.key")

# josef: csrf protection
csrf = CSRFProtect(app)

# josef: session protection
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# josef: recaptcha
# reCaptcha site: https://www.google.com/recaptcha/
# josef: key may have to be changed.
app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")

# josef: stripe pamyment system
# Stripe site: https://dashboard.stripe.com/test/dashboard
app.config['STRIPE_PUBLIC_KEY'] = os.getenv("STRIPE_PUBLIC_KEY")
app.config['STRIPE_SECRET_KEY'] = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = app.config['STRIPE_SECRET_KEY']

# aden
limiter = Limiter(app, key_func=get_remote_address,
                  default_limits=["30 per second"])

# josef, aden: twilio 2fa
# client format: Client("<account SID>", "<auth token>")
client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTHTOKEN"))
verify = client.verify.services(os.getenv("TWILIO_VERIFY_SID"))

# Initialize the app for use with this MySQL class
mysql.init_app(app)

# josef, aden: dynamic time
time_limit = 0


# aden: all wrappers
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)
    return wrap


def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))
    return wrap


def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin'))
        else:
            return f(*args, *kwargs)
    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


# josef, jayden: function to add to JSON
def write_json(new_data, key, filename='S4F_log.json'):
    flag = 0
    for val in new_data.values():
        # opening a text file
        with open("sqli.txt", "r") as file1:
            for line in file1:
                if val.find(line.strip()) >= 0:
                    flag = 1  # 1 = sus input
                    break
        # closing text file
        file1.close()

    with open(filename, 'r+') as file:

        # log input time.
        # dd/mm/YY H:M:S
        dt_string = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[key].append(new_data)

        file_data[key][-1]["dt_string"] = dt_string

        # check for sus input
        file_data[key][-1]["flagged_input"] = flag

        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=2)
    file.close()


def content_based_filtering(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s",
                (product_id,))  # getting id row
    data = cur.fetchone()  # get row info
    data_cat = data['category']  # get id category ex shirt
    print('Showing result for Product Id: ' + product_id)
    category_matched = cur.execute(
        "SELECT * FROM products WHERE category=%s", (data_cat,))  # get all shirt category
    print('Total product matched: ' + str(category_matched))
    cat_product = cur.fetchall()  # get all row
    cur.execute("SELECT * FROM product_level WHERE product_id=%s",
                (product_id,))  # id level info
    id_level = cur.fetchone()
    recommend_id = []
    cate_level = ['fruit_juice', 'tropical_fruits', 'temperate_fruit',
                  'plushies', 'vegetables', 'pickle_rick', 'spoiled_meat', 'meat', 'fish']
    for product_f in cat_product:
        cur.execute(
            "SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],))
        f_level = cur.fetchone()
        match_score = 0
        if f_level['product_id'] != int(product_id):
            for cat_level in cate_level:
                if f_level[cat_level] == id_level[cat_level]:
                    match_score += 1
            if match_score == 11:
                recommend_id.append(f_level['product_id'])
    print('Total recommendation found: ' + str(recommend_id))
    if recommend_id:
        cur = mysql.connection.cursor()
        placeholders = ','.join((str(n) for n in recommend_id))
        query = 'SELECT * FROM products WHERE id IN (%s)' % placeholders
        cur.execute(query)
        recommend_list = cur.fetchall()
        return recommend_list, recommend_id, category_matched, product_id
    else:
        return ''


def check_content_length_of_request_decorator(max_content_length):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if int(str(sys.getsizeof(str(request.args))) or 0) > max_content_length:
                return abort(400)
            else:
                return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# josef, aden: dynamic time
def current_time():
    global time_end
    time_end = datetime.datetime.now() + datetime.timedelta(hours=1)
    return time_end


attempts = adminattempts = 0


# joseph
@app.route('/')
@check_content_length_of_request_decorator(1024)
def index():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'fruit'
    cur.execute(
        "SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    fruit = cur.fetchall()
    values = 'vegetable'
    cur.execute(
        "SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    vegetable = cur.fetchall()
    values = 'meat'
    cur.execute(
        "SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    meat = cur.fetchall()
    # joseph removed shoes
    # Close Connection
    cur.close()
    return render_template('home.html', fruit=fruit, vegetable=vegetable, meat=meat, form=form)


class LoginForm(Form):  # Create Login Form
    recaptcha = RecaptchaField()  # josef
    username = StringField('', [validators.length(min=1, max=100)], render_kw={
                           'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3, max=100)], render_kw={
                             'placeholder': 'Password'})


# User Login
@app.route('/login', methods=['GET', 'POST'])
@check_content_length_of_request_decorator(1024)
@not_logged_in
# @limiter.limit("3/hour")  # Aden
def login():
    global attempts  # josef, aden: rate limiter
    if attempts < 3:
        current_time()
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():

            attempts += 1  # josef, aden: rate limiter

            # Get user form
            username = form.username.data
            # password_candidate = request.form['password']
            password_candidate = form.password.data

            # josef, jayden
            log_data = {"username": username}
            write_json(log_data, "user_login")

            # Create cursor
            cur = mysql.connection.cursor()
            # Get user by username
            result = cur.execute(
                "SELECT * FROM users WHERE username=%s", [username])
            if result > 0:
                # Get stored value
                data = cur.fetchone()
                password = data['password']
                uid = data['id']
                name = data['name']

                # aden
                """Verify a stored password against one provided by user"""
                salt = password[:64]
                password = password[64:]
                pwdhash = hashlib.pbkdf2_hmac('sha256',
                                              password_candidate.encode(
                                                  'utf-8'),
                                              salt.encode('ascii'),
                                              100000)
                pwdhash = binascii.hexlify(pwdhash).decode('ascii')
                # Compare password
                if pwdhash == password:

                    attempts = 0  # josef, aden: rate limiter

                    # aden, josef: redirect to 2fa
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "SELECT activation FROM users WHERE id=%s", (uid,))
                    activation = cur.fetchall()
                    if activation[0]["activation"] == "yes":
                        session['uid'] = uid
                        cur.execute(
                            "SELECT mobile FROM users WHERE id=%s", (uid,))
                        mobile = cur.fetchall()[0]['mobile']
                        verify.verifications.create(to=mobile, channel='sms')
                        return redirect(url_for("check2fa"))

                    # passed
                    session['logged_in'] = True
                    session['uid'] = uid
                    session['s_name'] = name
                    x = '1'
                    cur.execute(
                        "UPDATE users SET online=%s WHERE id=%s", (x, uid))
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect username or password entered', 'danger')
                    return render_template('login.html', form=form)
            else:
                flash('Incorrect username or password entered', 'danger')
                # Close connection
                cur.close()
                return render_template('login.html', form=form)
        return render_template('login.html', form=form)
    # josef, aden: rate limiter
    elif datetime.datetime.now() >= time_end:
        attempts = 0
        return redirect(url_for('login'))
    abort(429)  # josef, aden: rate limiter


class Form2fa(Form):  # Create 2fa Form
    code2fa = StringField('', [validators.length(min=6, max=6)], render_kw={
        'autofocus': True, 'placeholder': '2fa code'})


# aden, josef: check 2fa
@app.route("/check2fa", methods=['GET', 'POST'])
@not_logged_in
def check2fa():
    form = Form2fa(request.form)
    if request.method == 'POST' and form.validate():
        # Get user form
        code2fa = form.code2fa.data
        uid = session["uid"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT mobile FROM users WHERE id=%s", (uid,))
        mobile = cur.fetchall()[0]['mobile']
        cur.close()
        result = verify.verification_checks.create(to=mobile, code=code2fa)
        if result.status == "approved":
            cur = mysql.connection.cursor()
            cur.execute("SELECT name FROM users WHERE id=%s", (uid,))
            name = cur.fetchall()[0]['name']
            # passed
            session['logged_in'] = True
            session['uid'] = uid
            session['s_name'] = name
            x = '1'
            cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
            cur.close()
            flash('successful login & 2fa.', 'success')
            return redirect(url_for('index'))
        elif result.status == "pending":
            flash('unsuccessful 2fa.', 'danger')
            return redirect(url_for('login'))
        print("\n random")
    return render_template('check2fa.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))


# Aden
class RegisterForm(Form):
    recaptcha = RecaptchaField()  # josef
    name = StringField('', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    username = StringField('', [validators.length(min=3, max=25)], render_kw={
                           'placeholder': 'Username'})
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('', [validators.length(min=3, max=100)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('', [validators.length(min=8, max=11)], render_kw={
                         'placeholder': 'Mobile'})

    def validate_password(self, field):
        if not re.search("[a-z]", field.data):
            raise validators.ValidationError("Minimum 1 lowercase.")
        elif not re.search("[A-Z]", field.data):
            raise validators.ValidationError("Minimum 1 uppercase.")
        elif not re.search("[0-9]", field.data):
            raise validators.ValidationError("Minimum 1 numerical digit.")
        elif not re.search("[@%+/!#$^?:,()]", field.data):
            raise validators.ValidationError("Minimum 1 special character.")
        elif re.search("\s", field.data):
            raise validators.ValidationError("No whitespace.")


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        # aden
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        password = hashlib.pbkdf2_hmac('sha256', form.password.data.encode('utf-8'),
                                       salt, 100000)
        password = (salt + binascii.hexlify(password)).decode('ascii')
        mobile = form.mobile.data

        # josef, jayden
        log_data = {"name": name,
                    "email": email,
                    "username": username,
                    "mobile": mobile
                    }
        write_json(log_data, "user_signup")

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password, mobile) VALUES(%s, %s, %s, %s, %s)",
                    (name, email, username, password, mobile))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


# joseph
class OrderForm(Form):  # Create Order Form
    recaptcha = RecaptchaField()  # josef
    quantity = SelectField('', [validators.DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('', [validators.length(min=1, max=100), validators.DataRequired()],
                              render_kw={'placeholder': 'Order Place'})


# joseph
@app.route('/fruit', methods=['GET', 'POST'])
@check_content_length_of_request_decorator(1024)
def fruit():
    session.pop("ordered", None)  # delete session for ordered
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'fruit'
    cur.execute(
        "SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()
    if request.method == 'POST' and form.validate():
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        cur = mysql.connection.cursor()
        cur.execute("SELECT api_id FROM products WHERE id=%s ", (pid,))
        api_id = cur.fetchall()[0]["api_id"]
        mysql.connection.commit()
        cur.close()

        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']

            curs.execute("INSERT INTO orders(uid, pid, oplace, quantity, ddate, api_id) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (uid, pid, order_place, quantity, now_time, api_id))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        if 'order' in request.args:

            # josef: get id from orders & store as session
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
            oid = cur.fetchall()[0]["id"]
            session["oid"] = oid
            session["ordered"] = True
            mysql.connection.commit()
            cur.close()

            product_id = request.args['order']
            curso = mysql.connection.cursor()
            curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
            product = curso.fetchall()
            x = content_based_filtering(product_id)
            return render_template('order_product.html', x=x, fruits=product, form=form)
        return render_template('fruit.html', fruit=products, form=form)
    if 'view' in request.args:
        product_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        wrappered = wrappers(content_based_filtering, product_id)
        execution_time = timeit.timeit(wrappered, number=0)
        # print('Execution time: ' + str(execution_time) + ' usec')
        if 'uid' in session:
            uid = session['uid']
            # Create cursor
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM product_view WHERE user_id=%s AND product_id=%s", (uid, product_id))
            result = cur.fetchall()
            if result:
                now = datetime.datetime.now()
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                cur.execute("UPDATE product_view SET date=%s WHERE user_id=%s AND product_id=%s",
                            (now_time, uid, product_id))
        return render_template('view_product.html', x=x, fruits=product)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, fruits=product, form=form)
    return render_template('fruit.html', fruit=products, form=form)


# josef
@app.route('/vegetable', methods=['GET', 'POST'])
@check_content_length_of_request_decorator(1024)
def vegetable():
    session.pop("ordered", None)  # delete session for ordered
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'vegetable'
    cur.execute(
        "SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        cur = mysql.connection.cursor()
        cur.execute("SELECT api_id FROM products WHERE id=%s ", (pid,))
        api_id = cur.fetchall()[0]["api_id"]
        mysql.connection.commit()
        cur.close()

        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']

            curs.execute("INSERT INTO orders(uid, pid, oplace, quantity, ddate, api_id) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (uid, pid, order_place, quantity, now_time, api_id))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        if 'order' in request.args:

            # josef: get id from orders & store as session
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
            oid = cur.fetchall()[0]["id"]
            session["oid"] = oid
            session["ordered"] = True
            mysql.connection.commit()
            cur.close()

            product_id = request.args['order']
            curso = mysql.connection.cursor()
            curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
            product = curso.fetchall()
            x = content_based_filtering(product_id)
            return render_template('order_product.html', x=x, fruits=product, form=form)
        return render_template('vegetable.html', vegetable=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, fruits=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, fruits=product, form=form)
    return render_template('vegetable.html', vegetable=products, form=form)


# josef
@app.route('/meat', methods=['GET', 'POST'])
@check_content_length_of_request_decorator(1024)
def meat():
    session.pop("ordered", None)  # delete session for ordered

    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'meat'
    cur.execute(
        "SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        cur = mysql.connection.cursor()
        cur.execute("SELECT api_id FROM products WHERE id=%s ", (pid,))
        api_id = cur.fetchall()[0]["api_id"]
        mysql.connection.commit()
        cur.close()

        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']

            curs.execute("INSERT INTO orders(uid, pid, oplace, quantity, ddate, api_id) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (uid, pid, order_place, quantity, now_time, api_id))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        if 'order' in request.args:

            # josef: get id from orders & store as session
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
            oid = cur.fetchall()[0]["id"]
            session["oid"] = oid
            session["ordered"] = True
            mysql.connection.commit()
            cur.close()

            product_id = request.args['order']
            curso = mysql.connection.cursor()
            curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
            product = curso.fetchall()
            x = content_based_filtering(product_id)
            return render_template('order_product.html', x=x, fruits=product, form=form)
        return render_template('meat.html', meat=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, fruits=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, fruits=product, form=form)
    return render_template('meat.html', meat=products, form=form)


# josef: stripe
@app.route('/stripe_pay')
def stripe_pay():
    if not session.get("oid"):
        return redirect(url_for('index'))
    try:
        oid = session['oid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT api_id, quantity FROM orders WHERE id=%s", (oid,))
        order = cur.fetchall()
        api_id = order[0]['api_id']
        quantity = order[0]['quantity']
        mysql.connection.commit()
        cur.close()
    except:
        return render_template(url_for('index'))
    # trying to get session['oid'] here
    sessione = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': api_id,  # price id
            'quantity': quantity,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + \
        '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': sessione['id'],
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }


# josef: webhook for stripe for secure transactions
@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = os.getenv("STRIPE_ENDPOINT_SECRET")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(
            session['id'], limit=1)
        print(line_items['data'][0]['description'])
    return {}


# josef: page after orders
@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


class AdminLoginForm(Form):  # Create Login Form
    recaptcha = RecaptchaField()  # josef
    email = StringField('', [validators.length(min=1, max=100)], render_kw={
                           'autofocus': True, 'placeholder': 'Email'})
    password = PasswordField('', [validators.length(min=3, max=100)], render_kw={
                             'placeholder': 'Password'})


@app.route('/admin_login', methods=['GET', 'POST'])
@check_content_length_of_request_decorator(1024)
@not_admin_logged_in
# @limiter.limit("3/hour")  # Aden
def admin_login():
    global adminattempts  # josef, aden: rate limiter
    if adminattempts < 3:
        current_time()
        form = AdminLoginForm(request.form)
        print("yes")
        if request.method == 'POST' and form.validate():
            print("yesyesy")
            adminattempts += 1

            # GEt user form
            username = form.email.data
            password_candidate = form.password.data

            # josef, jayden
            log_data = {"email": username}
            write_json(log_data, "admin_login")

            # Create cursor
            cur = mysql.connection.cursor()

            # Get user by username
            result = cur.execute(
                "SELECT * FROM admin WHERE email=%s", [username])

            if result > 0:
                # Get stored value
                data = cur.fetchone()
                password = data['password']
                uid = data['id']
                name = data['firstName']

                # aden
                """Verify a stored password against one provided by user"""
                salt = password[:64]
                password = password[64:]
                pwdhash = hashlib.pbkdf2_hmac('sha256',
                                              password_candidate.encode(
                                                  'utf-8'),
                                              salt.encode('ascii'),
                                              100000)
                pwdhash = binascii.hexlify(pwdhash).decode('ascii')
                # Compare password
                if pwdhash == password:

                    adminattempts = 0  # josef, aden: rate limiter

                    # passed
                    session['admin_logged_in'] = True
                    session['admin_uid'] = uid
                    session['admin_name'] = name

                    return redirect(url_for('admin'))

                else:
                    flash('Incorrect password', 'danger')
                    return render_template('pages/login.html', form=form)
            else:
                flash('Username not found', 'danger')
                # Close connection
                cur.close()
                return render_template('pages/login.html', form=form)
        return render_template('pages/login.html', form=form)

    elif datetime.datetime.now() >= time_end:
        adminattempts = 0
        return redirect(url_for('admin'))
    abort(429)  # josef, aden: rate limiter


@app.route('/admin_out')
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))


@app.route('/admin')
@is_admin_logged_in
def admin():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    result = curso.fetchall()
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    return render_template('pages/index.html', result=result, row=num_rows, order_rows=order_rows, users_rows=users_rows)


@app.route('/orders')
@is_admin_logged_in
def orders():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    result = curso.fetchall()
    users_rows = curso.execute("SELECT * FROM users")
    return render_template('pages/all_orders.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/users')
@is_admin_logged_in
def users():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    result = curso.fetchall()
    return render_template('pages/all_users.html', result=result, row=num_rows, order_rows=order_rows, users_rows=users_rows)


@app.route('/admin_add_product', methods=['POST', 'GET'])
@is_admin_logged_in
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form['price']
        description = request.form['description']
        available = request.form['available']
        category = request.form['category']
        item = request.form['item']
        code = request.form['code']
        file = request.files['picture']
        if name and price and description and available and category and item and code and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                save_photo = photos.save(file, folder=category)
                if save_photo:
                    # Create Cursor
                    curs = mysql.connection.cursor()
                    curs.execute("INSERT INTO products(pName,price,description,available,category,item,pCode,picture)"
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (name, price, description, available, category, item, code, picture))
                    mysql.connection.commit()
                    product_id = curs.lastrowid
                    curs.execute(
                        "INSERT INTO product_level(product_id)" "VALUES(%s)", [product_id])
                    if category == 'fruit':
                        level = request.form.getlist('fruit')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    elif category == 'vegetable':
                        level = request.form.getlist('vegetable')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    elif category == 'meat':
                        level = request.form.getlist('meat')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    else:
                        flash('Product level not fund', 'danger')
                        return redirect(url_for('admin_add_product'))
                    # Close Connection
                    curs.close()

                    flash('Product added successful', 'success')
                    return redirect(url_for('admin_add_product'))
                else:
                    flash('Picture not save', 'danger')
                    return redirect(url_for('admin_add_product'))
            else:
                flash('File not supported', 'danger')
                return redirect(url_for('admin_add_product'))
        else:
            flash('Please fill up all form', 'danger')
            return redirect(url_for('admin_add_product'))
    else:
        return render_template('pages/add_product.html')


@app.route('/edit_product', methods=['POST', 'GET'])
@is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute(
            "SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        curso.execute(
            "SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        product_level = curso.fetchall()
        if res:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form['price']
                description = request.form['description']
                available = request.form['available']
                category = request.form['category']
                item = request.form['item']
                code = request.form['code']
                file = request.files['picture']
                # Create Cursor
                if name and price and description and available and category and item and code:
                    save_photo = None
                    print("file is", file.filename)
                    if file.filename != "":
                        pic = file.filename
                        photo = pic.replace("'", "")
                        picture = photo.replace(" ", "")
                        if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                            file.filename = picture
                            save_photo = photos.save(file, folder=category)
                        else:
                            flash('File not support', 'danger')
                            return render_template('pages/edit_product.html', product=product,
                                                   product_level=product_level)

                    cur = mysql.connection.cursor()
                    if save_photo:
                        # Create Cursor
                        exe = curso.execute(
                            "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                            (name, price, description, available, category, item, code, picture, product_id))
                    else:
                        exe = curso.execute(
                            "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s WHERE id=%s",
                            (name, price, description, available, category, item, code, product_id))

                    if exe:
                        mysql.connection.commit()
                        flash('Product updated', 'success')
                        return redirect(url_for('edit_product'))
                    else:
                        flash('Data updated', 'success')
                        return redirect(url_for('edit_product'))

                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_product.html', product=product,
                                           product_level=product_level)
            else:
                return render_template('pages/edit_product.html', product=product, product_level=product_level)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))


# logging: josef, jayden
@app.route('/admin_logging')
@is_admin_logged_in
def admin_logging():
    # Opening JSON file
    f = open('S4F_log.json', "r+")

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    f.close()
    return render_template('pages/logging.html', data=data)


@app.route('/logging_user_login')
@is_admin_logged_in
def logging_user_login():
    # Opening JSON file
    f = open('S4F_log.json', "r+")

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    f.close()
    return render_template('pages/user_login.html', data=data)


@app.route('/logging_admin_login')
@is_admin_logged_in
def logging_admin_login():
    # Opening JSON file
    f = open('S4F_log.json', "r+")

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    f.close()
    return render_template('pages/admin_login.html', data=data)


@app.route('/logging_search')
@is_admin_logged_in
def logging_search():
    # Opening JSON file
    f = open('S4F_log.json', "r+")

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    f.close()
    return render_template('pages/search.html', data=data)


# josef
@app.route('/search', methods=['POST', 'GET'])
@check_content_length_of_request_decorator(1024)
def search():
    form = OrderForm(request.form)
    if 'q' in request.args:
        q = request.args['q']

        # josef, jayden
        log_data = {"query": q}
        write_json(log_data, "search")

        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        query_string = "SELECT * FROM products WHERE pName LIKE %s ORDER BY id ASC"
        cur.execute(query_string, ('%' + q + '%',))
        products = cur.fetchall()
        # Close Connection
        cur.close()
        flash('Showing result for: ' + q, 'success')
        return render_template('search.html', products=products, form=form)
    else:
        flash('Search again', 'danger')
        return render_template('search.html')


@app.route('/profile')
@is_logged_in
def profile():
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                curso.execute(
                    "SELECT * FROM orders WHERE uid=%s ORDER BY id ASC", (session['uid'],))
                res = curso.fetchall()
                return render_template('profile.html', result=res)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


# Aden
class UpdateRegisterForm(Form):
    name = StringField('Full Name', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    email = EmailField('Email', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', [validators.length(min=3, max=100)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('Mobile', [validators.length(
        min=8, max=11)], render_kw={'placeholder': 'Mobile'})
    activation = SelectField("2FA", choices=[("yes", "yes"), ("no", "no")])


@app.route('/settings', methods=['POST', 'GET'])
@is_logged_in
def settings():
    form = UpdateRegisterForm(request.form)
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                if request.method == 'POST' and form.validate():
                    name = form.name.data
                    email = form.email.data
                    salt = hashlib.sha256(os.urandom(
                        60)).hexdigest().encode('ascii')
                    password = hashlib.pbkdf2_hmac(
                        'sha256', form.password.data.encode('utf-8'), salt, 100000)
                    password = (salt + binascii.hexlify(password)
                                ).decode('ascii')
                    mobile = form.mobile.data
                    activation = form.activation.data
                    # Create Cursor
                    cur = mysql.connection.cursor()
                    exe = cur.execute("UPDATE users SET name=%s, email=%s, password=%s, mobile=%s, activation=%s WHERE id=%s",
                                      (name, email, password, mobile, activation, q))
                    if exe:
                        flash('Profile updated', 'success')
                        return render_template('user_settings.html', result=result, form=form)
                    else:
                        flash('Profile not updated', 'danger')
                return render_template('user_settings.html', result=result, form=form)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


# Aden
@app.errorhandler(429)
def page_not_found(e):
    # josef, aden: dynamic time
    timediff = str(time_end - datetime.datetime.now())
    return render_template('ratelimit.html', timediff=timediff[:7])


# josef: error page for DDOS
@app.errorhandler(400)
def page_not_found2(e):
    return render_template('error400.html')


if __name__ == '__main__':
    app.run(debug=True, ssl_context=context)
