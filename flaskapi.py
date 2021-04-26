
import flask
from flask import request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import pychromecast

## Perso Libraries 
from src.hc_config import home_cinema

app = flask.Flask(__name__)
undertaker= flask.Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

CURRENT_VERSION = "v_0.0.0_beta"
RELEASE_DATE = "01 MAY. 2021"
HC = home_cinema()
##############################################################################################################################################################################
## Functions #################################################################################################################################################################
##############################################################################################################################################################################

@app.route('/', methods=['GET'])
def home():
    return "<h1>Cinecast</h1>"

@app.route('/api/devices', methods=['GET'])
def devices():
    devices = HC.getDevices()
    return json.dumps({'devices':devices})

@app.route('/api/config', methods=['POST'])
def config():
    video =  request.json['v_device']
    audio =  request.json['a_device']
    HC.config(v_name=video, a_name=audio)
    return json.dumps({'video':video, 'audio': audio})

@app.route('/api/playurl', methods=['POST'])
def playUrl():
    video =  request.json['v_device']
    audio =  request.json['a_device']
    url =  request.json['url']
    HC.playUrl(url)
    return json.dumps({'video':video, 'audio': audio, 'url':url})

@app.route('/api/status', methods=['GET'])
def v_status():
    status = HC.getVStatus()
    print(status)
    return json.dumps({'title':status.title,'current_time':status.current_time, 'duration':status.duration, 'player_state':status.player_state})

@app.route('/api/pause', methods=['GET'])
def pause():
    HC.pause()
    return json.dumps({})

@app.route('/api/play', methods=['GET'])
def play():
    HC.play()
    return json.dumps({})