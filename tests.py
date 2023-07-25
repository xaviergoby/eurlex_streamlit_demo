
if __name__ == "__main__":
	import json
	import src_utils
	import data_src
	# from data_src import DataSrc
	
	eurlex_src = data_src.DataSrc(sparql_query_name="financial_domain_eurlex_sparql_query_non_distinct_grouping")
	query = eurlex_src.query_str
	# src_utils.gen_sparql_query_eurovocs_mapping(query, eurovoc_json_mapping_file_name="eurovoc_codes_and_labels_test")
	with open("eurovoc_codes_and_labels.json", 'r') as eurovoc_mapping_json:
		eurovocs_mapping = eurovoc_mapping_json.read()
	
	# parse file
	fin_domain_subjects_eurovoc_labels = list(json.loads(eurovocs_mapping).values())
	
	fin_domain_subjects_eurovoc_labels = list(json.loads(eurovocs_mapping).values())
	fin_domain_subjects_eurovoc_labels_formatted = "\n"
	for eurovoc_label in fin_domain_subjects_eurovoc_labels:
		fin_domain_subjects_eurovoc_labels_formatted += f"- {eurovoc_label}\n"
		
	print(f"fin_domain_subjects_eurovoc_labels_formatted: {fin_domain_subjects_eurovoc_labels_formatted}")
