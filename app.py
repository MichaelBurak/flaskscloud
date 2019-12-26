from flask import Flask, render_template, send_file, make_response, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,BooleanField
from wtforms.validators import DataRequired
import stylecloud
from PIL import Image
import io
import matplotlib
import palettable
matplotlib.use('TkAgg')

import os 

app = Flask(__name__,static_url_path='/static')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['SECRET_KEY'] = 'mysecretkey'


OUTPUT_NAME = "./static/out.png"


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class MyForm(FlaskForm):
    txt =  TextAreaField('Text here')
    color = StringField("Select a solid color for text if you want")
    bgcolor = StringField('Select a background color')
    moonrise = BooleanField('Moonrise Kingdom Mode Colors?')
    submit = SubmitField('Submit')


def sc(tx, bg, clr, mk):

    if bg == "":
        bg = "white"
    
    if clr == "":
        clr = None
    
    if mk == False:
        mk = 'cartocolors.qualitative.Bold_5'
    
    if mk == True:
        mk = 'Moonrise1_5'

    stylecloud.gen_stylecloud(text=tx,
                              background_color=bg, output_name=OUTPUT_NAME, colors=clr, palette=mk)
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
        img = sc(form.txt.data,form.bgcolor.data, form.color.data, form.moonrise.data)
        resp = make_response(render_template('img.html')) #here you could use make_response(render_template(...)) too
        resp.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        resp.headers['Cache-Control'] = 'public, max-age=0'
        return resp
    return render_template('index.html', img=img, form=form, place=place)


@app.route('/img')
def img():
    return render_template('img.html', img=img)


if __name__ == '__main__':
    app.run(debug=True, port=9000)
    #debug=true
