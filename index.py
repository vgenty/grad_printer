# Flask
from flask import Flask, render_template, request, Response, redirect, url_for, flash, abort
from flask.ext.script import Manager

# Login
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import login_user , logout_user , current_user , login_required

# File Form
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import SubmitField, TextField, PasswordField, validators
from werkzeug import secure_filename

# Boot
from flask.ext.bootstrap import Bootstrap

# Other
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY']  = 'Bitch'

manager   = Manager(app)
bootstrap = Bootstrap(app)


        
@app.route('/')
def index():
    return redirect(url_for('login'))

class UserNotFoundError(Exception):
    pass

def next_is_valid(next):
    return True

class User(UserMixin): #Inherit from UsrMixIn
    
        '''Single User'''
        USERS = {
            # username: password
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
            
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
            flash('Username or password incorrect')
            return redirect(url_for('login'))
             
        flash(u'Successfully logged in as %s' % form.username.data)

        next = request.args.get('next')
        print next
        
        if not next_is_valid(next):
            return abort(400)
        return redirect(next or url_for('upload'))

    return render_template('login.html', form=form)


class ToPrintForm(Form):
    document = FileField('Document to Print',validators=[validators.Required()])
    submit   = SubmitField('Submit')
    
@app.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    name  = None
    error = None
    form = ToPrintForm()
    if form.validate_on_submit():
        filename = secure_filename(form.document.data.filename)
        form.document.data.save('/home/vgenty/web/uploads/' + filename)
        
        
    return render_template('baka.html', form=form)

if __name__ == '__main__':
    manager.run()


    
# def check_auth(username, password):
#     """This function is called to check if a username /
#     password combination is valid.
#     """
#     return username == 'admin' and password == 'secret'
# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     return Response(
#         'Could not verify your access level for that URL.\n'
#         'You have to login with proper credentials', 401,
#         {'WWW-Authenticate': 'Basic realm="Login Required"'})

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return authenticate()
#         return f(*args, **kwargs)
#     return decorated
