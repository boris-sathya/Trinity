import markdown
import os
import shelve


from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)

# Fetch Database Context and Apply DataStore Wrapper
def getDeviceDataBaseContext():
	db = getattr(g, '_device_database', None)
	if db is None:
		db = g._device_database = shelve.open("data/devices.db")
	return db

def getPowerDataBaseContext():
	db = getattr(g, '_power_database', None)
	if db is None:
		db = g._power_database = shelve.open("data/utilization.db")
	return db

def getDeviceRepo():
    repo = getattr(g, '_device_repository', None)
    if repo is None:
        repo = g._device_repository = DataStore(getDeviceDataBaseContext())
    return repo

def getPowerRepo():
	repo = getattr(g, '_device_repository', None)
	if repo is None:
		repo = g._device_repository = DataStore(getPowerDataBaseContext())
	return repo

@app.teardown_appcontext
def teardownDataBaseContext(exception):
	ddb = getattr(g, '_device_database', None)
	pdb = getattr(g, '_power_database', None)
	if ddb is not None:
		ddb.close()
	if pdb is not None:
		pdb.close()

@app.route("/")
def index():
	with open(os.path.dirname(app.root_path) + '/README.md', 'r') as doc:
		content = doc.read()
		return markdown.markdown(content)

# Smart Home Controller APIs

# API 1: View Devices
# API 2: Add a new device 
class DeviceList(Resource):
	def get(self):
		repo = getDeviceRepo()
		devices = repo.find_all()

		return {'data': devices}, 200

	def post(self):
		parser = reqparse.RequestParser()

		parser.add_argument('id', required=True)
		parser.add_argument('device', required=True)
		parser.add_argument('power', required=True)
		parser.add_argument('name', required=True)
		parser.add_argument('type', required=True)
		parser.add_argument('controller', required=True)
		parser.add_argument('location', required=True)

		args = parser.parse_args()

		repo = getDeviceRepo()
		repo.save(args)

		return 200

# API 3: View device specific data
# API 4: Delete a specific device
class Device(Resource):
    def get(self, identifier: str):
        device = getDeviceRepo().find(identifier)

        if device is None:
            return 404

        return {'data': device}, 200

    def delete(self, identifier: str):
        device_repo = getDeviceRepo()

        device = device_repo.find(identifier)

        if device is None:
            return 404

        device_repo.delete(identifier)

        return '', 200


# Database Wrapper
class DataStore:
    def __init__(self, dbContext):
        self.dbContext = dbContext

    def find_all(self):
        keys = list(self.dbContext.keys())
        objects = []

        for key in keys:
        	objects.append(self.dbContext[key])

        return objects

    def find(self, identifier: str):

        if not (identifier in self.dbContext):
            return None

        return self.dbContext[identifier]

    def find_by(self, key: str, value: str):
        objects = []

        for obj in self.find_all():
            if obj[key] == value:
                objects.append(obj)

        return objects

    def save(self, obj):
        self.dbContext[obj['id']] = obj

    def delete(self, identifier: str):
        del self.dbContext[identifier]

# HTTP API Routes
api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')

