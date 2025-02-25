import pandas as pd
import untangle as ut
from bs4 import BeautifulSoup
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

def extract_name(row):
    name = 'Unnamed performance'
    date = 'unknown date'

    if not pd.isna(row['additionalInfo']):
        # parse all variations of additional info (= different language variants)
        parsed_info = ut.parse(row['additionalInfo'])
        # for each language variant, add information to graph with the correct language code
        for info in parsed_info.root.AdditionalInfo:
            soup = BeautifulSoup(info.cdata, 'html.parser')
            first_b = soup.b
            if first_b is not None:
                name = first_b.get_text()
                # common name format: <b>Name.</b> or <b>Name (Original composition name).</b>
                # take only the part before the composition name and strip trailing spaces
                name = name.split('(')[0].strip(' ,.')
                break
    
    if not pd.isna(row['performanceDate']):
        date = row['performanceDate'].split()[0] # take only date part from timestamp
    
    return name + ' (' + date + ')'

def handle_performance_row(graph, row):
    performanceURI = URIRef('http://ldf.fi/operasampo/performances_' + str(row['performanceId']))
    graph.add((performanceURI, RDF.type, SCOP.Performance))

    # composition with compositionId
    if row['compositionId'] != 0:
        compositionURI = URIRef('http://ldf.fi/operasampo/compositions_' + str(row['compositionId']))
        graph.add((performanceURI, SCOP.composition, compositionURI))

    # conductor with conductorId
    if row['conductorId'] != 0:
        conductorURI = URIRef('http://ldf.fi/operasampo/persons_' + str(row['conductorId']))
        graph.add((performanceURI, SCOP.conductedBy, conductorURI))

    # director with directorId
    if row['directorId'] != 0:
        directorURI = URIRef('http://ldf.fi/operasampo/persons_' + str(row['directorId']))
        graph.add((performanceURI, SCOP.directedBy, directorURI))

    # producer with producerId
    if row['producerId'] != 0:
        producerURI = URIRef('http://ldf.fi/operasampo/producers_' + str(row['producerId']))
        graph.add((performanceURI, SCOP.producedBy, producerURI))

    # place with placeId
    if not pd.isna(row['placeId']):
        placeURI = URIRef('http://ldf.fi/operasampo/places_' + str(row['placeId']))
        graph.add((performanceURI, SCOP.performedIn, placeURI))

    # season
    if not pd.isna(row['season']):
        graph.add((performanceURI, SCOP.season, Literal(row['season'])))
    
    # performanceDate
    if not pd.isna(row['performanceDate']):
        date = row['performanceDate'].split()[0] # take only date part from timestamp
        graph.add((performanceURI, SCOP.performanceDate, Literal(date, datatype=XSD.date)))

    # orchestra
    if not pd.isna(row['orchestra']):
        parsed_orchestra = ut.parse(row['orchestra'])
        for orchestra in parsed_orchestra.root.Orchestra:
            language_code = orchestra['language-id'][:2]
            graph.add((performanceURI, SCOP.orchestra, Literal(orchestra.cdata.replace('\\n', '<br>'), lang=language_code)))
    
    # tickets
    if not pd.isna(row['tickets']):
        parsed_tickets = ut.parse(row['tickets'])
        for ticket in parsed_tickets.root.Tickets:
            language_code = ticket['language-id'][:2]
            graph.add((performanceURI, SCOP.tickets, Literal(ticket.cdata.replace('\\n', '<br>'), lang=language_code)))

    # additionalInfo
    if not pd.isna(row['additionalInfo']):
        # parse all variations of additional info (= different language variants)
        parsed_info = ut.parse(row['additionalInfo'])
        # for each language variant, add information to graph with the correct language code
        for info in parsed_info.root.AdditionalInfo:
            language_code = info['language-id'][:2]
            # for text content, replace newlines (\n) with <br> for rendering in UI
            graph.add((performanceURI, SCOP.additionalInfo, Literal(info.cdata.replace('\\n', '<br>'), lang=language_code)))

    # extract name using performanceDate and additionalInfo
    extracted_name = extract_name(row)
    graph.add((performanceURI, SKOS.prefLabel, Literal(extracted_name, lang='fi')))

def create_performance_instances():
    graph = Graph()
    bind_namespaces(graph)

    performances_file = pd.read_csv('../csv/foc_Performance.csv', sep=";")
    
    print("Adding people..")
    for i, row in performances_file.iterrows():
        handle_performance_row(graph, row)
    
    print("Serializing performances.ttl..")
    graph.serialize('../ttl/performances.ttl', format='turtle')
