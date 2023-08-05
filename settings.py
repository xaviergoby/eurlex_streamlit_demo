import os

# Proj root % data dirs
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # returns C:\Users\XGOBY\OneDrive\HODL\HODL_Research_Analysis
DATA_DIR = os.path.join(ROOT_DIR, "data")  # C:\Users\XGOBY\OneDrive\HODL\HODL_Research_Analysis\data_sources
# Queries dirs
QUERIES_DIR = os.path.join(ROOT_DIR, "queries")
SPARQL_QUERIES_DIR = os.path.join(QUERIES_DIR, "sparql_queries")
SPARQL_QUERY_RESULTS_DIR = os.path.join(QUERIES_DIR, "sparql_query_results")
# Eurovoc related settings & configs
EUROVOC_MODULE_DIR = os.path.join(ROOT_DIR, "eurovoc_module")
EUROVOC_CODES_JSON_FILE_PATH = os.path.join(EUROVOC_MODULE_DIR, "eurovoc_codes.json")
EUROVOC_DESCRIPTORS_JSON_FILE_PATH = os.path.join(EUROVOC_MODULE_DIR, "eurovoc_descriptors.json")
# Mappings dir
MAPPINGS_DIR = os.path.join(ROOT_DIR, "mappings")
# EU Sparql endpoint
EURLEX_SPARQL_ENDPOINT_URL = "https://publications.europa.eu/webapi/rdf/sparql"

if __name__ == "__main__":
	print(f"ROOT_DIR: {ROOT_DIR}")
	
	print(f"\nDATA_DIR: {DATA_DIR}")
	
	print(f"\nQUERIES_DIR: {QUERIES_DIR}")
	print(f"SPARQL_QUERIES_DIR: {SPARQL_QUERIES_DIR}")
	print(f"SPARQL_QUERY_RESULTS_DIR: {SPARQL_QUERY_RESULTS_DIR}")
	
	print(f"\nEUROVOC_MODULE_DIR: {EUROVOC_MODULE_DIR}")
	print(f"EUROVOC_CODES_JSON_FILE_PATH: {EUROVOC_CODES_JSON_FILE_PATH}")
	print(f"EUROVOC_DESCRIPTORS_JSON_FILE_PATH: {EUROVOC_DESCRIPTORS_JSON_FILE_PATH}")
	
	print(f"\nEURLEX_SPARQL_ENDPOINT_URL: {EURLEX_SPARQL_ENDPOINT_URL}")
