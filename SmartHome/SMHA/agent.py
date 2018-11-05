from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 1337), requestHandler=RequestHandler) as server:
	server.register_introspection_functions() #remove this

	def getStatus(id):
		return "ok"

	def setPowerState(id, state):
		return "ok"

	def discoverDevices():
		return "Devices"

	server.register_function(getStatus, 'status')
	server.register_function(setPowerState, 'power')
	server.register_function(discoverDevices, 'discover')

	server.serve_forever()

