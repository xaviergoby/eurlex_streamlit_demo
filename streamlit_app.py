import json
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

# sidebar_info = st.sidebar.markdown("<h2 style='color: white;'>Sidebar Info</h2>", unsafe_allow_html=True)

# st.sidebar.markdown("""
#         <style>
#         .block-container {
#                     padding-top: 1rem;
#                     padding-bottom: 0rem;
#                     padding-left: 5rem;
#                     padding-right: 5rem;
#                     }
#         </style>
#         """, unsafe_allow_html=True)

# h1 {
#     font-family: "Source Sans Pro", sans-serif;
#     font-weight: 700;
#     color: rgb(250, 250, 250);
#     padding: 2rem 0px 1rem;
#     margin: 0px;
#     line-height: 1.2;
# }

st.markdown("""
  <style>
    block-container css-1y4p8pa e1g8pov64 {
      padding: 2rem 1px 1.5rem;
    }
    .css-1y4p8pa {
    width: 100%;
    padding: 1.5rem 1rem 10rem;
    max-width: 46rem;
}
h1 {
    font-size: calc(1.8rem + 2vw);
}
  </style>
""", unsafe_allow_html=True)
st.markdown("""
  <style>
    .css-1544g2n {
      padding: 2rem 1rem 1.5rem;
    }
  </style>
""", unsafe_allow_html=True)

# .css-1544g2n {
#     padding: 6rem 1rem 1.5rem;
# }

# sidebar_info_project_name = st.sidebar.markdown("<h1 style='text-align: center; color: white;'><b><font size='+20'><em>COEUS</em></font></b></h1>", unsafe_allow_html=True)
sidebar_info_project_name = st.sidebar.markdown("<h2 style='text-align: center; color: white; padding-top: -50px;'><b><font size='+20'><em>COEUS</em></font></b></h2>", unsafe_allow_html=True)
# st.sidebar.markdown("<h1><b><font size='+20'><em>COEUS</em></font></b></h1>", unsafe_allow_html=True)

proj_name_caption_wiki_url = "https://en.wikipedia.org/wiki/Coeus"
proj_name_caption_wiki_label = "Coeus - Wikipedia"
sidebar_info_proj_name_caption = st.sidebar.markdown("<h5 style='text-align: center; color: white;'>In Greek mythology, "
													 "Coeus (Ancient Greek: Κοῖος), Koios, meaning 'query, questioning' or "
													 "'intelligence', also called Polus, was one of the Titans, one of the "
													 f"three groups of children born to Uranus (Sky) and Gaia (Earth).<a href='{proj_name_caption_wiki_url}' id='my-link'>{proj_name_caption_wiki_label}</a></h5>", unsafe_allow_html=True)

st.sidebar.divider()
sidebar_info_project_title = st.sidebar.markdown('<h4 style="text-align: center; color: white;"><font size="+6">EurLex Financial\n'
												 'Domain Publications\nQuerying & Retrieval\n<em>"Streamlitnined"</em></font></h4>', unsafe_allow_html=True)

st.markdown("""
  <style>
h4 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(250, 250, 250);
    padding: 0.25rem 0px 0.5rem;
    margin: 0px;
    line-height: 1.2;
}
  </style>
""", unsafe_allow_html=True)
# st.sidebar.divider()

sidebar_info_gen_desc_header = st.sidebar.markdown("<h2 style='color: white;'>General Description</h2>", unsafe_allow_html=True)

with open("eurovoc_codes_and_labels.json", 'r') as eurovoc_mapping_json:
    eurovocs_mapping = eurovoc_mapping_json.read()

publications_of_the_eu_office_url = "https://op.europa.eu/en/home"
eur_lex_url = "https://eur-lex.europa.eu/homepage.html"
eurovocs_url = "https://op.europa.eu/en/web/eu-vocabularies"
sidebar_info_gen_desc = st.sidebar.markdown("<p>This applications purpose is to facilitate the querying & acquisition of financial related"
											f"official publications from the <a href='{publications_of_the_eu_office_url}' id='my-link'>Publications Office of the EU</a>.<br>See the list of financial subjects below"
											f"(i.e. <a href='{eurovocs_url}' id='my-link'>EuroVoc's</a>) defining the financial domain/corpus of knowledge available via the <a href='{eur_lex_url}' id='my-link'>EUR-Lex</a> platform.</p>", unsafe_allow_html=True)

# parse file
fin_domain_subjects_eurovoc_labels = list(json.loads(eurovocs_mapping).values())
fin_domain_subjects_eurovoc_labels_formatted = "\n"
for eurovoc_label in fin_domain_subjects_eurovoc_labels:
	fin_domain_subjects_eurovoc_labels_formatted += f"- {eurovoc_label}\n"
fin_domain_subjects_eurovoc_labels_formatted = f"""
{fin_domain_subjects_eurovoc_labels_formatted}
"""
# st.markdown(f"""
# 	EuroVocs:
# 	{fin_domain_subjects_eurovoc_labels_formatted}
# 	""")
# sidebar_info_eurlex_subjects_toggle = st.sidebar.markdown("<details> <summary>Sidebar Info</summary> BODY CONTENT </details> ", unsafe_allow_html=True)
# sidebar_info_eurlex_subjects_toggle = st.sidebar.markdown(f"<details> <summary>Sidebar Info</summary>{fin_domain_subjects_eurovoc_labels_formatted}</details> ", unsafe_allow_html=True)
# sidebar_info_eurlex_subjects_toggle = st.sidebar.markdown(f"""<details> <summary>EuroVocs:</summary>{fin_domain_subjects_eurovoc_labels_formatted}</details>""",
# 														  unsafe_allow_html=True)
sidebar_info_eurlex_subjects_toggle = st.sidebar.markdown(f"<details> <summary>EuroVocs:</summary>{fin_domain_subjects_eurovoc_labels_formatted}</details>",
														  unsafe_allow_html=True)
# st.sidebar.divider()
sidebar_info_usage_guide_header = st.sidebar.markdown("<h2 style='color: white;'>Usage Guide</h2>", unsafe_allow_html=True)

sidebar_info_usage_guide = st.sidebar.markdown("<p>Intuitive enough I hope</p>", unsafe_allow_html=True)

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
init_pub_date = input_row1_col1.date_input("Earliest date of publications (YYYY-MM-DD)").strftime('%Y-%m-%d')
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
st.divider()
st.markdown("<h2 style='color: white;'>SPARQL Query Results</h2>", unsafe_allow_html=True)

# st.write("#")
# st.write("#")

# st.divider()




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
	# st.write(f"**Document # {i}:**")
	st.markdown(f"<h3 style='color: white;'><b>Document # {i}</b></h3>", unsafe_allow_html=True)
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
	# col1.write(f"**Document # {i}:**")
	col1.write(f"Date: {doc_date}")
	col2.write(f"Format: {doc_mtypes}")
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

