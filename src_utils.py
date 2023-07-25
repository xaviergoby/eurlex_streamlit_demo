from SPARQLWrapper import SPARQLWrapper, JSON, POST
import xmltodict, json
import requests
import json
import re


def to_json_output_file(file_name, data):
	"""
	Print the given data input to
	a file in json format with the given file_name.

	:param file_name: str
	:param data: structured data
	:return: text file
	"""
	with open(file_name, 'w') as outfile:
		# print('JSON_DUMPS:', json.dumps(data))
		json.dump(data, outfile, indent=4)


def text_to_str(file_path):
	"""
	Read lines of file in given path
	and return string of the text.
	:param file_path: file path str
	:return: text str
	"""
	with open(file_path, 'r') as file:
		return file.read()


def print_list_to_file(outfile_name, list):
	"""
	Create a file with the given outfile_name
	and print each element in the given list
	on a new line of the new file.
	Last line not followed by newline.

	:param outfile_name: str
	:param list: list
	:return: None
	"""
	with open(outfile_name, 'w') as outfile:
		for elt in list[:-1]:
			outfile.write('{name}{newline}'.format(name=elt, newline='\n'))
		for file_name in list[-1]:
			outfile.write(file_name)


def get_sparql_query_results(sparql_query):
	"""
	Send the given sparql_query to the EU Sparql endpoint
	and retrieve and return the results in JSON format.
	:param sparql_query: str
	:return: json dict
	"""
	endpoint = "http://publications.europa.eu/webapi/rdf/sparql"  # 2020-06-12 THIS
	sparql = SPARQLWrapper(endpoint)
	sparql.setQuery(sparql_query)
	sparql.setMethod(POST)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results


def eurovoc_xmlrdf_response_2_label(xmlrdf_response):
	o = xmltodict.parse(xmlrdf_response.text)
	j = json.dumps(o)
	labels = [i["skos:prefLabel"] for i in json.loads(j)["rdf:RDF"]['rdf:Description'] if "skos:prefLabel" in list(i.keys())][0]
	# lang_label =
	for label in labels:
		if "@xml:lang" in list(label.keys()) and label["@xml:lang"] == "en":
			return re.sub('[^a-zA-Z]+ ', '', label["#text"])


def convert_eurovoc_code_2_label_via_get_req(eurovoc_code):
	headers = {"charset": "utf-8", "Content-Type": "application/json"}
	# url = f"https://publications.europa.eu/resource/authority/eurovoc/{label_id}"
	url = f"http://eurovoc.europa.eu/{eurovoc_code}"
	res = requests.get(url, headers=headers)
	label_eurovoc_name = eurovoc_xmlrdf_response_2_label(res).lower()
	return label_eurovoc_name


def gen_sparql_query_eurovocs_mapping(sparql_query_str, eurovoc_json_mapping_file_name="eurovoc_codes_and_labels"):
	query_str_graph_ga_init_strs = "graph ?ga {"
	query_str_graph_ga_init_1st_idx = sparql_query_str.index(query_str_graph_ga_init_strs)
	query_str_graph_ga_end_strs = """	}
	graph ?ge {"""
	query_str_graph_ga_end_1st_idx = sparql_query_str.index(query_str_graph_ga_end_strs) + len(
			query_str_graph_ga_end_strs[:query_str_graph_ga_end_strs.index("}")]) + 1
	query_str_graph_ga_section = sparql_query_str[query_str_graph_ga_init_1st_idx:query_str_graph_ga_end_1st_idx]
	query_str_subject_filter_init_1st_idx = query_str_graph_ga_section.index("FILTER( ?subject = ")
	query_str_subject_filter = query_str_graph_ga_section[query_str_subject_filter_init_1st_idx:]
	eurovoc_urls = re.findall(r'<([^<>]*)>', query_str_subject_filter)
	eurovoc_codes = [eurovoc_url.split("/")[-1] for eurovoc_url in eurovoc_urls]
	eurovoc_labels = [convert_eurovoc_code_2_label_via_get_req(eurovoc_code) for eurovoc_code in eurovoc_codes]
	eurovocs_dict = dict(zip(eurovoc_codes, eurovoc_labels))
	with open(f"{eurovoc_json_mapping_file_name}.json", "w") as json_file:
		json.dump(eurovocs_dict, json_file, indent=4)
