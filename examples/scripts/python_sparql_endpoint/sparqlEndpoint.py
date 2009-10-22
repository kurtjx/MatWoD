'''This is a very basic script that sets up a sparql
endpoind on localhost which you can query 
(e.g. using SPARQLWrapper)

Requirements: 
rdflib (RDF library)
cherrypy (Web server)

'''

from __future__ import with_statement
import os
import rdflib
import cherrypy

# a simple example we will load into the store
example='''
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix mo: <http://purl.org/ontology/mo/> .
@prefix : <#> .

<file://sparqlEndpoint.py> dc:title "Hello SPARQL" .

:track a mo:Track ;
	dc:title "my favourite song" ;
	mo:available_as :file .

:file a mo:AudioFile ;
    mo:encodes :signal .

:signal a mo:Signal .

'''

# ============================================
# 	RDF Store using RDFlib 
# ============================================

class TripleStore(object):
	'''Very high-level wrapper around an rdflib triple store.'''
	
	def __init__(self):
		'''Create a store. We ought to do more configuration here.
		This will just keep everything in memory.'''
		self.g = rdflib.ConjunctiveGraph()
		
	def loadStringSource(self,string,format='n3'):
		source = rdflib.StringInputSource(string)
		self.g.parse(source,format=format)
		
	def loadFileSource(self,file,graph_context=None,format='n3'):
		fileURI = rdflib.URIRef('file://'+os.path.basename(file))
		with open(file) as fh :
			fs = rdflib.FileInputSource(fh)
			self.g.parse(fs, publicID=fileURI, format=format)
			
	def answerQuery(self,query,result_format='JSON'):
		results = self.g.query(query)
		return results.serialize(format=result_format)
						

# ============================================
# 	SPARQL request handler application 
# ============================================

class SparqlEndpoint(object):
	
	def __init__(self):
		self.rdf_store = TripleStore()
		
	@cherrypy.expose
	def sparql(self,query,output=None,results=None):
		if results == 'json' or output == 'json' :
			cherrypy.response.headers['Content-Type'] = "application/sparql-results+json"
		else :
			results = 'xml'
			cherrypy.response.headers['Content-Type'] = "application/sparql-results+xml"
		return self.rdf_store.answerQuery(query,result_format = results)

# ============================================
# 	Web Server using Cherypy 
# ============================================

class WebServer(object):
		
	def __init__(self):
		pass
		
	def mount(self,requestHandler):
		app_config = {'/' : {
		'server.socket_timeout': 30,
		'tools.sessions.on': False
		}}
		cherrypy.tree.mount(requestHandler,config=app_config)
		
	def quickstart(self,ip="127.0.0.1",port=8081):
		cp_config = {
		'global': {
		'server.socket_host': ip,
		'server.socket_port': port,
		'engine.autoreload_on' : True,
		'engine.autoreload_frequency' : 5
		}}
		cherrypy.quickstart(script_name='', config=cp_config)

		
def main(args):
	
	server = WebServer()

	endpoint = SparqlEndpoint()
	endpoint.rdf_store.loadStringSource(example)
	try :
		endpoint.rdf_store.loadFileSource("trout_quintet.n3")
	except IOError:
		print "File not found."

	server.mount(endpoint)
	server.quickstart()

if __name__ == '__main__':
	import sys
	main(sys.argv[1:])
