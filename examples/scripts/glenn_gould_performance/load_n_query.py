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
    query = """
    PREFIX mo: <http://purl.org/ontology/mo/>
    PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
    SELECT ?place
    WHERE {
    ?performance
      mo:performer <http://dbpedia.org/resource/Glenn_Gould> ;
      event:place ?place
    }"""
	
    # create an rdflib graph in memory
    graph = rdflib.ConjunctiveGraph()
    
    # parse the n3 file into the graph
    fname = 'glenn_gould_performance.n3'
    print "Importing local RDF file: %s" % fname
    graph.parse(fname, format='n3')
	
    # make the sparql query against the graph
    print "Loading:"
    for row in graph.query(query):
        print "\t"+row[0]
        # Loading more information about the place
        graph.parse(row[0])
  
    # Using the enriched graph to make a more interesting query
    # As well as getting the place in which Glenn Gould has played,
    # get a description of it, its latitude and its longitude 
    query = """
    PREFIX mo: <http://purl.org/ontology/mo/>
    PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    SELECT ?place ?comment ?lat ?long
    WHERE {
    ?performance
      mo:performer <http://dbpedia.org/resource/Glenn_Gould> ;
      event:place ?place .
    ?place
      rdfs:comment ?comment ;
      geo:lat ?lat ;
      geo:long ?long .
    }"""
 
    print "Glenn Gould has played in:"
    for row in graph.query(query):
        print "\t"+row[0]
        print row[1]
        print "It is at latitude " + row[2] + " and longitude " + row[3]

if __name__ == '__main__':
    main()

