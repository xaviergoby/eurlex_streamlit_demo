from SPARQLBurger.SPARQLQueryBuilder import *
import utils

class EURLexSPARQLQueryBuilder:
	
	def __init__(self, distinct=True, limit=50):
		self.distinct = distinct
		self.limit = limit
		self.select_query = SPARQLSelectQuery(distinct=distinct, limit=limit)
		self.prefixes = utils.load_json_as_dict("eurlex_sparql_prefix_namespace_mapping")
		self.variables = [GroupConcatination("work", "cellarURIs", "|").get_text(),
						  GroupConcatination("title", "workTitles", "|").get_text(),
						  GroupConcatination("langIdentifier", "lang", "|").get_text(),
						  "\n?mtype",
						  GroupConcatination("resType", "workTypes", "|").get_text(),
						  "\n?date",
						  GroupConcatination("agentName", "authors", "|").get_text(),
						  GroupConcatination("subjectLabel", "subjects", "|", distinct=False).get_text(),
						  GroupConcatination("subject", "subject_ids", "|").get_text(),
						  "\n?workId",
						  GroupConcatination("celex", "celexIds", "|").get_text()
						  ]
		self.where_graph = SPARQLGraphPattern()
		self.graph_g = SPARQLGraphPattern(name="g")
		self.graph_ga = SPARQLGraphPattern(name="ga")
		self.graph_ge = SPARQLGraphPattern(name="ge")
		self.graph_lgc = SPARQLGraphPattern(name="lgc")
		self.graph_gagent = SPARQLGraphPattern(name="gagent")
		self.graph_gaa = SPARQLGraphPattern(name="gaa")
		self.graph_gm = SPARQLGraphPattern(name="gm")
		
		# self.add_prefixes()
		# self.add_variables()
		
	def add_prefixes(self):
		self.select_query.add_prefixes(prefixes=self.prefixes)
		
	def add_variables(self):
		for variable in self.variables:
			self.select_query.add_variables(variables=[variable])
			
	def add_graph_g_triples(self):
		graph_g_triples = [
			Triple(subject="?work", predicate="rdf:type", object="?resType"),
			Triple(subject="?work", predicate="cdm:work_id_document", object="?workId"),
			Triple(subject="?work", predicate="cdm:resource_legal_id_celex", object="?celex"),
			Triple(subject="?work", predicate="cdm:work_date_document", object="?date"),
			Triple(subject="?work", predicate="cdm:work_is_about_concept_eurovoc", object="?subject")
			]
		self.graph_g.add_triples(triples=graph_g_triples)
		
	def add_graph_g_date_filter(self, earliest_pub_date):
		graph_g_date_filter = Filter(expression=f"?date > '{earliest_pub_date}'^^xsd:date")
		self.graph_g.add_filter(filter=graph_g_date_filter)

	def add_graph_g_res_type_filter(self):
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
		self.graph_g.add_filter(filter=graph_g_res_type_filter)
		
	def add_graph_g_eurovoc_subjects_filter(self, subjects=None):
		eurovoc_subject_labels = []
		eurovoc_codes_and_labels = utils.load_json_as_dict("eurovoc_codes_and_labels")
		if subjects is None:
			selected_eurovoc_codes_and_labels = eurovoc_codes_and_labels
		else:
			selected_eurovoc_codes_and_labels = {k:v for k, v in eurovoc_codes_and_labels.items() if v in [subj.lower() for subj in subjects]}
		
		for k, v in list(selected_eurovoc_codes_and_labels.items()):
			eq = Equality(left_term="?subject", right_term=f"<http://eurovoc.europa.eu/{k}>")
			eurovoc_subject_labels.append(eq)
		
		graph_g_filter_2_rel_op_seq = RelationalOperationSequence("||", eurovoc_subject_labels)
		graph_g_filter_2_rel_op_seq_exp = graph_g_filter_2_rel_op_seq.get_text(indentation_depth=3)
		graph_g_eurovoc_filter = Filter(expression=graph_g_filter_2_rel_op_seq_exp)
		self.graph_g.add_filter(filter=graph_g_eurovoc_filter)
		
	def add_graph_ga_triples(self):
		graph_ga_triples = [Triple(subject="?subject", predicate="skos:prefLabel", object="?subjectLabel")]
		self.graph_ga.add_triples(triples=graph_ga_triples)
		
	def add_graph_ga_language_filter(self):
		graph_ga_language_filter = Filter(expression="lang(?subjectLabel)='en'",)
		self.graph_ga.add_filter(filter=graph_ga_language_filter)
		
	def add_graph_ge_triples(self):
		graph_ge_triples = [
			Triple(subject="?exp", predicate="cdm:expression_belongs_to_work", object="?work"),
			Triple(subject="?exp", predicate="cdm:expression_title", object="?title"),
			Triple(subject="?exp", predicate="cdm:expression_uses_language", object="?lg")
			]
		self.graph_ge.add_triples(triples=graph_ge_triples)
		
	def add_graph_ge_language_filter(self):
		graph_ge_language_filter = Filter(expression="lang(?title)='en' or lang(?title)='eng' or lang(?title)=''")
		self.graph_ge.add_filter(filter=graph_ge_language_filter)
		
	def add_graph_lgc_triples(self):
		graph_lgc_triples = [Triple(subject="?lg", predicate="dc:identifier", object="?langIdentifier")]
		self.graph_lgc.add_triples(triples=graph_lgc_triples)
		
	def add_graph_ge_lang_identifier_filter(self):
		graph_ge_lang_identifier_filter = Filter(expression='str(?langIdentifier)="ENG"')
		self.graph_ge.add_filter(filter=graph_ge_lang_identifier_filter)
		
	def add_graph_gagent_triples(self):
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
		self.graph_gagent.add_nested_graph_pattern(graph_pattern=first_pattern)
		self.graph_gagent.add_nested_graph_pattern(graph_pattern=second_pattern)
		self.graph_gagent.add_nested_graph_pattern(graph_pattern=third_pattern)
		
		
	def add_graph_gaa_triples(self):
		graph_gaa_triples = [Triple(subject="?agent", predicate="skos:prefLabel", object="?agentName")]
		self.graph_gaa.add_triples(triples=graph_gaa_triples)
		
	def add_graph_gaa_language_filter(self):
		graph_gaa_language_filter = Filter(expression='lang(?agentName)="en"',)
		self.graph_gaa.add_filter(filter=graph_gaa_language_filter)
		
	def add_graph_gm_triples(self):
		graph_gm_triples = [Triple(subject="?manif", predicate="cdm:manifestation_manifests_expression", object="?exp"),
							Triple(subject="?manif", predicate="cdm:manifestation_type", object="?mtype"),]
		self.graph_gm.add_triples(triples=graph_gm_triples)
		
	def add_graph_gm_mtype_filter(self):
		result_type_abbreviations = ["html", "html_simpl",
									 "txt", "xhtml",
									 "xhtml_simpl"]
		result_types = []
		for res_type in result_type_abbreviations:
			eq = Equality(left_term="str(?mtype)", right_term=f'"{res_type}"')
			result_types.append(eq)
		
		graph_gm_res_type_rel_op_seq = RelationalOperationSequence("||", result_types)
		graph_gm_res_type_rel_op_seq_exp = graph_gm_res_type_rel_op_seq.get_text(indentation_depth=3)
		graph_gm_res_type_filter = Filter(expression=graph_gm_res_type_rel_op_seq_exp)
		self.graph_gm.add_filter(filter=graph_gm_res_type_filter)
		
		
	def finalize(self):
		self.graph_g.add_nested_graph_pattern(graph_pattern=self.graph_ga)
		self.graph_ge.add_nested_graph_pattern(graph_pattern=self.graph_lgc)
		
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_g)
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_ge)
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_gagent)
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_gaa)
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_gm)
		
		self.select_query.set_where_pattern(self.where_graph)
		
	def build(self, subjects=None, earliest_publication_date="2014-01-01"):
		# self.add_prefixes()
		# self.add_variables()
		self.add_graph_g_triples()
		self.add_graph_g_date_filter(earliest_pub_date=earliest_publication_date)
		self.add_graph_g_res_type_filter()
		# self.add_graph_g_triples_2()
		self.add_graph_g_eurovoc_subjects_filter(subjects=subjects)
		self.add_graph_ga_triples()
		self.add_graph_ga_language_filter()
		self.add_graph_ge_triples()
		self.add_graph_ge_language_filter()
		self.add_graph_lgc_triples()
		self.add_graph_ge_lang_identifier_filter()
		self.add_graph_gagent_triples()
		self.add_graph_gaa_triples()
		self.add_graph_gaa_language_filter()
		self.add_graph_gm_triples()
		self.add_graph_gm_mtype_filter()
		self.finalize()
		
	def get_text(self, order_by="desc", indent_depth=0):
		query_txt = self.select_query.get_text(indentation_depth=indent_depth)
		if order_by == "desc":
			query_txt = query_txt.replace(f"LIMIT {self.limit}", f"ORDER BY DESC(?date)\nLIMIT {self.limit}")
		elif order_by == "asc":
			query_txt = query_txt.replace(f"LIMIT {self.limit}", f"ORDER BY ASC(?date)\nLIMIT {self.limit}")
		else:
			pass
		return query_txt
		
	
if __name__ == "__main__":
	import pprint
	import pandas as pd
	pd.set_option('display.max_rows', 500)
	pd.set_option('display.max_columns', 500)
	pd.set_option('display.width', 1000)
	import utils
	
	
	res_limit = 10
	eurlex_sparql_query_builder = EURLexSPARQLQueryBuilder(distinct=True, limit=res_limit)
	# eurlex_sparql_query_builder.build(subjects=None)
	eurlex_sparql_query_builder.build(subjects=None, earliest_publication_date="2020-01-01")
	# selected_subjects = ["selling price", "clearing agreement",
	# 					 "international payment", "regulation of investments",
	# 					 "investment policy", "private investment", "investment promotion",]
	# eurlex_sparql_query_builder.build(subjects=selected_subjects)
	# Print the graph pattern
	query = eurlex_sparql_query_builder.get_text(indent_depth=0)
	# print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	# print(f"\nselect_query:\n{query}")
	# qq = query.replace(f"LIMIT {res_limit}", f"ORDER BY DESC(?date)\nLIMIT {res_limit}")
	
	
	# results = get_sparql_query_results(qq)
	results = utils.get_sparql_query_results(query)
	# pprint.pprint(results)
	
	res = results["results"]["bindings"]
	
	
	# df1 = convert_sparql_output_to_dataframe({'results': {'bindings': [{'subject': {'value': 'cdm:test'}}]}}).to_dict()
	# df1 = convert_sparql_output_to_dataframe(results)
	df1 = utils.convert_sparql_output_to_df(results)
	print(df1)
	
	# df2 = get_celex_dataframe(df1.loc[0]["celexIds"])
	df2 = utils.get_celex_id_as_df(df1.loc[0]["celexIds"])
	# print(df2)