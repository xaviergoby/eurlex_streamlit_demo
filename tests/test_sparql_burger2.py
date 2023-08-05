from SPARQLBurger.SPARQLQueryBuilder import *
import utils


# Creating the where statement
select_query = SPARQLSelectQuery(distinct=True, limit=50)
prefixes = utils.load_json_as_dict("eurlex_sparql_prefix_namespace_mapping")
select_query.add_prefixes(prefixes=prefixes)


select_query.add_variables(variables=[
		GroupConcatination("work", "cellarURIs", "|").get_text(),
		GroupConcatination("title", "workTitles", "|").get_text()
		])
select_query.add_variables(variables=["\n?mtype"])
select_query.add_variables(variables=[GroupConcatination("work", "cellarURIs", "|").get_text()])
select_query.add_variables(variables=["\n?date"])
select_query.add_variables(variables=[
		GroupConcatination("agentName", "authors", "|").get_text(),
		GroupConcatination("subjectLabel", "subjects", "|", distinct=False).get_text(),
		GroupConcatination("subject", "subject_ids", "|").get_text()
		])
select_query.add_variables(variables=["\n?workId"])
select_query.add_variables(variables=[GroupConcatination("celex", "celexIds", "|").get_text()])

###################################
# graph ?g {
#
# 		#?work rdf:type cdm:legislation_secondary .
# 		?work rdf:type ?resType .
# 		?work cdm:work_id_document ?workId .
# 		?work cdm:resource_legal_id_celex ?celex .
# 		?work cdm:work_date_document ?date .
# 		FILTER( ?date > "2014-01-01"^^xsd:date)
# 		FILTER(  ?resType = cdm:act_preparatory
# 		        || ?resType = cdm:decision_delegated
# 		        || ?resType = cdm:decision_implementing
# 		        || ?resType = cdm:decision
# 		        || ?resType = cdm:directive
# 		        || ?resType = cdm:guideline_ecb
# 		        || ?resType = cdm:regulation_delegated
# 		        || ?resType = cdm:regulation_implementing
# 		        || ?resType = cdm:regulation
# 		        )
#
#         ?work cdm:work_is_about_concept_eurovoc ?subject .
#
#         graph ?ga {
#             ?subject skos:prefLabel ?subjectLabel . # Select the prefLabel (preferred label) of the concept
#             FILTER (lang(?subjectLabel)="en")  # Keep just the English version of the prefLabel
#             }
#
#         FILTER( ?subject = <http://eurovoc.europa.eu/1016>  #	international finance
#                 || ?subject = <http://eurovoc.europa.eu/1918>  #	clearing agreement
#                 || ?subject = <http://eurovoc.europa.eu/2219>  #	international payment
#                 || ?subject = <http://eurovoc.europa.e

# Creating GRAPH G
graph_g = SPARQLGraphPattern(name="g")

# Adding triples <subject-predicate-object> to the graph
graph_g_triples = [
		Triple(subject="?work", predicate="rdf:type", object="?resType"),
		Triple(subject="?work", predicate="cdm:work_id_document", object="?workId"),
		Triple(subject="?work", predicate="cdm:resource_legal_id_celex", object="?celex"),
		Triple(subject="?work", predicate="cdm:work_date_document", object="?date"),
		]

graph_g.add_triples(triples=graph_g_triples)

graph_g_date_filter = Filter(expression="?date > '2014-01-01'^^xsd:date")
graph_g.add_filter(filter=graph_g_date_filter)

result_type_abbreviations = ["act_preparatory", "decision_delegated",
							 "decision_implementing", "decision",
							 "directive", "guideline_ecb",
							 "regulation_delegated",
							 "regulation_implementing", "regulation"]
result_types = []
for res_type in result_type_abbreviations:
	eq = Equality(left_term="?resType", right_term=f"cdm:{res_type}")
	result_types.append(eq)
	
graph_g_res_type_rel_op_seq = RelationalOperationSequence("||", result_types)
graph_g_res_type_rel_op_seq_exp = graph_g_res_type_rel_op_seq.get_text(indentation_depth=3)
graph_g_res_type_filter = Filter(expression=graph_g_res_type_rel_op_seq_exp)
graph_g.add_filter(filter=graph_g_res_type_filter)

graph_g_triples = [Triple(subject="?subject", predicate="cdm:expression_belongs_to_work", object="?work")]
graph_g.add_triples(triples=graph_g_triples)


###################################
#         graph ?ga {
#             ?subject skos:prefLabel ?subjectLabel . # Select the prefLabel (preferred label) of the concept
#             FILTER (lang(?subjectLabel)="en")  # Keep just the English version of the prefLabel
#             }

# Creating GRAPH GA
graph_ga = SPARQLGraphPattern(name="ga")

# Adding triples <subject-predicate-object> to the graph
graph_ga_triples = [Triple(subject="?subject", predicate="skos:prefLabel", object="?subjectLabel")]
graph_ga.add_triples(triples=graph_ga_triples)

graph_ga_filter_1 = Filter(expression="lang(?subjectLabel)='en'",)
graph_ga.add_filter(filter=graph_ga_filter_1)

eurovoc_subject_labels = []
eurovoc_codes_and_labels = utils.load_json_as_dict("eurovoc_codes_and_labels")

# for k, v in eurovoc_codes_and_labels.items():
for k, v in list(eurovoc_codes_and_labels.items())[:3]:
	eq = Equality(left_term="?subject", right_term=f"<http://eurovoc.europa.eu/{k}>")
	eurovoc_subject_labels.append(eq)
	
graph_g_filter_2_rel_op_seq = RelationalOperationSequence("||", eurovoc_subject_labels)
graph_g_filter_2_rel_op_seq_exp = graph_g_filter_2_rel_op_seq.get_text(indentation_depth=3)
graph_g_eurovoc_filter = Filter(expression=graph_g_filter_2_rel_op_seq_exp)
graph_g.add_filter(filter=graph_g_eurovoc_filter)


###################################
# graph_ge = SPARQLGraphPattern(name="ge")
# graph_ge.add_triples(triples=Triple(subject="?exp", predicate="cdm:expression_belongs_to_work", object="?work"))

# Finalisations
graph_g.add_nested_graph_pattern(graph_pattern=graph_ga)
select_query.set_where_pattern(graph_g)

# Print the graph pattern
# print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print(f"\ngraph_ga:\n{graph_ga.get_text()}")
print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(f"\nselect_query:\n{select_query.get_text()}")