from SPARQLBurger.SPARQLQueryBuilder import *
import utils


class EURLexSPARQLQueryConstructor:
	
	
	def __init__(self, distinct=True, limit=10, order_by="desc",
	             prefix_mapping_json_name="eurlex_sparql_prefix_namespace_mapping"):
		self.__distinct = distinct
		self.__limit = limit
		self.__order_by = order_by
		self.__earliest_pub_date = None
		self.__subjects = None
		self.__prefix_mapping_json_name = prefix_mapping_json_name
		self.__prefixes = utils.load_json_as_dict(self.__prefix_mapping_json_name)
		# self.select_query = SPARQLSelectQuery(distinct=self.__distinct, limit=limit, order_by=self.__order_by)
		# self.__select_query = SPARQLSelectQuery(distinct=self.__distinct, limit=limit, order_by=self.__order_by)
		self.__select_query = None
		# self.__select_query_initiated = False
		self.__variables = [GroupConcatination("work", "cellarURIs", "|").get_text(),
		# self.__variables = [GroupConcatination("work", "cellarURIs", "|", distinct=False).get_text(),
		                    GroupConcatination("title", "workTitles", "|").get_text(),
		                    GroupConcatination("langIdentifier", "lang", "|").get_text(),
		                    "\n?mtype",
		                    GroupConcatination("resType", "workTypes", "|").get_text(),
		                    "\n?date",
		                    # GroupConcatination("date", "pubDates", "|", distinct=False).get_text(),
		                    GroupConcatination("agentName", "authors", "|").get_text(),
		                    GroupConcatination("subjectLabel", "subjects", "|", distinct=False).get_text(),
		                    GroupConcatination("subject", "subject_ids", "|").get_text(),
		                    "\n?workId",
		                    # GroupConcatination("workId", "workIds", "|").get_text(),
		                    GroupConcatination("celex", "celexIds", "|").get_text()]
		self.where_graph = SPARQLGraphPattern()
		# self.__where_graph = None
		self.graph_g = SPARQLGraphPattern(name="g")
		# self.graph_g = None
		self.graph_ga = SPARQLGraphPattern(name="ga")
		# self.graph_ga = None
		self.graph_ge = SPARQLGraphPattern(name="ge")
		# self.graph_ge = None
		self.graph_lgc = SPARQLGraphPattern(name="lgc")
		# self.graph_lgc = None
		self.graph_gagent = SPARQLGraphPattern(name="gagent")
		# self.graph_gagent = None
		self.graph_gaa = SPARQLGraphPattern(name="gaa")
		# self.graph_gaa = None
		self.graph_gm = SPARQLGraphPattern(name="gm")
		# self.graph_gm = None
		
		self.__query_str = None
	
	
	@property
	def select_query(self):
		if self.__select_query is None:
			# self.__select_query = SPARQLSelectQuery(distinct=self.__distinct, limit=self.__limit, order_by=self.__order_by)
			# self.__setup_select_query()
			self.__init_select_query(self.__distinct, self.__limit, self.__order_by)
		return self.__select_query
	
	
	# def __init_select_query(self):
	# 	self.__select_query = SPARQLSelectQuery(distinct=self.__distinct, limit=self.__limit, order_by=self.__order_by)
	
	def __add_prefixes(self):
		self.__select_query.add_prefixes(prefixes=self.__prefixes)
	
	
	def __add_variables(self):
		for variable in self.__variables:
			self.__select_query.add_variables(variables=[variable])
	
	
	# def __setup_select_query(self):
	# def __init_select_query(self):
	# def __init_select_query(self, distinct=True, limit=10, order_by="desc"):
	def __init_select_query(self, distinct, limit, order_by):
		# self.__init_select_query()
		# self.__select_query = SPARQLSelectQuery(distinct=self.__distinct, limit=self.__limit, order_by=self.__order_by)
		self.__select_query = SPARQLSelectQuery(distinct, limit, order_by)
		self.__add_prefixes()
		self.__add_variables()
	
	
	# def __init_select_query(self):
	# 	self.__init_select_query()
	# self.__select_query = SPARQLSelectQuery(distinct=self.__distinct, limit=self.__limit, order_by=self.__order_by)
	# self.__add_prefixes()
	# self.__add_variables()
	
	def init_select_query(self, distinct, limit, order_by):
		# self.__setup_select_query()
		self.__init_select_query(distinct, limit, order_by)
	
	
	# @property
	# def select_query(self):
	# 	if self.__select_query is None:
	# 		if self.__select_query_initiated is False:
	# 			self.__init_select_query()
	# 			self.__select_query_initiated = True
	# 	return self.__select_query
	
	
	# def __init_where_graph(self):
	# 	self.__where_graph = SPARQLGraphPattern()
	#
	# @property
	# def where_graph(self):
	# 	if self.__where_graph is None:
	# 		self.__init_where_graph()
	# 	return self.__where_graph
	
	def __add_graph_g_triples(self):
		graph_g_triples = [
				Triple(subject="?work", predicate="rdf:type", object="?resType"),
				Triple(subject="?work", predicate="cdm:work_date_document", object="?date"),
				Triple(subject="?work", predicate="cdm:resource_legal_id_celex", object="?celex"),
				Triple(subject="?work", predicate="cdm:work_date_document", object="?date"),
				Triple(subject="?work", predicate="cdm:work_is_about_concept_eurovoc", object="?subject")
				]
		self.graph_g.add_triples(triples=graph_g_triples)
	
	
	def __add_graph_g_date_filter(self, earliest_pub_date):
		graph_g_date_filter = Filter(expression=f"?date > '{earliest_pub_date}'^^xsd:date")
		self.graph_g.add_filter(filter=graph_g_date_filter)
	
	
	def __add_graph_g_res_type_filter(self):
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
	
	
	def __add_graph_g_eurovoc_subjects_filter(self, subjects):
		eurovoc_subject_labels = []
		eurovoc_ids_n_labels = utils.load_json_as_dict("eurovoc_codes_and_labels")
		if subjects is None:
			selected_eurovoc_codes_and_labels = eurovoc_ids_n_labels
		else:
			selected_subjects = [subj.lower() for subj in subjects]
			selected_eurovoc_codes_and_labels = {k: v for k, v in eurovoc_ids_n_labels.items() if v in selected_subjects}
		
		for k, v in list(selected_eurovoc_codes_and_labels.items()):
			eq = Equality(left_term="?subject", right_term=f"<http://eurovoc.europa.eu/{k}>")
			eurovoc_subject_labels.append(eq)
		
		graph_g_filter_2_rel_op_seq = RelationalOperationSequence("||", eurovoc_subject_labels)
		graph_g_filter_2_rel_op_seq_exp = graph_g_filter_2_rel_op_seq.get_text(indentation_depth=3)
		graph_g_eurovoc_filter = Filter(expression=graph_g_filter_2_rel_op_seq_exp)
		self.graph_g.add_filter(filter=graph_g_eurovoc_filter)
	
	
	def __add_graph_ga_triples(self):
		graph_ga_triples = [Triple(subject="?subject", predicate="skos:prefLabel", object="?subjectLabel")]
		self.graph_ga.add_triples(triples=graph_ga_triples)
	
	
	def __add_graph_ga_language_filter(self):
		graph_ga_language_filter = Filter(expression="lang(?subjectLabel)='en'", )
		self.graph_ga.add_filter(filter=graph_ga_language_filter)
	
	
	def __add_graph_ge_triples(self):
		graph_ge_triples = [
				Triple(subject="?exp", predicate="cdm:expression_belongs_to_work", object="?work"),
				Triple(subject="?exp", predicate="cdm:expression_title", object="?title"),
				Triple(subject="?exp", predicate="cdm:expression_uses_language", object="?lg")
				]
		self.graph_ge.add_triples(triples=graph_ge_triples)
	
	
	def __add_graph_ge_language_filter(self):
		graph_ge_language_filter = Filter(expression="lang(?title)='en' or lang(?title)='eng' or lang(?title)=''")
		self.graph_ge.add_filter(filter=graph_ge_language_filter)
	
	
	def __add_graph_ge_lang_identifier_filter(self):
		graph_ge_lang_identifier_filter = Filter(expression='str(?langIdentifier)="ENG"')
		self.graph_ge.add_filter(filter=graph_ge_lang_identifier_filter)
	
	
	def __add_graph_lgc_triples(self):
		graph_lgc_triples = [Triple(subject="?lg", predicate="dc:identifier", object="?langIdentifier")]
		self.graph_lgc.add_triples(triples=graph_lgc_triples)
	
	
	def __add_graph_gagent_triples(self):
		# graph_gagent = SPARQLGraphPattern(name="gagent")
		first_pattern = SPARQLGraphPattern()
		# first_pattern = SPARQLGraphPattern(name="gagent")
		first_pattern_triples = [Triple(subject="?work", predicate="cdm:work_contributed_to_by_agent", object="?agent")]
		first_pattern.add_triples(triples=first_pattern_triples)
		second_pattern = SPARQLGraphPattern(union=True)
		second_pattern_triples = [Triple(subject="?work", predicate="cdm:work_created_by_agent", object="?agent")]
		second_pattern.add_triples(triples=second_pattern_triples)
		third_pattern = SPARQLGraphPattern(union=True)
		third_pattern_triples = [Triple(subject="?work", predicate="cdm:work_authored_by_agent", object="?agent")]
		third_pattern.add_triples(triples=third_pattern_triples)
		# graph_gagent = SPARQLGraphPattern(name="gagent")
		self.graph_gagent.add_nested_graph_pattern(graph_pattern=first_pattern)
		self.graph_gagent.add_nested_graph_pattern(graph_pattern=second_pattern)
		self.graph_gagent.add_nested_graph_pattern(graph_pattern=third_pattern)
	
	
	def __add_graph_gaa_triples(self):
		graph_gaa_triples = [Triple(subject="?agent", predicate="skos:prefLabel", object="?agentName")]
		self.graph_gaa.add_triples(triples=graph_gaa_triples)
	
	
	def __add_graph_gaa_language_filter(self):
		graph_gaa_language_filter = Filter(expression='lang(?agentName)="en"', )
		self.graph_gaa.add_filter(filter=graph_gaa_language_filter)
	
	
	def __add_graph_gm_triples(self):
		graph_gm_triples = [Triple(subject="?manif", predicate="cdm:manifestation_manifests_expression", object="?exp"),
		                    Triple(subject="?manif", predicate="cdm:manifestation_type", object="?mtype"), ]
		self.graph_gm.add_triples(triples=graph_gm_triples)
	
	
	def __add_graph_gm_mtype_filter(self):
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
	
	
	def __build_graph_ga(self):
		self.__add_graph_ga_triples()
		self.__add_graph_ga_language_filter()
	
	
	def __build_graph_g(self, earliest_pub_date, subjects):
		self.__add_graph_g_triples()
		self.__add_graph_g_date_filter(earliest_pub_date)
		self.__add_graph_g_res_type_filter()
		self.__add_graph_g_eurovoc_subjects_filter(subjects)
		self.__build_graph_ga()
		self.graph_g.add_nested_graph_pattern(graph_pattern=self.graph_ga)
	
	
	def __build_graph_lgc(self):
		self.__add_graph_lgc_triples()
	
	
	def __build_graph_ge(self):
		self.__add_graph_ge_triples()
		self.__add_graph_ge_language_filter()
		self.__add_graph_ge_lang_identifier_filter()
		self.__build_graph_lgc()
		self.graph_ge.add_nested_graph_pattern(graph_pattern=self.graph_lgc)
	
	
	def __build_graph_gagent(self):
		self.__add_graph_gagent_triples()
	
	
	def __build_graph_gaa(self):
		self.__add_graph_gaa_triples()
		self.__add_graph_gaa_language_filter()
	
	
	def __build_graph_gm(self):
		self.__add_graph_gm_triples()
		self.__add_graph_gm_mtype_filter()
	
	
	def __build_where_graph(self, earliest_pub_date, subjects):
		self.__build_graph_g(earliest_pub_date, subjects)
		self.__build_graph_ge()
		self.__build_graph_gagent()
		self.__build_graph_gaa()
		self.__build_graph_gm()
		
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_g)
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_ge)
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_gagent)
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_gaa)
		self.where_graph.add_nested_graph_pattern(graph_pattern=self.graph_gm)
	
	
	def __build_select_query(self, distinct, limit, order_by, earliest_pub_date, subjects):
		self.__init_select_query(distinct, limit, order_by)
		self.__build_where_graph(earliest_pub_date, subjects)
		self.select_query.set_where_pattern(self.where_graph)
	
	
	# def build_select_query(self, distinct, limit, order_by, earliest_pub_date, subjects):
	# 	self.__build_select_query(distinct, limit, order_by, earliest_pub_date, subjects)
	
	
	def build_query(self, distinct=True, limit=10, order_by="desc", earliest_pub_date="2014-01-01", subjects=None,
	                indent_depth=0):
		self.__distinct = distinct
		self.__limit = limit
		self.__order_by = order_by
		if self.__earliest_pub_date is None:
			self.__earliest_pub_date = earliest_pub_date
		if self.__subjects is None:
			self.__subjects = subjects
		# self.build_select_query(distinct, limit, order_by, earliest_pub_date, subjects)
		self.__build_select_query(distinct, limit, order_by, earliest_pub_date, subjects)
		self.__query_str = self.select_query.get_text(indentation_depth=indent_depth)
	
	
	@property
	def query_str(self):
		if self.__query_str is None:
			self.build_query()
		return self.__query_str
	
	
	def update_query_settings(self, distinct=None, limit=None, order_by=None,
	                          earliest_pub_date=None, subjects=None, indent_depth=None):
		if distinct is not None:
			self.__distinct = distinct
			self.__select_query.distinct = distinct
		if limit is not None:
			self.__limit = limit
			self.__select_query.limit = limit
		if order_by is not None:
			self.__order_by = order_by
			self.__select_query.order_by = order_by
		################
		if earliest_pub_date is not None:
			graph_g_date_filter = [f for f in self.graph_g.filters if "date" in f.get_text()][0]
			graph_g_date_filter_idx = self.graph_g.filters.index(graph_g_date_filter)
			# self.graph_g.filters[graph_g_date_filter_idx] = Filter(expression=f"?date > '{earliest_pub_date}'^^xsd:date")
			self.graph_g.filters.pop(graph_g_date_filter_idx)
			self.__add_graph_g_date_filter(earliest_pub_date)
			self.__earliest_pub_date = earliest_pub_date
		################
		if subjects is not None:
			graph_g_subjects_filter = [f for f in self.graph_g.filters if "subject" in f.get_text()][0]
			graph_g_subjects_filter_idx = self.graph_g.filters.index(graph_g_subjects_filter)
			self.graph_g.filters.pop(graph_g_subjects_filter_idx)
			self.__add_graph_g_eurovoc_subjects_filter(subjects)
			self.__subjects = subjects
		################
		self.__query_str = self.select_query.get_text(indentation_depth=indent_depth)


if __name__ == "__main__":
	from utils import get_sparql_query_results
	from pprint import pprint
	
	
	distinct_opt = True
	res_limit_opt = 10
	order_by_opt = "desc"
	earliest_pub_date_opt = "2014-01-01"
	# subjects_opt = None
	subjects_opt = ["regulation of investments"]
	eurlex_sparql_query_builder = EURLexSPARQLQueryConstructor(distinct=distinct_opt, limit=res_limit_opt)
	eurlex_sparql_query_builder.build_query(distinct=True, limit=res_limit_opt, order_by=order_by_opt,
	                                        earliest_pub_date=earliest_pub_date_opt, subjects=subjects_opt,
	                                        indent_depth=0)
	
	query1 = eurlex_sparql_query_builder.query_str
	results1 = get_sparql_query_results(query1)
	data1 = results1["results"]["bindings"]
	df1 = utils.convert_sparql_output_to_df(results1)
	
	distinct_opt2 = True
	res_limit_opt2 = 50
	order_by_opt2 = "desc"
	earliest_pub_date_opt2 = "2018-01-01"
	# subjects_opt2 = ["investment promotion"]
	subjects_opt2 = None
	eurlex_sparql_query_builder.update_query_settings(distinct=distinct_opt2, limit=res_limit_opt2, order_by=order_by_opt2,
	                                                  earliest_pub_date=earliest_pub_date_opt2,
	                                                  subjects=subjects_opt2, indent_depth=0)
	
	query2 = eurlex_sparql_query_builder.query_str
	results2 = get_sparql_query_results(query2)
	data2 = results2["results"]["bindings"]
	df2 = utils.convert_sparql_output_to_df(results2)
	
	print(query2)

# eurlex_sparql_query_builder.build(subjects=None)
# eurlex_sparql_query_builder.init_select_query()
# eurlex_sparql_query_builder.build(subjects=None, earliest_publication_date="2020-01-01", res_limit=res_limit)
# selected_subjects = ["selling price", "clearing agreement",
# 					 "international payment", "regulation of investments",
# 					 "investment policy", "private investment", "investment promotion",]
# eurlex_sparql_query_builder.build(subjects=selected_subjects)
# Print the graph pattern
# query = eurlex_sparql_query_builder.create_query_text(indent_depth=0)
# print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print(f"\nselect_query:\n{query}")
# qq = query.replace(f"LIMIT {res_limit}", f"ORDER BY DESC(?date)\nLIMIT {res_limit}")

# from utils import get_sparql_query_results
# import pprint


# results = get_sparql_query_results(qq)
# results = get_sparql_query_results(query)
# pprint.pprint(results)

# res = results["results"]["bindings"]
