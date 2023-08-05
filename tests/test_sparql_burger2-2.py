from SPARQLBurger.SPARQLQueryBuilder import *
import utils


# SELECT QUERY PATTERN
select_query = SPARQLSelectQuery(distinct=True, limit=50)

prefixes = utils.load_json_as_dict("eurlex_sparql_prefix_namespace_mapping")
select_query.add_prefixes(prefixes=prefixes)
variables = [GroupConcatination("work", "cellarURIs", "|").get_text(),
			 GroupConcatination("title", "workTitles", "|").get_text(),
			 "\n?mtype",
			 GroupConcatination("work", "cellarURIs", "|").get_text(),
			 "\n?date", GroupConcatination("agentName", "authors", "|").get_text(),
			 GroupConcatination("subjectLabel", "subjects", "|", distinct=False).get_text(),
			 GroupConcatination("subject", "subject_ids", "|").get_text(),
			 "\n?workId",
			 GroupConcatination("celex", "celexIds", "|").get_text()]

for var in variables:
	select_query.add_variables(variables=[var])
	
# WHERE (GRAPH) PATTERN
where_graph = SPARQLGraphPattern()


# GRAPH G
graph_g = SPARQLGraphPattern(name="g")
graph_g_triples = [
		Triple(subject="?work", predicate="rdf:type", object="?resType"),
		Triple(subject="?work", predicate="cdm:work_id_document", object="?workId"),
		Triple(subject="?work", predicate="cdm:resource_legal_id_celex", object="?celex"),
		Triple(subject="?work", predicate="cdm:work_date_document", object="?date"),
		]
graph_g.add_triples(triples=graph_g_triples)

# GRAPH GA
graph_ga = SPARQLGraphPattern(name="ga")
graph_ga_triples = [Triple(subject="?subject", predicate="skos:prefLabel", object="?subjectLabel")]
graph_ga.add_triples(triples=graph_ga_triples)
graph_ga_filter_1 = Filter(expression="lang(?subjectLabel)='en'",)
graph_ga.add_filter(filter=graph_ga_filter_1)


##################
# graph_g.add_nested_graph_pattern(graph_pattern=graph_ga)
# select_query.set_where_pattern(graph_g)

#     graph ?gagent {
#         {?work cdm:work_contributed_to_by_agent ?agent .}
#         union
#         {?work cdm:work_created_by_agent ?agent . }
#         union
#         {?work cdm:work_authored_by_agent ?agent . }
#    }

first_pattern = SPARQLGraphPattern()
first_pattern_triples = [Triple(subject="?work", predicate="cdm:work_contributed_to_by_agent", object="?agent")]
first_pattern.add_triples(triples=first_pattern_triples)
second_pattern = SPARQLGraphPattern(union=True)
second_pattern_triples = [Triple(subject="?work", predicate="cdm:work_created_by_agent", object="?agent")]
second_pattern.add_triples(triples=second_pattern_triples)
third_pattern = SPARQLGraphPattern(union=True)
third_pattern_triples = [Triple(subject="?work", predicate="cdm:work_authored_by_agent", object="?agent")]
third_pattern.add_triples(triples=third_pattern_triples)
graph_gagent = SPARQLGraphPattern(name="gagent")
graph_gagent.add_nested_graph_pattern(graph_pattern=first_pattern)
graph_gagent.add_nested_graph_pattern(graph_pattern=second_pattern)
graph_gagent.add_nested_graph_pattern(graph_pattern=third_pattern)

graph_g.add_nested_graph_pattern(graph_pattern=graph_ga)
where_graph.add_nested_graph_pattern(graph_pattern=graph_g)
where_graph.add_nested_graph_pattern(graph_pattern=graph_gagent)
select_query.set_where_pattern(where_graph)

# Print the graph pattern
# print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print(f"\ngraph_ga:\n{graph_ga.get_text()}")
print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(f"\nselect_query:\n{select_query.get_text()}")