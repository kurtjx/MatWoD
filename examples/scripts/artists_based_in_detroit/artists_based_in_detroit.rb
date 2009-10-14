require 'rubygems'
require '4store-ruby'
require 'pp'

store = FourStore::Store.new 'http://dbpedia.org/sparql/'

results = store.select("
    SELECT *
    WHERE {
      ?artist <http://dbpedia.org/ontology/homeTown> <http://dbpedia.org/resource/Detroit> .
      ?artist <http://dbpedia.org/property/name> ?artist_name .
    }
");

pp results
