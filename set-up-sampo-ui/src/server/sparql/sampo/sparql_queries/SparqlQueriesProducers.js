const perspectiveID = 'producers'

export const producerProperties = `
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
    ?id scop:additionalInfo ?additionalInfo .
    FILTER(LANG(?additionalInfo) = 'fi')
  }
  UNION
  {
    ?id ^scop:producedBy ?producedPerformances__id .
    ?producedPerformances__id a scop:Performance ;
                              scop:composition ?composition__id .
    ?composition__id a scop:Composition ;
                    skos:prefLabel ?composition__prefLabel .
    FILTER(LANG(?composition__prefLabel) = 'fi')
    ?producedPerformances__id skos:prefLabel ?producedPerformances__prefLabel .
    BIND(CONCAT("/performances/page/", REPLACE(STR(?producedPerformances__id), "^.*\\\\/(.+)", "$1")) AS ?producedPerformances__dataProviderUrl)
  }
`