import os
import json
import pandas as pd
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON, POST


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
            # outfile.write("%s\n" % file_name)

        # Last line not followed by newline
        for file_name in list[-1]:
            outfile.write(file_name)


def get_sparql_query_results(sparql_query):
    """
    Send the given sparql_query to the EU Sparql endpoint
    and retrieve and return the results in JSON format.
    :param sparql_query: str
    :return: json dict
    """
    endpoint = "http://publications.europa.eu/webapi/rdf/sparql" # 2020-06-12 THIS
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sparql_query)
    sparql.setMethod(POST)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

