# import SPARQLBurger as spqb
from SPARQLBurger.SPARQLQueryBuilder import SPARQLSelectQuery, SPARQLGraphPattern
from SPARQLBurger.SPARQLQueryBuilder import Prefix, Triple, GroupBy

# Create an object of class SPARQLSelectQuery and set the limit for the results to 100
select_query = SPARQLSelectQuery(distinct=True, limit=100)
select_query2 = SPARQLSelectQuery(distinct=True, limit=100)

# Add a prefix
select_query.add_prefix(
    prefix=Prefix(prefix="ex", namespace="http://www.example.com#")
)

select_query2.add_prefix(
    prefix=Prefix(prefix="cdm", namespace="http://publications.europa.eu/ontology/cdm#")
)

# Add the variables we want to select
select_query.add_variables(variables=["?person", "?age"])
select_query2.add_variables(variables=['\n(GROUP_CONCAT(distinct ?work;separator="|") as ?cellarURIs)',
									   '\n(GROUP_CONCAT(distinct ?title;separator="|") as ?workTitle)'])
# (GROUP_CONCAT(distinct ?work;separator="|") as ?cellarURIs)

# Create a graph pattern to use for the WHERE part and add some triples
where_pattern = SPARQLGraphPattern()
where_pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
            Triple(subject="?person", predicate="ex:hasAge", object="?age"),
            Triple(subject="?person", predicate="ex:address", object="?address"),
        ]
    )

where_pattern2 = SPARQLGraphPattern()
where_pattern2.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
            Triple(subject="?person", predicate="ex:hasAge", object="?age"),
            Triple(subject="?person", predicate="ex:address", object="?address"),
        ]
    )

# Set this graph pattern to the WHERE part
select_query.set_where_pattern(graph_pattern=where_pattern)

# Group the results by age
select_query.add_group_by(
    group=GroupBy(
        variables=["?age"]
    )
)

# Print the query we have defined
print(select_query.get_text())