
## EUR-Lex Data Retrieval Notes

- SPARQL endpoint of the Publications Office of the European Union: http://publications.europa.eu/webapi/rdf/sparql
- Eurovoc only seeks to define labels that can be used to summarize all kind of subject matters addressed in EU documents.

## Notes on SPARQL

### Learning
- SPARQL Tutorial: https://docs.data.world/tutorials/sparql/
- SPARQL Examples – Select: https://codyburleson.com/blog/sparql-examples-select


- Variables start with a question mark

### SPARQL Statements

- `PREFIX`
  - Instead of having to use full IRIs in your query, you can use prefixed names.

```sparql  
`PREFIX cdm:<http://publications.europa.eu/ontology/cdm#>`
# ...
?resType = cdm:act_preparatory
# where cdm:act_preparatory is the IRI http://publications.europa.eu/ontology/cdm#act_preparatory
```

- `SELECT`
  - The SELECT query form returns variable bindings.
  - Returns all, or a subset of, the variables bound in a query pattern match.
  - appoints variables for the data your query will retrieve and display to the screen
- `WHERE`
  - specifies the data to pull out of your dataset


## Misc Notes

- IRIs: Internationalized Resource Identifiers
- URI: Uniform Resource Identifier
- Example of Turtle syntax/code: `@prefix dt:   <http://example.org/datatype#>`
- Example of SPARQL syntax/code: `PREFIX dt: <http://example.org/datatype#>`