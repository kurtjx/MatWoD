#!/usr/bin/ruby

require 'rubygems'
require 'rqommend'

# Artists that are based in Detroit are related
Rqommend::Can.new "
    SELECT *
    WHERE {
      @INPUT <http://dbpedia.org/ontology/homeTown> <http://dbpedia.org/resource/Detroit> .
      @INPUT <http://dbpedia.org/property/name> ?input_name .
      ?OUTPUT <http://dbpedia.org/ontology/homeTown> <http://dbpedia.org/resource/Detroit> .
      ?OUTPUT <http://dbpedia.org/property/name> ?output_name .
      FILTER (@INPUT != ?OUTPUT)
    }", 
    '<%= result["input_name"] %> and <%= result["output_name"] %> are both based in Detroit'

# Artists in the Manchester scene in the 70s are related
Rqommend::Can.new "
      SELECT * WHERE {
        @INPUT 
          a <http://dbpedia.org/class/yago/MusicalGroupsFromManchester> ;
          a <http://dbpedia.org/class/yago/1970sMusicGroups> ;
          <http://dbpedia.org/property/name> ?input_name .
        ?OUTPUT
          a <http://dbpedia.org/class/yago/MusicalGroupsFromManchester> ;
          a <http://dbpedia.org/class/yago/1970sMusicGroups> ;
          <http://dbpedia.org/property/name> ?output_name .
        FILTER (@INPUT != ?OUTPUT)
      }
    ",
    "<%= result['input_name'] %> and <%= result['output_name'] %> were both part of the 70s Manchester scene"

# Artists on independent record labels are related
Rqommend::Can.new "
      SELECT * WHERE {
        @INPUT
          <http://dbpedia.org/ontology/label> ?label ;
          <http://dbpedia.org/property/name> ?input_name .
        ?OUTPUT
           <http://dbpedia.org/ontology/label> ?label ;
          <http://dbpedia.org/property/name> ?output_name .
        ?label
          <http://xmlns.com/foaf/0.1/name> ?label_name ;
          a <http://dbpedia.org/class/yago/IndependentRecordLabels> ;
          <http://dbpedia.org/property/abstract> ?abstract .
        FILTER (
          (@INPUT != ?OUTPUT) &&
          (langMatches(lang(?abstract), 'en') || lang(?abstract) = '' )
        )
      }
    ",
    "<%= result['input_name'] %> and <%= result['output_name'] %> were both signed on <%= result['label_name'] %>. <%= result['abstract'] %>"

# Trying these rules out
require 'pp'
resource = Rqommend::Resource.new 'http://dbpedia.org/resource/Aretha_Franklin'
recommendations = resource.recommendations
puts '-------------------------------------------'
puts 'A random recommendation for Aretha Franklin'
pp recommendations[rand(recommendations.size)]
resource = Rqommend::Resource.new 'http://dbpedia.org/resource/Joy_Division'
recommendations = resource.recommendations
puts '-------------------------------------------'
puts 'A random recommendation for Joy Division'
pp recommendations[rand(recommendations.size)]
resource = Rqommend::Resource.new 'http://dbpedia.org/resource/Minor_Threat'
recommendations = resource.recommendations
puts '-------------------------------------------'
puts 'A random recommendation for Minor Threat'
pp recommendations[rand(recommendations.size)]
