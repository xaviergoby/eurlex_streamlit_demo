# from SPARQLWrapper import SPARQLWrapper, JSON, POST
import SPARQLWrapper
import xmltodict
import requests
import json
import re
import pandas as pd
import os
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import rdflib
import settings
from typing import Any


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


def print_data_to_file(outfile_name: str, data: list) -> None:
	"""
	Create a file with the given outfile_name and print each element
	in the given list on a new line of the new file. Last line not
	followed by newline.
	:param outfile_name: <str>
	:param data: <list>
	:return: <None>
	"""
	with open(outfile_name, "w") as output_file_obj:
		for elt in data[:-1]:
			# outfile.write('{name}{newline}'.format(name=elt, newline='\n'))
			output = f"{elt}\n"
			output_file_obj.write(output)
		for file_name in data[-1]:
			output_file_obj.write(file_name)


def get_sparql_query_results(sparql_query_str, sparql_endpoint_url: str = settings.EURLEX_SPARQL_ENDPOINT_URL):
	"""
	Send the given sparql_query to the EU Sparql endpoint
	and retrieve and return the results in JSON format.
	:param sparql_query_str: <str>
	:param sparql_endpoint_url: <str> Is https://publications.europa.eu/webapi/rdf/sparql by default.
	:return: json dict
	"""
	# sparql = SPARQLWrapper(endpoint)
	sparql = SPARQLWrapper.SPARQLWrapper(sparql_endpoint_url)
	sparql.setQuery(query=sparql_query_str)
	# sparql.setMethod(POST)
	sparql.setMethod(method=SPARQLWrapper.POST)
	# sparql.setReturnFormat(JSON)
	sparql.setReturnFormat(format=SPARQLWrapper.JSON)
	# results = sparql.query().convert()
	# Execute/Run the query and get the results (a <SPARQLWrapper.QueryResult> instance
	query_result = sparql.query()
	# Convert the returned query results as encoding depending on the return format prev set via setReturnFormat()
	# * in the case of :data:`JSON`, a json conversion will return a dictionary
	converted_query_result = query_result.convert()
	# print(f"~~~~~~~~~~~~~~~~ print(query) ~~~~~~~~~~~~~~~~\n")
	# print(query)
	# print(f"~~~~~~~~~~~~~~~~ print(query.geturl()) ~~~~~~~~~~~~~~~~\n")
	# print(query.geturl())
	# print(f"~~~~~~~~~~~~~~~~ print(query.info()) ~~~~~~~~~~~~~~~~\n")
	# print(query.info())
	# print(f"~~~~~~~~~~~~~~~~ print(query.requestedFormat) ~~~~~~~~~~~~~~~~\n")
	# print(query.requestedFormat)
	# print(f"~~~~~~~~~~~~~~~~ print(query._get_responseFormat()) ~~~~~~~~~~~~~~~~\n")
	# print(query._get_responseFormat())
	# print(f"~~~~~~~~~~~~~~~~ (sparql.returnFormat) ~~~~~~~~~~~~~~~~\n")
	# print(sparql.returnFormat)
	return converted_query_result


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


def convert_eurovoc_code_2_label_via_json_mapping(eurovoc_codes: list[str] | list[int] | str | int,
                                                  eurovoc_json_mapping_file_name: str = "eurovoc_codes_and_labels"):
	mappings_json_file_abs_path = os.path.join(settings.MAPPINGS_DIR, f"{eurovoc_json_mapping_file_name}.json")
	
	with open(mappings_json_file_abs_path, 'r') as eurovoc_mapping_json_file_obj:
		eurovocs_mapping_dict = eurovoc_mapping_json_file_obj.read()
	
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


def load_json_as_dict(json_file_path):
	with open(f"{json_file_path}.json", "r") as json_file_obj:
		json_file_content_str = json_file_obj.read()
	json_file_content_dict = json.loads(json_file_content_str)
	return json_file_content_dict


def simplify_iri(iri: str, sparql_prefix_mapping_json_name="eurlex_sparql_prefix_namespace_mapping") -> str:
	"""Simplify prefixes in an IRI.

	:param iri: <str> IRI to simplify.
	:return: <str> Simplified version where all prefixes are replaced by their shortcuts.
	Examples
	--------
	>>> simplify_iri("http://publications.europa.eu/ontology/cdm#test")
	'cdm:test'
	>>> simplify_iri("cdm:test")
	'cdm:test'
	"""
	prefixes_mapping = load_json_as_dict(sparql_prefix_mapping_json_name)
	for prefix_label, namespace_url in prefixes_mapping.items():
		if iri.startswith(namespace_url):
			formatted_iri = f"{prefix_label}:{iri[len(namespace_url):]}"
			return formatted_iri
	return iri


def convert_sparql_output_to_df(sparql_results: dict) -> pd.DataFrame:
	"""Convert SPARQL output to a DataFrame.

	:param sparql_results: <dict> A dictionary containing the SPARQL results.
	:return: <pd.DataFrame> The DataFrame representation of the SPARQL results.
	Examples
	--------
	>>> convert_sparql_output_to_df({'results': {'bindings': [{'subject': {'value': 'cdm:test'}}]}}).to_dict()
	{'subject': {0: 'cdm:test'}}
	"""
	bindings = [item for item in sparql_results["results"]["bindings"]]
	print(f"~~~~~~~~~~~~~~~~~~~ bindings: {bindings} ~~~~~~~~~~~~~~~~~~~")
	items = [
			{key: simplify_iri(item[key]["value"]) for key in item.keys()}
			for item in sparql_results["results"]["bindings"]
			]
	df = pd.DataFrame(items)
	return df


def get_celex_id_as_df(celex_id: str, base_url="http://publications.europa.eu/resource/") -> pd.DataFrame:
	""" Get CELEX data delivered in a DataFrame.

	:param celex_id: <str> The CELEX ID to get the data for.
	:return: <pd.DataFrame> A DataFrame containing the results.
	"""
	graph = rdflib.Graph()
	url_for_graph_2_parse = f"{base_url}celex/{str(celex_id)}?language=eng"
	results = graph.parse(url_for_graph_2_parse)
	items = [{key: simplify_iri(item[key]) for key in range(len(item))} for item in results]
	df = pd.DataFrame(items)
	df.columns = ["s", "o", "p"]
	return df


if __name__ == "__main__":
	# url = f"https://publications.europa.eu/resource/authority/eurovoc/{label_id}"
	# url = f"http://eurovoc.europa.eu/{eurovoc_code}"
	
	with open("mappings/eurovoc_codes_and_labels.json", 'r') as eurovoc_mapping_json:
		eurovocs_mapping = eurovoc_mapping_json.read()
	
	fin_domain_subjects_eurovoc_ids = list(json.loads(eurovocs_mapping).keys())
	
	convert_eurovoc_code_2_label_via_get_req("100142")
