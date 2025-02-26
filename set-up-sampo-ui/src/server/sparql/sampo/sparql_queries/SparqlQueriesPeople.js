const perspectiveID = 'people'

export const personProperties = `
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
    ?id foaf:firstName ?firstName .
  }
  UNION
  {
    ?id foaf:surname ?lastName .
  }
  UNION
  {
    ?id scop:dateOfBirth ?dateOfBirth .
  }
  UNION
  {
    ?id scop:placeOfBirth ?placeOfBirth .
  }
  UNION
  {
    ?id scop:dateOfDeath ?dateOfDeath .
  }
  UNION
  {
    ?id scop:placeOfDeath ?placeOfDeath .
  }
  UNION
  {
    ?id scop:additionalInfo ?additionalInfo .
    FILTER(LANG(?additionalInfo) = 'fi')
  }
  UNION
  {
    ?id ^scop:composedBy ?composedWork__id .
    ?composedWork__id skos:prefLabel ?composedWork__prefLabel .
    FILTER(LANG(?composedWork__prefLabel) = 'fi')
    BIND(CONCAT("/compositions/page/", REPLACE(STR(?composedWork__id), "^.*\\\\/(.+)", "$1")) AS ?composedWork__dataProviderUrl)
  }
  UNION
  {
    ?id ^scop:libretist ?libretto__id .
    ?libretto__id skos:prefLabel ?libretto__prefLabel .
    FILTER(LANG(?libretto__prefLabel) = 'fi')
    BIND(CONCAT("/compositions/page/", REPLACE(STR(?libretto__id), "^.*\\\\/(.+)", "$1")) AS ?libretto__dataProviderUrl)
  }
  UNION
  {
    ?id ^scop:performer ?pr .
    ?pr a scop:PerformanceRole ;
                    scop:compositionRole ?roleCharacter__id .
    ?roleCharacter__id skos:prefLabel ?prefLabel_ ;
                      scop:composition ?composition .
    FILTER(LANG(?prefLabel_) = 'fi')
    ?composition skos:prefLabel ?comp_pref_fi .
    FILTER(LANG(?comp_pref_fi) = 'fi')
    BIND(COALESCE(?prefLabel_, ?roleCharacter__id) as ?rc_pref)
    BIND(CONCAT(?rc_pref, " (", ?comp_pref_fi, ")") as ?roleCharacter__prefLabel)
    BIND(CONCAT("/roles/page/", REPLACE(STR(?roleCharacter__id), "^.*\\\\/(.+)", "$1")) AS ?roleCharacter__dataProviderUrl)
  }
  UNION
  {
    ?performanceRole__performanceRoleId a scop:PerformanceRole ;
          scop:performer ?id ;
          scop:performance ?performanceRole__roleValues__id ;
          scop:compositionRole ?performanceRole__id .
    ?performanceRole__roleValues__id skos:prefLabel ?performanceRole__roleValues__prefLabel .
    BIND(CONCAT("/performances/page/", REPLACE(STR(?performanceRole__roleValues__id), "^.*\\\\/(.+)", "$1")) AS ?performanceRole__roleValues__dataProviderUrl)
    ?performanceRole__id skos:prefLabel ?performanceRole__prefLabel .
    FILTER(LANG(?performanceRole__prefLabel) = 'fi')
    BIND(CONCAT("/roles/page/", REPLACE(STR(?performanceRole__id), "^.*\\\\/(.+)", "$1")) AS ?performanceRole__dataProviderUrl)
  }
`

export const personRolesQuery = `
  SELECT ?category ?prefLabel (COUNT(DISTINCT ?performance) as ?instanceCount)
  WHERE {
    BIND(<ID> as ?person)
    ?person a scop:Person .
    ?performanceRole a scop:PerformanceRole ;
                    scop:performer ?person ;
                    scop:performance ?performance .
    ?performanceRole scop:compositionRole ?category .
    OPTIONAL {
      ?category skos:prefLabel ?prefLabel_ .
      FILTER(LANG(?prefLabel_) = 'fi')
    }
    BIND(COALESCE(?prefLabel_, ?category) as ?prefLabel)
  }
  GROUP BY ?category ?prefLabel
  ORDER BY DESC(?instanceCount)
`

export const peopleByRelatedCompositionQuery = `
  SELECT ?category ?prefLabel (COUNT(DISTINCT ?person) as ?instanceCount)
  WHERE {
    <FILTER>
    {
      ?person a scop:Person ;
              (((^scop:performer/scop:performance)|^scop:conductedBy|^scop:directedBy|^scop:translator)/scop:composition)|^scop:composedBy|^scop:libretist ?category .
      ?category skos:prefLabel ?prefLabel .
      FILTER(LANG(?prefLabel) = 'fi')
    }
    UNION
    {
      ?person a scop:Person .
      FILTER NOT EXISTS {
        ?person (((^scop:performer/scop:performance)|^scop:conductedBy|^scop:directedBy|^scop:translator)/scop:composition)|^scop:composedBy|^scop:libretist [] .
      }
      BIND("Tuntematon" as ?category)
      BIND("Tuntematon" as ?prefLabel)
    }
  }
  GROUP BY ?category ?prefLabel
  ORDER BY DESC(?instanceCount)
`
