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
	
	# create an rdflib graph in memory
	graph = rdflib.ConjunctiveGraph()
	
	# parse the n3 file into the graph
	fname = 'glenn_gould_performance.n3'
	print "parsing local RDF file: %s" % fname
	graph.parse(fname, format='n3')
	
	# make the sparql query against the graph
	print "making query:"
	print query
	print "Glenn Gould has played in:"
	for row in graph.query(query):
		print "\t"+row[0]
	
	########################################
	# uncomment to parse data from dbpedia #
	########################################
	# graph.parse('http://dbpedia.org/resource/Glenn_Gould')
	# graph.parse('http://dbpedia.org/resource/Ebell_of_Los_Angeles')
	# 
	# query = """PREFIX mo: <http://purl.org/ontology/mo/>
	# PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
	# PREFIX dbp: <http://dbpedia.org/property/>
	# 
	# SELECT ?place ?architect
	# WHERE { ?performance
	# 	       mo:performer <http://dbpedia.org/resource/Glenn_Gould> ;
	# 	          event:place ?place .
	# 	    ?place dbp:architect ?architect .  }
	# 	""""
	# 	
	# query = """SELECT DISTINCT ?glenn WHERE { <http://dbpedia.org/resource/Glenn_Gould> <http://www.w3.org/2002/07/owl#sameAs> ?glenn . } """
	# sameAs = []
	# for row in graph.query(query):
	# 	sameAs.append(row[0])
	# 
	# for resource in sameAs:
	# 	graph.parse(resource)


if __name__ == '__main__':
	main()

