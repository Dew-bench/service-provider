from flask import Flask, request
import socket
import json
import requests

app = Flask(__name__)

SERVICES = {}
BROKERS = {}


######################################

@app.route('/')
def hello_world():
    return 'Service provider'

@app.route('/api/ip')
def get_ip():
    h_name = socket.gethostname()
    IP_addres = socket.gethostbyname(h_name)
    return json.dumps({
        "host_name": h_name,
        "ip": IP_addres
    })

######################################

@app.route('/api/broker/add', methods=['POST', 'PUT'])
def add_device():
    data = request.get_json() 
    BROKERS[data['id']] = data 
    return "ok"

@app.route('/api/broker/remove', methods=['POST', 'PUT'])
def remove_device():
    data = request.get_json() 
    BROKERS.pop(data['id'])
    return "ok"

@app.route('/api/broker/list', methods=['GET'])
def list_device():
    return json.dumps(BROKERS)

######################################

@app.route('/api/service/add', methods=['POST', 'PUT'])
def add_device():
    data = request.get_json() 
    SERVICES[data['id']] = data 
    return "ok"

@app.route('/api/service/remove', methods=['POST', 'PUT'])
def remove_device():
    data = request.get_json() 
    SERVICES.pop(data['id'])
    return "ok"

@app.route('/api/service/list', methods=['GET'])
def list_device():
    return json.dumps(SERVICES)

######################################


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5011)