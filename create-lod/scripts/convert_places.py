import pandas as pd
import untangle as ut
from rdflib import Namespace, URIRef, Literal, Graph, RDF, RDFS, XSD, FOAF

SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
OPS = Namespace('http://ldf.fi/operasampo/')
SCOP = Namespace('http://ldf.fi/schema/operasampo/')

def bind_namespaces(graph):
    graph.bind('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    graph.bind('skos', 'http://www.w3.org/2004/02/skos/core#')
    graph.bind('ops', 'http://ldf.fi/operasampo/')
    graph.bind('scop', 'http://ldf.fi/schema/operasampo/')
    graph.bind('foaf',  'http://xmlns.com/foaf/0.1/')

def handle_place_row(graph, row):
    placeURI = URIRef('http://ldf.fi/operasampo/places_' + str(row['placeId']))
    graph.add((placeURI, RDF.type, SCOP.Place))

    # name
    if not pd.isna(row['name']):
        # parse all variations of name (= different language variants)
        parsed_name = ut.parse(row['name'])
        # for each language variant, add name to graph with the correct language code
        for name in parsed_name.root.Name:
            language_code = name['language-id'][:2]
            graph.add((placeURI, SKOS.prefLabel, Literal(name.cdata, lang=language_code)))

    # city
    if not pd.isna(row['city']):
        parsed_city = ut.parse(row['city'])
        for city in parsed_city.root.City:
            language_code = city['language-id'][:2]
            graph.add((placeURI, SCOP.city, Literal(city.cdata, lang=language_code)))

    # country
    if not pd.isna(row['country']):
        parsed_country = ut.parse(row['country'])
        for country in parsed_country.root.Country:
            language_code = country['language-id'][:2]
            graph.add((placeURI, SCOP.country, Literal(country.cdata, lang=language_code)))

    # additionalInfo
    if not pd.isna(row['additionalInfo']):
        # parse all variations of additional info (= different language variants)
        parsed_info = ut.parse(row['additionalInfo'])
        # for each language variant, add information to graph with the correct language code
        for info in parsed_info.root.AdditionalInfo:
            language_code = info['language-id'][:2]
            # for text content, replace newlines (\n) with <br> for rendering in UI
            graph.add((placeURI, SCOP.additionalInfo, Literal(info.cdata.replace('\\n', '<br>'), lang=language_code)))

def create_place_instances():
    graph = Graph()
    bind_namespaces(graph)

    places_file = pd.read_csv('../csv/foc_Place.csv', sep=";", dtype=object)
    
    print("Adding places..")
    for i, row in places_file.iterrows():
        handle_place_row(graph, row)
    
    print("Serializing places.ttl..")
    graph.serialize('../ttl/places.ttl', format='turtle')
