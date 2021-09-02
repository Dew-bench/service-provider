from flask import Flask, request
import socket
import json
import requests
from pyK8sManager.DeploymentManager import DeploymentManager

app = Flask(__name__)

DeplManager = DeploymentManager()

SERVICES = {}
# BROKERS = {}


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

# @app.route('/api/broker/add', methods=['POST', 'PUT'])
# def add_device():
#     data = request.get_json() 
#     BROKERS[data['id']] = data 
#     return "ok"

# @app.route('/api/broker/remove', methods=['POST', 'PUT'])
# def remove_device():
#     data = request.get_json() 
#     BROKERS.pop(data['id'])
#     return "ok"

# @app.route('/api/broker/list', methods=['GET'])
# def list_device():
#     return json.dumps(BROKERS)

######################################

@app.route('/api/service/add', methods=['POST', 'PUT'])
def add_service():
    data = request.get_json() 

    for settings in data['settings']:
        if settings['dtype'] == "pod":
            if settings['settings']['command'] == "":
                settings['settings']['command'] = None

    SERVICES[data['id']] = {
        'settings': data['settings'],
        'id': data['id'],
        'settings_id': DeplManager.get_new_id(),
        'url': ''
    } 
    print( data['settings'])
    DeplManager.save_settings(SERVICES[data['id']]['settings'], SERVICES[data['id']]['settings_id'])
    DeplManager.instantiate_settings(SERVICES[data['id']]['settings_id'], SERVICES[data['id']]['settings_id'])

    return "ok"

@app.route('/api/service/url', methods=['POST','PUT'])
def service_url():
    data = request.get_json() 
    return DeplManager.get_instance_url(SERVICES[data['id']]['settings_id'])

@app.route('/api/service/remove', methods=['POST', 'PUT'])
def remove_service():
    data = request.get_json() 
    # SERVICES[data['id']]['settings_id']
    DeplManager.delete_settings_instance(SERVICES[data['id']]['settings_id'])
    SERVICES.pop(data['id'])
    return "ok"

# @app.route('/api/service/list', methods=['GET'])
# def list_device():
#     return json.dumps(SERVICES)

######################################


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5011)