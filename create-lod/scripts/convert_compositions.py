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

def handle_composition_row(graph, row):
    compositionURI = URIRef('http://ldf.fi/operasampo/compositions_' + str(row['compositionId']))
    graph.add((compositionURI, RDF.type, SCOP.Composition))

    # composer with composerId
    if not pd.isna(row['composerId']):
        composerURI = URIRef('http://ldf.fi/operasampo/persons_' + str(row['composerId']))
        graph.add((compositionURI, SCOP.composedBy, composerURI))
    
    # title with title
    if not pd.isna(row['title']):
        # parse all variations of title (= different language variants)
        parsed_title = ut.parse(row['title'])
        # for each language variant, add title to graph with the correct language code
        for title in parsed_title.root.Title:
            language_code = title['language-id'][:2]
            graph.add((compositionURI, SKOS.prefLabel, Literal(title.cdata, lang=language_code)))
    
    # additional title with additionalTitle
    if not pd.isna(row['additionalTitle']):
        # parse all variations of additional title (= different language variants)
        parsed_title = ut.parse(row['additionalTitle'])
        # for each language variant, add additional title to graph with the correct language code
        for title in parsed_title.root.AdditionalTitle:
            language_code = title['language-id'][:2]
            graph.add((compositionURI, SCOP.additionalTitle, Literal(title.cdata, lang=language_code)))
    
    # originalTitle
    if not pd.isna(row['originalTitle']):
        graph.add((compositionURI, SCOP.originalTitle, Literal(row['originalTitle'])))

def handle_composition_libretist_row(graph, row):
    compositionURI = URIRef('http://ldf.fi/operasampo/compositions_' + str(row['compositionId']))
    
    # personId
    if not pd.isna(row['personId']):
        personURI = URIRef('http://ldf.fi/operasampo/persons_' + str(row['personId']))
        graph.add((compositionURI, SCOP.libretist, personURI))

def create_composition_instances():
    graph = Graph()
    bind_namespaces(graph)

    composition_file = pd.read_csv('../csv/foc_Composition.csv', sep=";")
    
    print("Adding compositions..")
    for i, row in composition_file.iterrows():
        handle_composition_row(graph, row)
    
    composition_libretist_file = pd.read_csv('../csv/foc_CompositionLibretist.csv', sep=";")
    
    print("Adding libretists to compositions..")
    for i, row in composition_libretist_file.iterrows():
        handle_composition_libretist_row(graph, row)
    
    print("Serializing compositions.ttl..")
    graph.serialize('../ttl/compositions.ttl', format='turtle')
