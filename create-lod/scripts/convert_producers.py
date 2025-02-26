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

def handle_producer_row(graph, row):
    producerURI = URIRef('http://ldf.fi/operasampo/producers_' + str(row['producerId']))
    graph.add((producerURI, RDF.type, SCOP.Producer))

    # name
    if not pd.isna(row['name']):
        # parse all variations of name (= different language variants)
        parsed_name = ut.parse(row['name'])
        # for each language variant, add name to graph with the correct language code
        for name in parsed_name.root.Name:
            language_code = name['language-id'][:2]
            graph.add((producerURI, SKOS.prefLabel, Literal(name.cdata, lang=language_code)))

    # additionalInfo
    if not pd.isna(row['additionalInfo']):
        # parse all variations of additional info (= different language variants)
        parsed_info = ut.parse(row['additionalInfo'])
        # for each language variant, add information to graph with the correct language code
        for info in parsed_info.root.AdditionalInfo:
            language_code = info['language-id'][:2]
            # for text content, replace newlines (\n) with <br> for rendering in UI
            graph.add((producerURI, SCOP.additionalInfo, Literal(info.cdata.replace('\\n', '<br>'), lang=language_code)))

def create_producer_instances():
    graph = Graph()
    bind_namespaces(graph)

    producers_file = pd.read_csv('../csv/foc_Producer.csv', sep=";", dtype=object)
    
    print("Adding producers..")
    for i, row in producers_file.iterrows():
        handle_producer_row(graph, row)
    
    print("Serializing producers.ttl..")
    graph.serialize('../ttl/producers.ttl', format='turtle')
