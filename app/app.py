import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from config import Config
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegistrationForm, ContactForm


app = Flask(__name__)
load_dotenv(".env")
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['APP_MAIL_SUBJECT_PREFIX'] = '[Markkinavisio]'
app.config['APP_MAIL_SENDER'] = 'Markkinavisio <info@markkinavisio.fi>'
app.config['APP_ADMIN'] = os.environ.get('APP_ADMIN')

bootstrap = Bootstrap(app)
mail = Mail(app)
moment = Moment(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))
 
 
    def __init__(self, username, password):
        self.username = username
        self.password = password
 

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', bg_class='bkg')

@app.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html', bg_class='bkg')

@app.route('/resource')
@login_required
def resource():
    return render_template('resource.html', bg_class='bkg')

@app.route('/contact', methods=['GET', 'POST'])
def Contact():
    cform = ContactForm()

    if request.method == 'POST':
        if cform.validate_on_submit():
            mailSender = cform.email.data
            mailSubject = cform.subject.data
            msg = Message(
                subject=mailSubject, 
                sender=mailSender, 
                recipients=['info@markkinavisio.fi'],
                body = cform.message.data)
            mail.send(msg)
            return render_template('contact.html', form=cform, success=True, bg_class='bkg')

    return render_template('contact.html', form=cform, bg_class='bkg')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login' , methods = ['GET', 'POST'])
def Login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
 
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('analysis'))
                flash("Väärä tunnus tai salasana")
    return render_template('login.html', form = form, bg_class='bkg')

@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
 
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        username = form.username.data
        password = hashed_password
 
        new_register =Users(username=username, password=password)
        db.session.add(new_register)
        db.session.commit()
        flash("Rekisteröityminen onnistui, kirjaudu sisään")
        return redirect(url_for('Login'))
    return render_template('registration.html', form=form, bg_class='bkg')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', bg_class='bkg'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', bg_class='bkg'), 500

if __name__ == "__main__":
    app.run()

