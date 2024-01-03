import flask_cors
from flask import Flask, request, render_template, jsonify
import os
import configparser
import psutil

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__, template_folder=os.path.join(os.path.abspath('./run/web'), 'templates'))
flask_cors.CORS(app)

@app.route('/', methods=['GET'])
def index():    
    return render_template('index.html')

@app.route('/scripts/<script>', methods=['GET'])
def script(script):

    file = os.path.join(os.path.abspath('./run/web'), 'scripts', script)
    
    if os.path.exists(file):
        return open(file).read()
    else:
        return '404'
        
    
@app.route('/api/ram', methods=['GET'])
def ram():
    return jsonify({'ram': psutil.virtual_memory().percent})

@app.route('/api/cpu', methods=['GET'])
def cpu():
    return jsonify({'cpu': psutil.cpu_percent(interval=5)})

@app.route('/api/uptime', methods=['GET'])
def uptime():
    return jsonify({'uptime': psutil.boot_time()})




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=config.getint('SERVER', 'PORT'), debug=True)
