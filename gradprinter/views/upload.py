from .. import app

from flask import Blueprint, render_template, session
from flask_wtf import Form
from flask_wtf.file import FileField
from flask.ext.login import login_required


from wtforms import SubmitField, validators
from wtforms.validators import ValidationError

from werkzeug import secure_filename

import re
import gradprinter.extern.printer as printer

upload = Blueprint('upload',__name__,
                   template_folder = 'templates')

def allowed_file_types(ftypes): #fancy factory definition
    message = 'Allowed file types are' + str(ftypes)
    
    def _allowed_file_types(form, field):
        m = re.search(r'.([a-z]{3})$',field.data.filename)
        if m is None or m.group(1) not in ftypes:
            raise ValidationError(message)
        
    return _allowed_file_types


class ToPrintForm(Form):
    document = FileField('Document to Print',
                         validators=[validators.Required(),
                                     allowed_file_types(app.config['ALLOWED_FILE_TYPES'])])
    submit   = SubmitField('Submit')
    
    
printer = printer.Printer()

@upload.route('/upload',methods=['GET','POST'])
@login_required
def upload_to_server():

    filename = None
    form     = ToPrintForm()
    
    if form.validate_on_submit():
        filename = secure_filename(form.document.data.filename)
        form.document.data.save(app.config['UPLOAD_FOLDER'] + filename)
        session['filename'] = filename #put filename in the damn cookie!
        printer.send(app.config['UPLOAD_FOLDER'],filename)
    
    return render_template('upload.html', form=form, filename=filename)
