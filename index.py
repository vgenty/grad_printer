# Flask
from flask import Flask, render_template, request, Response, redirect, url_for, flash, abort, session
from flask.ext.script import Manager

# Login
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import login_user , logout_user , current_user , login_required

# File Form
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import SubmitField, TextField, PasswordField, validators
from wtforms.validators import ValidationError
from werkzeug import secure_filename

# Boot
from flask.ext.bootstrap import Bootstrap

# Other
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY']  = 'Bitch'

manager   = Manager(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


        
@app.route('/')
def index():
    return redirect(url_for('login'))

class UserNotFoundError(Exception):
    pass

def next_is_valid(next):
    return True

class User(UserMixin): #Inherit from UsrMixin class
    
    '''Single User'''
    USERS = {
        'norman': 'christ',
    }
    
    def __init__(self, id):
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]
        
    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None

            
@login_manager.user_loader
def load_user(id):
    return User.get(id)

class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    submit   = SubmitField('Submit')
    
@app.route('/login',methods=['GET','POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():

        user = User.get(form.username.data)

        if (user and user.password == form.password.data):
            login_user(user)
        else:
            flash(u'Contact Vic for User/Pass')
            return redirect(url_for('login'))

        # Not sure what this does...
        next = request.args.get('next')
        
        if not next_is_valid(next):
            return abort(400)
        return redirect(next or url_for('upload'))

    return render_template('login.html', form=form)


import re
def allowed_file_types(ftypes): #fancy factory definition
    message = 'Allowed file types are' + str(ftypes)

    def _allowed_file_types(form, field):
        m = re.search(r'.([a-z]{3})$',field.data.filename)
        if m is None or m.group(1) not in ftypes:
            raise ValidationError(message)
        
    return _allowed_file_types

class ToPrintForm(Form):
    document = FileField('Document to Print',validators=[validators.Required(),
                                                         allowed_file_types(['pdf','txt','doc','docx'])])
                         #allowed_max_size)
    submit   = SubmitField('Submit')

import printer
printer = printer.Printer()

@app.route('/upload',methods=['GET','POST'])
@login_required
def upload():

    filename = None
    form = ToPrintForm()
    if form.validate_on_submit():
        filename = secure_filename(form.document.data.filename)
        form.document.data.save('/home/vgenty/web/uploads/' + filename)
        session['filename'] = filename #put filename in cookie!
        printer.send('/home/vgenty/web/uploads/',filename)
    
    return render_template('baka.html', form=form, filename=filename)


if __name__ == '__main__':
    manager.run()
