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

def handle_person_row(graph, row):
    personURI = URIRef('http://ldf.fi/operasampo/persons_' + str(row['personId']))
    graph.add((personURI, RDF.type, SCOP.Person))

    # firstName
    if not pd.isna(row['firstName']):
        graph.add((personURI, FOAF.firstName, Literal(row['firstName'])))
    
    # lastName
    if not pd.isna(row['lastName']):
        graph.add((personURI, FOAF.surname, Literal(row['lastName'])))
    
    # displayName
    if not pd.isna(row['displayName']):
        graph.add((personURI, SKOS.prefLabel, Literal(row['displayName'], lang='fi')))

    # dateOfBirth
    if not pd.isna(row['dateOfBirth']):
        graph.add((personURI, SCOP.dateOfBirth, Literal(row['dateOfBirth'])))
    
    # dateOfDeath
    if not pd.isna(row['dateOfDeath']):
        graph.add((personURI, SCOP.dateOfDeath, Literal(row['dateOfDeath'])))
    
    # placeOfBirth
    if not pd.isna(row['placeOfBirth']):
        graph.add((personURI, SCOP.placeOfBirth, Literal(row['placeOfBirth'])))
    
    # placeOfDeath
    if not pd.isna(row['placeOfDeath']):
        graph.add((personURI, SCOP.placeOfDeath, Literal(row['placeOfDeath'])))

    # additionalInfo
    if not pd.isna(row['additionalInfo']):
        # parse all variations of additional info (= different language variants)
        parsed_info = ut.parse(row['additionalInfo'])
        # for each language variant, add information to graph with the correct language code
        for info in parsed_info.root.AdditionalInfo:
            language_code = info['language-id'][:2]
            # for text content, replace newlines (\n) with <br> for rendering in UI
            graph.add((personURI, SCOP.additionalInfo, Literal(info.cdata.replace('\\n', '<br>'), lang=language_code)))

def create_person_instances():
    graph = Graph()
    bind_namespaces(graph)

    people_file = pd.read_csv('../csv/foc_Person.csv', sep=";", dtype=object)
    
    print("Adding people..")
    for i, row in people_file.iterrows():
        handle_person_row(graph, row)
    
    print("Serializing people.ttl..")
    graph.serialize('../ttl/people.ttl', format='turtle')
