from flask import Flask, request, render_template
from app import utils
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    metadata = {}
    if request.method == 'POST':
        if 'image' not in request.files:
            metadata['Error'] = 'No file found'
        file = request.files['image']
        if file.filename != '':
            metadata = utils.get_exif_data(file.stream)
    return render_template('index.html', metadata=metadata)
