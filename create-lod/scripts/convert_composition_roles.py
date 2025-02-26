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

def handle_composition_role_row(graph, row):
    roleURI = URIRef('http://ldf.fi/operasampo/roles_' + str(row['compositionRoleId']))
    graph.add((roleURI, RDF.type, SCOP.Role))

    # composition
    if not pd.isna(row['compositionId']):
        compositionURI = URIRef('http://ldf.fi/operasampo/compositions_' + str(row['compositionId']))
        graph.add((roleURI, SCOP.composition, compositionURI))

    # name
    if not pd.isna(row['name']):
        # parse all variations of name (= different language variants)
        parsed_name = ut.parse(row['name'])
        # for each language variant, add name to graph with the correct language code
        for name in parsed_name.root.Name:
            language_code = name['language-id'][:2]
            graph.add((roleURI, SKOS.prefLabel, Literal(name.cdata, lang=language_code)))

def create_composition_role_instances():
    graph = Graph()
    bind_namespaces(graph)

    composition_roles_file = pd.read_csv('../csv/foc_CompositionRole.csv', sep=";", dtype=object)
    
    print("Adding composition roles..")
    for i, row in composition_roles_file.iterrows():
        handle_composition_role_row(graph, row)
    
    print("Serializing composition_roles.ttl..")
    graph.serialize('../ttl/composition_roles.ttl', format='turtle')
