# Notes


- Cellar is the <em>semantic web technologies</em> based common database/repository of the Publications Office of the European Union. Its endpoint is http://publications.europa.eu/webapi/rdf/sparql
    - [The Ontology-based Approach of the Publications Office of the EU for Document Accessibility and Open Data Services](https://www.ai.rug.nl/~verheij/ssail2019/readings/Francesconi-EGOVIS2015.pdf)
    - Cellar is used by:
      - EUR-Lex
        - EUR-Lex is the online entry to search and retrieve EU Legal publications. Cellar is the storage base of EUR-Lex, from where EUR-Lex retrieves the EU Legal publications and their metadata.
      - OP Portal
        - The OP Portal is the online entry to search and retrieve EU general publications and other types of publications and data. OP Portal retrieves the EU general publications and their metadata from Cellar.


- '(expression)' expression is treated as a unit and may be combined as described in this list.
- 'A?' matches A or nothing; optional A.
- 'A | B' matches A or B.
- 'A+' matches 1 or more occurrences of A. Concatenation has higher precedence than alternation; thus A+ | B+ is identical to (A+) (B+).

---
- SelectQuery	  ::=  	SelectClause DatasetClause* WhereClause SolutionModifier
- SelectClause	  ::=  	'SELECT' ( 'DISTINCT' | 'REDUCED' )? ( ( Var | ( '(' Expression 'AS' Var ')' ) )+ | '*' )
- WhereClause	  ::=  	'WHERE'? GroupGraphPattern
- GroupGraphPattern	  ::=  	'{' ( SubSelect | GroupGraphPatternSub ) '}'
- GroupGraphPatternSub	  ::=  	TriplesBlock? ( GraphPatternNotTriples '.'? TriplesBlock? )*
- GraphPatternNotTriples	  ::=  	GroupOrUnionGraphPattern | OptionalGraphPattern | MinusGraphPattern | GraphGraphPattern | ServiceGraphPattern | Filter | Bind | InlineData
- GraphGraphPattern	  ::=  	'GRAPH' VarOrIri GroupGraphPattern
- Filter	  ::=  	'FILTER' Constraint
- Constraint	  ::=  	BrackettedExpression | BuiltInCall | FunctionCall
- BrackettedExpression	  ::=  	'(' Expression ')'


---


import requests
import json
import pprint
eurovoc_id = 560
# headers = {"charset": "utf-8", "Content-Type": "application/json"}
# headers = {"charset": "utf-8", "Content-Type": "text/html"}
headers = {"charset": "utf-8", "Content-Type": "application/xml"}
# uri = f"https://publications.europa.eu/resource/authority/eurovoc/{str(eurovoc_id)}"
# url = f"https://op.europa.eu/en/web/eu-vocabularies/concept/-/resource?uri={uri}"
url = f"http://publications.europa.eu/resource/celex/{eurovoc_id}"
res = requests.get(url, headers=headers)
content = res.content
# content = json.reads(res.content)
pprint.pprint(content)
print(f"Request->Response Status Code:{res.status_code}")
print(f"Request->Response Reason:{res.content.decode()}")
print(f"Content type: {type(content)}")
print(f"type(res.content.decode()) type: {type(res.content.decode())}")
content_dict = json.dumps(res.content.decode())
print(f"content_dict:{content_dict}")

'SELECT' ( 'DISTINCT' | 'REDUCED' )? ( ( Var | ( '(' Expression 'AS' Var ')' ) )+ | '*' )

SELECT
SELECT DISTINCT
(GROUP_CONCAT(distinct ?work;separator="|") as ?cellarURIs)


---

Mine: ?manif cdm:manifestation_type ?mtype .

Ref: {?manif cdm:manifestation_type ?mtype .}


---

- [Publications Office Web Guide | Define and plan | URLs](https://op.europa.eu/en/web/webguide/urls)
- [Publications Office Web Guide | Define and plan | URIs](https://op.europa.eu/en/web/webguide/uris)

https://op.europa.eu/en/web/cellar/cellar-data/metadata/metadata-notices


https://eur-lex.europa.eu/content/help/data-reuse/linking.html


https://eur-lex.europa.eu/content/help/eurlex-content/experimental-features.html


- [Identifiers request | URL to request] http://publications.europa.eu/resource/{ps-name}/{ps-id}
  - Parameters
    - {ps-name} is a valid production system name 
    - {ps-id} is a valid production system id identifying a work, and compatible with its {ps-name}
  - The following HTTP headers may be set on the request:
    - For a given resource:
      - `Accept:application/xml;notice=identifiers.`
- RDF request | URL to request:
  - http://publications.europa.eu/resource/{ps-name}/{ps-id}
- XML request | URL to request:
  - http://publications.europa.eu/resource/{ps-name}/{ps-id}?language={dec-lang}&filter={in_notice-only}

- List of available resource types: http://publications.europa.eu/resource/authority/resource-type
- Cellar SPARQL Endpoint URL: "http://publications.europa.eu/webapi/rdf/sparql"
- A resource ID, e.g. CELEX or Cellar URI: "http://publications.europa.eu/resource/celex/32014R0001"
- A EuroVoc concept URI: "http://eurovoc.europa.eu/100142"



