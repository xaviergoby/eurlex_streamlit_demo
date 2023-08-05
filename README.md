# EurLex Financial Domain Publications Querying & Retrieval "*Streamlit'ined*"

> This project/endeavour is strictly <b>NOT</b> associated with the Publications Office of the European Union, EUR-Lex nor any other entity whatsoever. This is strictly the work of (Alexander) Xavier Goby.


[//]: # (<p  float="left">)
<p style="text-align:center">
<a href="https://eurlexappdemo-4rnhk0qylob.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" width="175" height="60"/></a>
<a href="https://op.europa.eu/"><img src="docs/assets/images/OP_EU.png" width="140" height="45"/></a>
</p>


---


# SPARQL

[About SPARQL](https://data.europa.eu/en/about/sparql)


SPARQL protocol and RDF query language (SPARQL) defines a query language for RDF data, analogous to the Structured Query Language (SQL) for relational databases.

## SPARQL Endpoint

A service that accepts SPARQL queries and returns answers as SPARQL result sets. It is a best practice for dataset providers to give the URL of their SPARQL endpoint to allow access to their data programmatically or through a web interface.




View returned result by clicking [here](https://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=prefix+cdm%3A+%3Chttp%3A%2F%2Fpublications.europa.eu%2Fontology%2Fcdm%23%3E%0D%0A%0D%0A%0D%0Aselect+%3Fact%2C++%3Fdate_entry_into_force%2C+GROUP_CONCAT+%28%3FactID%2C%27%2C%27%29+as+%3FactIds%0D%0A%7B%0D%0A%3Fact+cdm%3Aresource_legal_in-force+%22true%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23boolean%3E.%0D%0A%3Fact+cdm%3Aresource_legal_date_entry-into-force+%3Fdate_entry_into_force.%0D%0A%3Fact+cdm%3Awork_id_document+%3FactID%0D%0AFILTER%28+%3Fdate_entry_into_force%3E%3D+%222022-01-01%22%5E%5Exsd%3Adate++%26%26+%3Fdate_entry_into_force%3C+%222023-01-01%22%5E%5Exsd%3Adate%29%0D%0A%7D%0D%0Aorder+by+%3Fdate_entry_into_force%0D%0A&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)
```sparksql
prefix cdm: <http://publications.europa.eu/ontology/cdm#>
select ?act,  ?date_entry_into_force, GROUP_CONCAT (?actID,',') as ?actIds
where {
?act cdm:resource_legal_in-force "true"^^<http://www.w3.org/2001/XMLSchema#boolean>.
?act cdm:resource_legal_date_entry-into-force ?date_entry_into_force.
?act cdm:work_id_document ?actID
FILTER( ?date_entry_into_force>= "2022-01-01"^^xsd:date  && ?date_entry_into_force< "2023-01-01"^^xsd:date)
}
order by ?date_entry_into_force
```

---


# European Union Official Publications & 

[European Union Research Guide: EUR-Lex
](https://libguides.law.umich.edu/c.php?g=863873&p=6233793)

- [E-Learning Module](https://eur-lex.europa.eu/e-learning/index.html)
  - > This e-learning module provides search tips that will enable you to make the most of EUR-Lex.
- [Browse by EuroVoc](https://eur-lex.europa.eu/browse/eurovoc.html)
- [Webtools](https://op.europa.eu/en/web/webtools/)

# What is CELEX & How are CELEX Numbers are Composed?

- [CELEX numbers](https://eur-lex.europa.eu/content/help/eurlex-content/celex-number.html#:~:text=A%20CELEX%20number%20has%20different,Water%20Framework%20Directive%20is%2032000L0060.)

- [How CELEX numbers are composed](https://eur-lex.europa.eu/content/tools/HowCelexNumbersAreComposed.pdf) - Version 26/01/2021

- [The CELEX number in EUR-Lex - Infographic](https://eur-lex.europa.eu/content/tools/eur-lex-celex-infographic-A3.pdf)

# What is Cellar?


## Cellar Data | Metadata | Knowledge graph

[Advanced SPARQL Query Editor](https://op.europa.eu/en/advanced-sparql-query-editor)

### Extracting publications and metadata from Cellar

> The complete metadata associated with a work can be extracted in XML or RDF format using the Cellar dissemination RESTFul interface. More details are given in the [metadata page](https://op.europa.eu/en/web/cellar/cellar-data/metadata). SPARQL queries can also be used for this purpose. You can customize your SPARQL query depending of what you want. This section give you some concrete examples.

#### Retrieve acts put in force in 2022 and still in force
View returned result by clicking [here](https://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=prefix+cdm%3A+%3Chttp%3A%2F%2Fpublications.europa.eu%2Fontology%2Fcdm%23%3E%0D%0A%0D%0A%0D%0Aselect+%3Fact%2C++%3Fdate_entry_into_force%2C+GROUP_CONCAT+%28%3FactID%2C%27%2C%27%29+as+%3FactIds%0D%0A%7B%0D%0A%3Fact+cdm%3Aresource_legal_in-force+%22true%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23boolean%3E.%0D%0A%3Fact+cdm%3Aresource_legal_date_entry-into-force+%3Fdate_entry_into_force.%0D%0A%3Fact+cdm%3Awork_id_document+%3FactID%0D%0AFILTER%28+%3Fdate_entry_into_force%3E%3D+%222022-01-01%22%5E%5Exsd%3Adate++%26%26+%3Fdate_entry_into_force%3C+%222023-01-01%22%5E%5Exsd%3Adate%29%0D%0A%7D%0D%0Aorder+by+%3Fdate_entry_into_force%0D%0A&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)
```sparksql
prefix cdm: <http://publications.europa.eu/ontology/cdm#>
select ?act,  ?date_entry_into_force, GROUP_CONCAT (?actID,',') as ?actIds
where {
?act cdm:resource_legal_in-force "true"^^<http://www.w3.org/2001/XMLSchema#boolean>.
?act cdm:resource_legal_date_entry-into-force ?date_entry_into_force.
?act cdm:work_id_document ?actID
FILTER( ?date_entry_into_force>= "2022-01-01"^^xsd:date  && ?date_entry_into_force< "2023-01-01"^^xsd:date)
}
order by ?date_entry_into_force
```

# Uncategorized Links

- https://eur-lex.europa.eu/content/tools/webservices/SearchWebServiceUserManual_v2.00.pdf
- https://eur-lex.europa.eu/content/welcome/data-reuse.html
- https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/cdm
- https://github.com/kevin91nl/eurlex
- https://github.com/kevin91nl/salience-detection
- https://github.com/mangiafico/eurlex-python/tree/master
- https://github.com/ndrplz/eurlex-toolbox
- https://mscottodivettimo.github.io/project/oeil_app/
- https://mscottodivettimo.github.io/files/oeil_app/oeil_app_documentation.pdf
- https://github.com/seljaseppala/eu_corpus_compiler/tree/master

- https://eur-lex.europa.eu/content/help/eurlex-content/celex-number.html#:~:text=A%20CELEX%20number%20is%20a,on%20the%20type%20of%20document.

- https://op.europa.eu/en/web/cellar/cellar-data/metadata/knowledge-graph

- https://op.europa.eu/en/web/cellar/cellar-data/metadata/knowledge-graph
- https://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=prefix+cdm%3A+%3Chttp%3A%2F%2Fpublications.europa.eu%2Fontology%2Fcdm%23%3E%0D%0A%0D%0A%0D%0Aselect+%3Fact%2C++%3Fdate_entry_into_force%2C+GROUP_CONCAT+%28%3FactID%2C%27%2C%27%29+as+%3FactIds%0D%0A%7B%0D%0A%3Fact+cdm%3Aresource_legal_in-force+%22true%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23boolean%3E.%0D%0A%3Fact+cdm%3Aresource_legal_date_entry-into-force+%3Fdate_entry_into_force.%0D%0A%3Fact+cdm%3Awork_id_document+%3FactID%0D%0AFILTER%28+%3Fdate_entry_into_force%3E%3D+%222022-01-01%22%5E%5Exsd%3Adate++%26%26+%3Fdate_entry_into_force%3C+%222023-01-01%22%5E%5Exsd%3Adate%29%0D%0A%7D%0D%0Aorder+by+%3Fdate_entry_into_force%0D%0A&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+
- [VocBench](https://vocbench.uniroma2.it/)

