# Imoort packages
from flask import Flask, request, render_template, jsonify
import socket
import psutil
import subprocess

# Import utils which contains metadata extractor method
from app import utils

# Define flask application instance
app = Flask(__name__)

# Define default root route with POST method as default is only GET
@app.route('/', methods=['GET', 'POST'])
def index():
    metadata = {}
    filename = None
     
    # This gets the pod ID
    hostname = socket.gethostname()
    
    if request.method == 'POST':
        if 'image' not in request.files:
            metadata['Error'] = 'No file found'
        
        file = request.files.get("image")
        if file and file.filename != "":
            filename = file.filename
            metadata = utils.get_exif_data(file.stream)

    # Use Template
    return render_template("index.html", metadata=metadata, filename=filename, hostname=hostname)

@app.route('/cpu')
def cpu_usage():
     usage = psutil.cpu_percent(interval=0.1)
     return jsonify({"cpu": usage})

stress_process = None  # Global handle to keep track of the process

@app.route('/start-cpu-burn', methods=['POST'])
def start_cpu_burn():
    global stress_process
    if stress_process and stress_process.poll() is None:
        return jsonify({'status': 'Already running'})

    try:
        # Start stress in background
        stress_process = subprocess.Popen(['stress', '--cpu', '1', '--timeout', '10'])
        return jsonify({'status': 'CPU burn started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop-cpu-burn', methods=['POST'])
def stop_cpu_burn():
    global stress_process
    if stress_process and stress_process.poll() is None:
        try:
            stress_process.terminate()  # Send SIGTERM
            stress_process.wait(timeout=5)
            return jsonify({'status': 'CPU burn stopped'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'status': 'No CPU burn process running'})

# Run app when Docker runs Python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)