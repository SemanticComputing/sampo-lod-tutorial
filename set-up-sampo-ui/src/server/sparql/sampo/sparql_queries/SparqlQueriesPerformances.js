const perspectiveID = 'performances'

export const performanceProperties = `
    {
      ?id skos:prefLabel ?prefLabel__id .
      BIND(?prefLabel__id AS ?prefLabel__prefLabel)
      BIND(CONCAT("/${perspectiveID}/page/", REPLACE(STR(?id), "^.*\\\\/(.+)", "$1")) AS ?prefLabel__dataProviderUrl)
      BIND(?id as ?uri__id)
      BIND(?id as ?uri__dataProviderUrl)
      BIND(?id as ?uri__prefLabel)
    }
    UNION
    {
      ?id scop:composition ?composition__id .
      ?composition__id skos:prefLabel ?composition__prefLabel .
      FILTER(LANG(?composition__prefLabel) = 'fi')
      BIND(CONCAT("/compositions/page/", REPLACE(STR(?composition__id), "^.*\\\\/(.+)", "$1")) AS ?composition__dataProviderUrl)
    }
    UNION
    {
      ?id scop:composition/scop:composedBy ?composer__id .
      ?composer__id skos:prefLabel ?composer__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?composer__id), "^.*\\\\/(.+)", "$1")) AS ?composer__dataProviderUrl)
    }
    UNION
    {
      ?id scop:composition/scop:libretist ?libretist__id .
      ?libretist__id skos:prefLabel ?libretist__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?libretist__id), "^.*\\\\/(.+)", "$1")) AS ?libretist__dataProviderUrl)
    }
    UNION
    {
      ?id scop:choirLeadBy ?choirLeader__id .
      ?choirLeader__id skos:prefLabel ?choirLeader__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?choirLeader__id), "^.*\\\\/(.+)", "$1")) AS ?choirLeader__dataProviderUrl)
    }
    UNION
    {
      ?id scop:conductedBy ?conductor__id .
      ?conductor__id skos:prefLabel ?conductor__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?conductor__id), "^.*\\\\/(.+)", "$1")) AS ?conductor__dataProviderUrl)
    }
    UNION
    {
      ?id scop:directedBy ?director__id .
      ?director__id skos:prefLabel ?director__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?director__id), "^.*\\\\/(.+)", "$1")) AS ?director__dataProviderUrl)
    }
    UNION
    {
      ?id scop:costumeDesignBy ?costumeDesigner__id .
      ?costumeDesigner__id skos:prefLabel ?costumeDesigner__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?costumeDesigner__id), "^.*\\\\/(.+)", "$1")) AS ?costumeDesigner__dataProviderUrl)
    }
    UNION
    {
      ?id scop:choreographyBy ?choreographer__id .
      ?choreographer__id skos:prefLabel ?choreographer__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?choreographer__id), "^.*\\\\/(.+)", "$1")) AS ?choreographer__dataProviderUrl)
    }
    UNION
    {
      ?id scop:scenographyBy ?scenographer__id .
      ?scenographer__id skos:prefLabel ?scenographer__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?scenographer__id), "^.*\\\\/(.+)", "$1")) AS ?scenographer__dataProviderUrl)
    }
    UNION
    {
      ?id scop:producedBy ?producer__id .
      ?producer__id skos:prefLabel ?producer__prefLabel .
      FILTER(LANG(?producer__prefLabel) = 'fi')
      BIND(CONCAT("/producers/page/", REPLACE(STR(?producer__id), "^.*\\\\/(.+)", "$1")) AS ?producer__dataProviderUrl)
    }
    UNION
    {
      ?id scop:language ?language .
    }
    UNION
    {
      ?id scop:translator ?translator__id .
      ?translator__id skos:prefLabel ?translator__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?translator__id), "^.*\\\\/(.+)", "$1")) AS ?translator__dataProviderUrl)
    }
    UNION
    {
      ?id scop:performanceDate ?performanceDate__id .
      BIND(STR(?performanceDate__id) as ?performanceDate__prefLabel)
    }
    UNION
    {
      ?id scop:performedIn ?place__id .
      ?place__id skos:prefLabel ?place__prefLabel .
      FILTER(LANG(?place__prefLabel) = 'fi')
      BIND(CONCAT("/places/page/", REPLACE(STR(?place__id), "^.*\\\\/(.+)", "$1")) AS ?place__dataProviderUrl)
    }
    UNION
    {
      ?id scop:season ?season .
    }
    UNION
    {
      ?id scop:orchestra ?orchestra .
      FILTER(LANG(?orchestra) = 'fi')
    }
    UNION
    {
      ?id scop:tickets ?tickets .
      FILTER(LANG(?tickets) = 'fi')
    }
    UNION
    {
      ?id scop:additionalInfo ?additionalInfo .
      FILTER(LANG(?additionalInfo) = 'fi')
    }
    UNION
    {
      ?id scop:editorNotes ?editorNotes .
    }
    UNION
    {
      ?compositionId a scop:Composition ;
                  ^scop:composition ?id .
      ?performanceRole__id a scop:Role ;
            scop:composition ?compositionId .
      OPTIONAL {
        ?performanceRoleId a scop:PerformanceRole ;
                        scop:performance ?id ;
                        scop:performer ?performerId ;
                        scop:compositionRole ?performanceRole__id .
        ?performerId skos:prefLabel ?performerLabel .
        BIND(CONCAT("/people/page/", REPLACE(STR(?performerId), "^.*\\\\/(.+)", "$1")) AS ?performanceRole__roleValues__dataProviderUrl)
      }
      BIND(COALESCE(?performerId, <http://ldf.fi/MISSING_VALUE>) as ?performanceRole__roleValues__id)
      BIND(COALESCE(?performerLabel, '-') as ?performanceRole__roleValues__prefLabel)
      ?performanceRole__id skos:prefLabel ?performanceRole__prefLabel .
      FILTER(LANG(?performanceRole__prefLabel) = 'fi')
      BIND(CONCAT("/roles/page/", REPLACE(STR(?performanceRole__id), "^.*\\\\/(.+)", "$1")) AS ?performanceRole__dataProviderUrl)
    }
    UNION 
    {
      ?otherPerformanceRoleId a scop:PerformanceRole ;
                      scop:performance ?id ;
                      scop:performer ?otherPerformer__id ;
                      scop:compositionRole <http://ldf.fi/operasampo/roles_unknown> .
      ?otherPerformer__id skos:prefLabel ?otherPerformer__prefLabel .
      BIND(CONCAT("/people/page/", REPLACE(STR(?otherPerformer__id), "^.*\\\\/(.+)", "$1")) AS ?otherPerformer__dataProviderUrl)
    }
    UNION 
    {
      ?id ^scop:performance ?image__id .
      ?image__id a scop:PerformanceImage ;
                scop:imageUrl ?image__url .
      OPTIONAL {
        ?image__id scop:copyright ?image__description .
      }
    }
`

export const performancesByConductorQuery = `
  SELECT ?category ?prefLabel (COUNT(DISTINCT ?performance) as ?instanceCount)
  WHERE {
    <FILTER>
    {
      ?performance a scop:Performance .
      ?performance scop:conductedBy ?category .
      ?category skos:prefLabel ?prefLabel .
    }
    UNION
    {
      ?performance a scop:Performance .
      FILTER NOT EXISTS {
        ?performance scop:conductedBy [] .
      }
      BIND("Tuntematon" as ?category)
      BIND("Tuntematon" as ?prefLabel)
    }
  }
  GROUP BY ?category ?prefLabel
  ORDER BY DESC(?instanceCount)
`

export const performancesByDirectorQuery = `
  SELECT ?category ?prefLabel (COUNT(DISTINCT ?performance) as ?instanceCount)
  WHERE {
    <FILTER>
    {
      ?performance a scop:Performance .
      ?performance scop:directedBy ?category .
      ?category skos:prefLabel ?prefLabel .
    }
    UNION
    {
      ?performance a scop:Performance .
      FILTER NOT EXISTS {
        ?performance scop:directedBy [] .
      }
      BIND("Tuntematon" as ?category)
      BIND("Tuntematon" as ?prefLabel)
    }
  }
  GROUP BY ?category ?prefLabel
  ORDER BY DESC(?instanceCount)
`

export const performancesByProducerQuery = `
  SELECT ?category ?prefLabel (COUNT(DISTINCT ?performance) as ?instanceCount)
  WHERE {
    <FILTER>
    {
      ?performance a scop:Performance ;
                  scop:producedBy ?category .
      ?category skos:prefLabel ?prefLabel .
    }
    UNION
    {
      ?performance a scop:Performance .
      FILTER NOT EXISTS {
        ?performance scop:producedBy [] .
      }
      BIND("Tuntematon" as ?category)
      BIND("Tuntematon" as ?prefLabel)
    }
  }
  GROUP BY ?category ?prefLabel
  ORDER BY DESC(?instanceCount)
`

export const performancesByComposerQuery = `
  SELECT ?category ?prefLabel (COUNT(DISTINCT ?performance) as ?instanceCount)
  WHERE {
    <FILTER>
    {
      ?performance a scop:Performance ;
                  scop:composition/scop:composedBy ?category .
      ?category skos:prefLabel ?prefLabel .
    }
    UNION
    {
      ?performance a scop:Performance .
      FILTER NOT EXISTS {
        ?performance scop:composition/scop:composedBy [] .
      }
      BIND("Tuntematon" as ?category)
      BIND("Tuntematon" as ?prefLabel)
    }
  }
  GROUP BY ?category ?prefLabel
  ORDER BY DESC(?instanceCount)
`

export const performancesByCompositionQuery = `
  SELECT ?category ?prefLabel (COUNT(DISTINCT ?performance) as ?instanceCount)
  WHERE {
    <FILTER>
    {
      ?performance a scop:Performance ;
                  scop:composition ?category .
      ?category skos:prefLabel ?prefLabel .
      FILTER(LANG(?prefLabel) = 'fi')
    }
    UNION
    {
      ?performance a scop:Performance .
      FILTER NOT EXISTS {
        ?performance scop:composition [] .
      }
      BIND("Tuntematon" as ?category)
      BIND("Tuntematon" as ?prefLabel)
    }
  }
  GROUP BY ?category ?prefLabel
  ORDER BY DESC(?instanceCount)
`

export const performancesByPerformancePlaceQuery = `
  SELECT ?category ?prefLabel (COUNT(DISTINCT ?performance) as ?instanceCount)
  WHERE {
    <FILTER>
    {
      ?performance a scop:Performance ;
                  scop:performedIn ?category .
      ?category skos:prefLabel ?prefLabel .
    }
    UNION
    {
      ?performance a scop:Performance .
      FILTER NOT EXISTS {
        ?performance scop:performedIn [] .
      }
      BIND("Tuntematon" as ?category)
      BIND("Tuntematon" as ?prefLabel)
    }
  }
  GROUP BY ?category ?prefLabel
  ORDER BY DESC(?instanceCount)
`

export const performancesByYearQuery = `
  SELECT ?category (COUNT (DISTINCT ?performance) as ?count) WHERE {
    <FILTER>
    ?performance a scop:Performance ;
                scop:performanceDate ?date .
    BIND(YEAR(xsd:date(?date)) as ?category)
  }
  GROUP BY ?category
  ORDER BY ?category
`
