# Imoort packages
from flask import Flask, request, render_template

# Import utils which contains metadata extractor method
from app import utils

# Define flask main configuration app container
app = Flask(__name__)

# Define default root route with POST method as default is only GET
@app.route('/', methods=['GET', 'POST'])
def index():
    metadata = {}
    if request.method == 'POST':
        if 'image' not in request.files:
            metadata['Error'] = 'No file found'
        file = request.files['image']
        if file.filename != '':
            metadata = utils.get_exif_data(file.stream)
    
    # Use template
    return render_template('index.html', metadata=metadata)
