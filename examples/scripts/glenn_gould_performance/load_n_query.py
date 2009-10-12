#!/usr/bin/env python
# encoding: utf-8
"""
load_n_query.py

Created by kurtjx on 2009-10-12.

"""

import sys
try:
	import rdflib
except:
	print '''Error importing rdflib - perhaps it is not installed'''
	print ''' $ sudo easy_install -U "rdflib>=2.4"'''
	sys.exit(1)

def main():
	query = '''
	PREFIX mo: <http://purl.org/ontology/mo/>
	PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
	SELECT ?place
	FROM <glenn_gould_performance.n3>
	WHERE {
	?performance
	  mo:performer <http://dbpedia.org/resource/Glenn_Gould> ;
	  event:place ?place
	}'''
	
	graph = rdflib.ConjunctiveGraph()
	fname = 'glenn_gould_performance.n3'
	print "parsing local RDF file: %s" % fname
	graph.parse(fname, format='n3')
	print "making query:"
	print query
	print "Glenn Gould has played in:"
	for row in graph.query(query):
		print "\t"+row[0]
	


if __name__ == '__main__':
	main()

