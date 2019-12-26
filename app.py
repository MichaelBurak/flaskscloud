from flask import Flask, render_template, send_file, make_response, Response, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug import secure_filename
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import stylecloud
from PIL import Image
import io
import matplotlib
matplotlib.use('TkAgg')

import os 

app = Flask(__name__,static_url_path='/static')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['SECRET_KEY'] = 'mysecretkey'


OUTPUT_NAME = "./static/out.png"


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class MyForm(FlaskForm):
    txt =  TextAreaField('Enter Text Here!')
    color = StringField("Select a solid color for text if you want")
    bgcolor = StringField('Select a background color')
    submit = SubmitField('Submit')


class UploadForm(FlaskForm):
    file = FileField()


def sc(tx=None, bg="white", clr=None, fp=None):

    if bg == "":
        bg = "white"
    
    if clr == "":
        clr = None
    
    stylecloud.gen_stylecloud(text=tx,
                              background_color=bg, output_name=OUTPUT_NAME, colors=clr, file_path=fp)
    pil_im = Image.open(OUTPUT_NAME)
    file_object = io.BytesIO()

    # write PNG in file-object
    pil_im.save(file_object, 'PNG')

    # move to beginning of file so `send_file()` it will read from start
    file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')

@app.route('/', methods=('GET', 'POST'))
def index():
    form = MyForm()
    img = []
    
    place = ""
    if form.validate_on_submit():
        img = sc(form.txt.data,form.bgcolor.data, form.color.data)
        resp = make_response(render_template('img.html')) #here you could use make_response(render_template(...)) too
        resp.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        resp.headers['Cache-Control'] = 'public, max-age=0'
        return resp
    return render_template('index.html', img=img, form=form, place=place)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        path = 'static/text.txt'
        form.file.data.save(path)
        sc(fp=path)
        resp = make_response(render_template('img.html')) #here you could use make_response(render_template(...)) too
        resp.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        resp.headers['Cache-Control'] = 'public, max-age=0'
        return resp

    return render_template('upload.html', form=form)

@app.route('/img')
def img():
    return render_template('img.html', img=img)

@app.route('/sepia')
def sepia():
    return render_template('sepia.html')

if __name__ == '__main__':
    app.run(debug=True, port=9000)
    #debug=true
