from ..      import app
from ..forms import ToPrintForm

from flask import Blueprint, render_template, session
from flask.ext.login import login_required
from werkzeug import secure_filename

import gradprinter.extern.printer as printer


upload = Blueprint('upload',__name__,
                   template_folder = 'templates')


    
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
