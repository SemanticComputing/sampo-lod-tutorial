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

def handle_performance_role_row(graph, row):
    performanceRoleURI = URIRef('http://ldf.fi/operasampo/performance_roles_' + str(row['performanceRoleId']))
    graph.add((performanceRoleURI, RDF.type, SCOP.PerformanceRole))

    # composition role with compositionRoleId
    if not pd.isna(row['compositionRoleId']):
        compositionRoleURI = URIRef('http://ldf.fi/operasampo/roles_' + str(row['compositionRoleId']))
        graph.add((performanceRoleURI, SCOP.compositionRole, compositionRoleURI))
    
    # performance with performanceId
    if not pd.isna(row['performanceId']):
        performanceURI = URIRef('http://ldf.fi/operasampo/performances_' + str(row['performanceId']))
        graph.add((performanceRoleURI, SCOP.performance, performanceURI))
    
    # performer of the role with personId
    if not pd.isna(row['personId']):
        personURI = URIRef('http://ldf.fi/operasampo/persons_' + str(row['personId']))
        graph.add((performanceRoleURI, SCOP.performer, personURI))

def create_performance_role_instances():
    graph = Graph()
    bind_namespaces(graph)

    performance_roles_file = pd.read_csv('../csv/foc_PerformanceRole.csv', sep=";", dtype=object)
    
    print("Adding performance roles..")
    for i, row in performance_roles_file.iterrows():
        handle_performance_role_row(graph, row)
    
    print("Serializing performance_roles.ttl..")
    graph.serialize('../ttl/performance_roles.ttl', format='turtle')
