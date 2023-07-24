import time
import data_src
# from data_src import DataSrc
# from sparql_query_builder import SparqlQueryBuilder
from src_utils import get_sparql_query_results
import streamlit as st



# sparl_query_builder = SparqlQueryBuilder()
# query = sparl_query_builder.build_query()

# eurlex_src = DataSrc(base_sparql_query_name="eurlex_base_financial_domain_sparql_query")
# eurlex_src = data_src.DataSrc(sparql_query_name="financial_domain_sparql_2019-01-07_V2")
# eurlex_src = data_src.DataSrc(sparql_query_name="financial_domain_eurlex_sparql_query")
eurlex_src = data_src.DataSrc(sparql_query_name="financial_domain_eurlex_sparql_query_non_distinct_grouping")
query = eurlex_src.query_str
# results = get_sparql_query_results(query)

updated_query = ''

# st.title("EurLex Financial Domain Publications Retrieval Demo")
# title_alignment = "<style> #the-title { text-align: center}EurLex Financial Domain Publications Retrieval Demo</style>"
# st.markdown(title_alignment, unsafe_allow_html=True)

# style = "<style>h1 {text-align: center;}</style>"
# st.markdown(style, unsafe_allow_html=True)
# st.header("EurLex Financial Domain Publications Retrieval Demo")

# with st.sidebar:
# 	language_opt = st.sidebar.selectbox("Publication language", options=["EN", "NL"])
# 	ordering = st.sidebar.selectbox("Publications ordering", options=["Descending", "Ascending"])
# 	if ordering == "ASC" and "DESC(?date)" in updated_query:
# 		updated_query = updated_query.replace("DESC(?date)", "ASC(?date)")
# 	elif ordering == "DESC" and "ASC(?date)" in updated_query:
# 		updated_query = updated_query.replace("ASC(?date)", "DESC(?date)")
	
# language_opt2 = st.sidebar.date_input("Please enter earliest date of publications (YYYY-MM-DD)").strftime('%Y-%m-%d')
# subject_filer = st.sidebar.selectbox("Please enter earliest date of publications (YYYY-MM-DD)").strftime('%Y-%m-%d')

st.markdown("<h1 style='text-align: center; color: white;'>EurLex Financial Domain Publications Retrieval Demo</h1>", unsafe_allow_html=True)
# st.header("SPARQL Query Results")
# st.columns(3)[1].header("SPARQL Query Results")

# descriptor_term = st.text_input("Sparql queries file name")
# FILTER( ?date = "2014-01-01"^^xsd:date)

# st.write("#")

# st.markdown("<h2 style='text-align: center; color: white;'>Options</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='color: white;'>Options</h2>", unsafe_allow_html=True)

input_row1_col1, input_row1_col2 = st.columns(2)
input_row2_col1, input_row2_col2 = st.columns(2)


# init_pub_date = st.text_input("Please enter a starting date for publications desired (YYYY-MM-DD)")
# init_pub_date = st.date_input("Please enter a starting date for publications desired (YYYY-MM-DD)").strftime('%Y-%m-%d')
init_pub_date = input_row1_col1.date_input("Please enter earliest date of publications (YYYY-MM-DD)").strftime('%Y-%m-%d')
# print(f"init_pub_date: {init_pub_date}")

# st.write(f"init_pub_date: {init_pub_date}")

updated_query = query.replace('FILTER( ?date > "2014-01-01"^^xsd:date)', f'FILTER( ?date > "{init_pub_date}"^^xsd:date)')

while updated_query == '':
	time.sleep(1)
	
res_limit = None

# res_limit = st.text_input("Please enter a limit number of results desired")
# res_limit = st.slider("Results to return (1-25)", 1, 25)
max_res_limit = 50
res_limit = input_row1_col2.slider(f"Results to return (1-{max_res_limit})", 1, max_res_limit)

updated_query = updated_query.replace('LIMIT 10', f'LIMIT {res_limit}')

while res_limit is None:
	time.sleep(1)
	
ordering = input_row2_col1.selectbox("Publications ordering", options=["Descending", "Ascending"])
if ordering == "Ascending" and "DESC(?date)" in updated_query:
	updated_query = updated_query.replace("DESC(?date)", "ASC(?date)")
elif ordering == "Descending" and "ASC(?date)" in updated_query:
	updated_query = updated_query.replace("ASC(?date)", "DESC(?date)")
	
language_opt = input_row2_col2.selectbox("Publications language", options=["EN", "NL"])
# updated_query = updated_query.


# st.divider()

# st.markdown("<h2 style='text-align: center; color: white;'>SPARQL Query Results</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='color: white;'>SPARQL Query Results</h2>", unsafe_allow_html=True)

# st.write("#")
# st.write("#")

st.divider()




results = get_sparql_query_results(updated_query)
for i, res in enumerate(results["results"]["bindings"], start=1):
	print(f"\n~~~~~~~~~~~ i={i} => len(res): {len(res)} ~~~~~~~~~~~")
	print(f"~~~~~~~~~~~ i={i} => len(res['celexIds']['value'].split('|')): {len(res['celexIds']['value'].split('|'))} ~~~~~~~~~~~")
	# print(f"\n~~~~~~~~~~~ doc_url KEYS: {res.keys()} ~~~~~~~~~~~")
	# print(f"~~~~~~~~~~~ doc_url VALUES: {res.values()} ~~~~~~~~~~~")
	doc_date = res["date"]["value"]
	doc_title = res["workTitles"]["value"]
	# doc_title = res["workTitles"]["value"].split("|")
	doc_celex_id = res["celexIds"]["value"]
	doc_subjects = res["subjects"]["value"]
	# doc_subjects = res["subjectLabel"]["value"]
	doc_url = res["cellarURIs"]["value"]
	doc_authors = res["authors"]["value"]
	# doc_mtypes = res["mtypes"]["value"]
	doc_mtypes = res["mtype"]["value"]
	# doc_ids = res["workIds"]["value"]
	# st.write(f"**Document # {i}:**")
	# st.write(f"Date: {doc_date}")
	# st.write(f"CELEX: {doc_celex_id}")
	# col1, col2 = st.columns(2)
	# col1, col2, col3 = st.columns(3)
	# col1.write(f"**Document # {i}:**")
	# col2.write(f"Date: {doc_date}")
	# col3.write(f"CELEX: {doc_celex_id}")
	# st.write(f"Title: {doc_title}")
	# st.write(f"Subjects: {doc_subjects.replace('|', ', ')}")
	# st.write(f"URL: {doc_url}")
	if len(doc_celex_id) > 11:
		col1, col2, col3 = st.columns((1,1,2))
	else:
		col1, col2, col3 = st.columns(3)
	col1.write(f"**Document # {i}:**")
	col2.write(f"Date: {doc_date}")
	col3.write(f"CELEX: {doc_celex_id}")
	st.write(f"Title:\n<a href='{doc_url}' id='my-link'>{doc_title}</a>", unsafe_allow_html=True)
	# st.write(f"Title:\n<h3 style='color: white;' href='{doc_url}' id='my-link'>{doc_title}</h3>", unsafe_allow_html=True)
	# st.markdown("<h2 style='color: white;'>SPARQL Query Results</h2>", unsafe_allow_html=True)
	# st.write(f"Authors: {doc_authors.replace('|', ', ')}")
	# authors_list = '-'.join(doc_authors.split('|'))
	authors_list_formatted = "\n"
	for author in doc_authors.split('|'):
		authors_list_formatted += f"- {author}\n"
	st.markdown(f"""
	Authors:
	{authors_list_formatted}
	""")
	# st.write(f"Subjects: {doc_subjects.replace('|', ', ')}")
	subjects_list_formatted = "\n"
	for subject in list(set(doc_subjects.split('|'))):
		subjects_list_formatted += f"- {subject}\n"
	st.markdown(f"""
		Subjects:
		{subjects_list_formatted}
		""")
	# st.write(f"IDs: {doc_ids}")
	# print(f"||||||||||| IDs: {doc_ids}")
	# st.write(f"Document types: {doc_mtypes.replace('|', ', ')}")
	st.write("---")

