import configparser
import json
import logging

from BioSim import simulator

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Simulation(Resource):
    def post(self):
        reqString = request.form['sim']
        simReq = json.loads(reqString)
        trial_results = simulator.run_trials(config, log, int(simReq['num_trials']))

        return trial_results

api.add_resource(Simulation, '/')

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('sim_config.ini')
    config = config['DEFAULT']
    log = logging.getLogger(__name__)

    app.run(debug=True)