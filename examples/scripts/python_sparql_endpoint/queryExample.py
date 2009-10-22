from SPARQLWrapper import SPARQLWrapper, JSON
from urllib2 import HTTPError,URLError

prefixes = [
'PREFIX dc: <http://purl.org/dc/elements/1.1/>',\
'PREFIX mo: <http://purl.org/ontology/mo/>']

# this query should answer: Hello SPARQL
basicQuery = '\n'.join(prefixes) + ("""\n
SELECT ?title
WHERE { 
<file://sparqlEndpoint.py> dc:title ?title .
}
""")

# this query prints all 'titles' present in the store
titlesQuery = '\n'.join(prefixes) + ("""\n
SELECT DISTINCT ?title
WHERE { ?s dc:title ?title . }
""")

# this is our end-point listening on localhost
endpointURI = "http://127.0.0.1:8081/sparql"
wrapper = SPARQLWrapper(endpointURI)

#wrapper.setQuery(basicQuery)
wrapper.setQuery(titlesQuery)

#execute the query catching common errors
results = None
wrapper.setReturnFormat(JSON)
try :
	results = wrapper.query().convert()
except (HTTPError,URLError), msg:
	print "Error: "+str(msg)

# parse the query results
if results and type(results) == dict:
	bindings = results['results']['bindings']
	for res in bindings : print res['title']['value']
