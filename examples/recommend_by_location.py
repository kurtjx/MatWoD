#!/usr/bin/env python
'''
Location-based Jamendo Recs - Tutorial Music and the Web of Data

    Recommend Jamendo artists based on the location of origin of artists found in a last.fm
    user's profile.  The http://dbtune.org/last-fm/ service is used to grab scrobbles and links
    to DBpedia.  Then DBpedia is used to get the location of origin for these artists.  Latitude
    and longitude values are obtained by dereferencing Geonames URIs.  These coordinates are
    used to find artists based near the same location in http://dbtune.org/jamendo/

    @requires: SPARQLWrapper, rdflib

'''

import sys
from rdflib import ConjunctiveGraph
from SPARQLWrapper import SPARQLWrapper2, SPARQLWrapper, XML
from xml.dom import minidom


def parse_lastfm(username):
    ''' return an array of zitgist uris for scrobbled artists '''
    graph = ConjunctiveGraph()
    print 'parsing last.fm data from dbtune for %s' % username
    graph.parse('http://dbtune.org/last-fm/'+username)
    query = '''
            PREFIX mo: <http://purl.org/ontology/mo/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>

            SELECT DISTINCT ?same WHERE {
                ?artist a mo:MusicArtist ;
                    owl:sameAs ?same .
                }
            '''
    same = []
    for row in graph.query(query):
        same.append(row[0])
    return same

def get_locations_from_dbpedia(uri):
    '''starting from a zitgist uri, get a geonames location, this will use SPARQLWrapper'''
    sparql = SPARQLWrapper2('http://dbpedia.org/sparql')
    query = '''
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dbprop: <http://dbpedia.org/property/>

        SELECT ?geo WHERE {
            ?artist owl:sameAs <%s> ;
                 dbprop:origin ?place .
            ?place owl:sameAs ?geo .
            FILTER ( REGEX (?geo, "geonames") )
            }
        ''' % uri
    sparql.setQuery(query)
    print 'querying dbpedia for geoname of %s' % uri
    response = sparql.query()
    geoname = None
    for binding in response.bindings:
        geoname = binding['geo'].value

    return geoname

def find_long_lat(uri):
    '''return tuple of the longitude and latitude (long,lat) for a geonames uri and the name'''
    graph = ConjunctiveGraph()
    graph.parse(uri)
    query = '''
            PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX geo: <http://www.geonames.org/ontology#>
            SELECT ?long ?lat ?name WHERE
            { ?x wgs:long ?long;
                 wgs:lat ?lat;
                 geo:name ?name.
            }
            '''
    long_lat_name = None
    print 'finding coordinates for %s ' % uri
    for row in graph.query(query):
        long_lat_name = (row[0], row[1], row[2])
    return long_lat_name


def query_jamendo(longlat, distance='3', limit ='3'):
    '''
    query jamendo endpoint to find artists near the recently scrobbled artists
        @warning: the Jamendo endpoint does not return JSON so we cannot use the SPARQLWrapper2
    '''
    long = longlat[0]
    lat = longlat[1]

    # Jamendo endpoint does not support JSON so we cannot us the more convenient SPARQLWrapper2
    sparql = SPARQLWrapper('http://dbtune.org/jamendo/sparql/')
    sparql.setReturnFormat(XML)

    # the FILTER() clause is a bit confusing here - note the "%(var)s" syntax is part of Python
    # for adding the dictionary of local variables in place in the string
    query = '''
            PREFIX mo: <http://purl.org/ontology/mo/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX geo: <http://www.geonames.org/ontology#>
            PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>

            SELECT DISTINCT ?name ?artist ?pname ?place ?lat ?long where { ?artist
                 a mo:MusicArtist;
                 foaf:based_near ?place ;
                 foaf:name ?name .
            ?place
                 wgs:lat ?lat;
                 wgs:long ?long;
                 geo:name ?pname .
            FILTER (
            ( ((%(lat)s - xsd:float(?lat) ) < %(distance)s && (%(lat)s - xsd:float(?lat)) > 0 ) ||
            ( (xsd:float(?lat)-%(lat)s) < %(distance)s && (xsd:float(?lat)-%(lat)s) > 0)) &&
            ( (( %(long)s - xsd:float(?long)) < %(distance)s && ( %(long)s - xsd:float(?long)) > 0)) ||
            ( ((xsd:float(?long)- %(long)s ) < %(distance)s && (xsd:float(?long)- %(long)s ) > 0))
            )
            } LIMIT %(limit)s ''' % locals()

    sparql.setQuery(query)
    #print 'querying for artists nearby %s ' % longlat[2]
    response = sparql.query()

    # super annoying, need to parse XML by hand
    xml = response.response.read()
    dom = minidom.parseString(xml)
    result_dict = {}
    ret=[]
    for result in dom.getElementsByTagName('result'):
        name = result.getElementsByTagName('binding')[0].childNodes[1].firstChild.nodeValue
        auri = result.getElementsByTagName('binding')[1].childNodes[1].firstChild.nodeValue
        pname = result.getElementsByTagName('binding')[2].childNodes[1].firstChild.nodeValue
        puri = result.getElementsByTagName('binding')[3].childNodes[1].firstChild.nodeValue
        plat = result.getElementsByTagName('binding')[4].childNodes[1].firstChild.nodeValue
        plong = result.getElementsByTagName('binding')[5].childNodes[1].firstChild.nodeValue
        ret.append((name,auri,pname, plat, plong, puri))
    return ret





def main(argv=['kurtjx']):
    username = argv[0]
    # first parse last.fm for a user finding sameAs
    artists = parse_lastfm(username)

    # then use the Zitgist URIs to find locations in DBpedia
    geonames = []
    for artist in artists:
        geoname = get_locations_from_dbpedia(artist)
        if geoname != None:
            geonames.append(geoname)

    # find longitude and latitude by dereferencing Geonames URIs
    longlats = []
    for uri in geonames:
        longlats.append(find_long_lat(uri))

    print 'found %d geoname coordinates' % len(longlats)
    # query DBtune/Jamendo for 'nearby' artists
    for idx, longlat in enumerate(longlats):
        print '===============results near %s %s %s -- %s==================' % (longlats[idx][2], longlats[idx][1], longlats[idx][0], geonames[idx])
        results = query_jamendo(longlat)
        if len(results)==0:
            print 'no artists found'
        for result in results:
            print '''name:  %s - %s ---\n   place: %s %s %s --- %s''' % result

if __name__ == '__main__':
    main(sys.argv[1:])


