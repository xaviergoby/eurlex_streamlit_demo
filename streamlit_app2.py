import json
import time
from utils import get_sparql_query_results
import streamlit as st
import data_src
from eurlex_sparql_query_constructor import EURLexSPARQLQueryBuilder
from eurlex_sparql_query_constructorV3 import EURLexSPARQLQueryConstructor


max_res_limit = 50

# eurlex_src = data_src.DataSrc(sparql_query_name="financial_domain_eurlex_sparql_query_non_distinct_grouping")
# query = eurlex_src.query_str
# eurlex_src = EURLexSPARQLQueryBuilder(distinct=True)
# query = eurlex_src.create_query()
distinct_opt = True
res_limit_opt = 10
order_by_opt = "desc"
earliest_pub_date_opt = "2014-01-01"
subjects_opt = None
eurlex_src = EURLexSPARQLQueryConstructor(distinct=distinct_opt, limit=res_limit_opt)
eurlex_src.build_query(distinct=True, limit=res_limit_opt, order_by=order_by_opt,
                       earliest_pub_date=earliest_pub_date_opt, subjects=subjects_opt,
                       indent_depth=0)
query = eurlex_src.query_str

updated_query = ''

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

sidebar_info_project_name = st.sidebar.markdown(
	"<h2 style='text-align: center; color: white; padding-top: -50px;'><b><font size='+20'><em>COEUS</em></font></b></h2>", unsafe_allow_html=True)

proj_name_caption_wiki_url = "https://en.wikipedia.org/wiki/Coeus"
proj_name_caption_wiki_label = "Coeus - Wikipedia"
sidebar_info_proj_name_caption = st.sidebar.markdown("<h5 style='text-align: center; color: white;'>In Greek mythology, "
                                                     "Coeus (Ancient Greek: Κοῖος), Koios, meaning 'query, questioning' or "
                                                     "'intelligence', also called Polus, was one of the Titans, one of the "
                                                     f"three groups of children born to Uranus (Sky) and Gaia (Earth).<a href='"
                                                     f"{proj_name_caption_wiki_url}' id='my-link'>{proj_name_caption_wiki_label}</a></h5>",
                                                     unsafe_allow_html=True)

st.sidebar.divider()
sidebar_info_project_title = st.sidebar.markdown('<h4 style="text-align: center; color: white;"><font size="+6">EurLex Financial\n'
                                                 'Domain Publications\nQuerying & Retrieval\n<em>"Streamlitnined"</em></font></h4>',
                                                 unsafe_allow_html=True)

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

st.markdown("""
  <style>
p, ol, ul, dl {
    margin: 4px 1px 0.20rem;a
    padding: 0px;
    font-size: 1rem;
    font-weight: 400;
}
  </style>
""", unsafe_allow_html=True)

sidebar_info_gen_desc_header = st.sidebar.markdown("<h2 style='color: white;'>General Description</h2>", unsafe_allow_html=True)

with open("mappings/eurovoc_codes_and_labels.json", 'r') as eurovoc_mapping_json:
	eurovocs_mapping = eurovoc_mapping_json.read()

publications_of_the_eu_office_url = "https://op.europa.eu/en/home"
eur_lex_url = "https://eur-lex.europa.eu/homepage.html"
eurovocs_url = "https://op.europa.eu/en/web/eu-vocabularies"
sidebar_info_gen_desc = st.sidebar.markdown("<p>This applications purpose is to facilitate the querying & acquisition of financial related"
                                            f"official publications from the <a href='{publications_of_the_eu_office_url}' "
                                            f"id='my-link'>Publications Office of the EU</a>.<br>See the list of financial subjects below"
                                            f"(i.e. <a href='{eurovocs_url}' id='my-link'>EuroVoc's</a>) defining the financial domain/corpus of "
                                            f"knowledge available via the <a href='{eur_lex_url}' id='my-link'>EUR-Lex</a> platform.</p>",
                                            unsafe_allow_html=True)

# parse EuroVoc descriptors/labels & IDs JSON mapping file
fin_domain_subjects_eurovoc_ids = list(json.loads(eurovocs_mapping).keys())

fin_domain_subjects_eurovoc_labels = list(json.loads(eurovocs_mapping).values())
fin_domain_subjects_eurovoc_labels_formatted = "\n"
for eurovoc_label in fin_domain_subjects_eurovoc_labels:
	fin_domain_subjects_eurovoc_labels_formatted += f"- {eurovoc_label}\n"
fin_domain_subjects_eurovoc_labels_formatted = f"""
{fin_domain_subjects_eurovoc_labels_formatted}
"""

st.write("##")

sidebar_info_eurlex_subjects_toggle = st.sidebar.markdown(f"<details> "
                                                          f"<summary><font size='+4'>Financial Subjects (EuroVoc's):</summary>"
                                                          f"{fin_domain_subjects_eurovoc_labels_formatted}</details>",
                                                          unsafe_allow_html=True)
sidebar_info_usage_guide_header = st.sidebar.markdown("<h2 style='color: white;'>Usage Guide</h2>", unsafe_allow_html=True)

# sidebar_info_usage_guide = st.sidebar.markdown("<p>Intuitive enough I hope</p>", unsafe_allow_html=True)
sidebar_info_usage_guide = st.sidebar.markdown("<li>Select the earliest publication date to retrieve results for.</li>"
                                               f"<li>Select the number of results to be retrieved (min of 1 & max of {max_res_limit}.</li>"
                                               f"<li>Select the date-wise ordering of retrieved publication results.</li>"
                                               f"<li>Select the language of publications to be retrieved.</li>", unsafe_allow_html=True)

st.sidebar.divider()

warning_note = st.sidebar.markdown("This project/endeavour is strictly <b>NOT</b> associated with the "
                                   "Publications Office of the European Union, EUR-Lex nor any other entity "
                                   "whatsoever. This is strictly the work of (Alexander) Xavier Goby.")

st.markdown("<h1 style='text-align: center; color: white;'>EurLex Financial Domain Publications Retrieval Demo</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='color: white;'>Options</h2>", unsafe_allow_html=True)

input_row1_col1, input_row1_col2 = st.columns(2)
input_row2_col1, input_row2_col2 = st.columns(2)

init_pub_date = input_row1_col1.date_input("Earliest date of publications (YYYY-MM-DD)").strftime('%Y-%m-%d')

# updated_query = query.replace('FILTER( ?date > "2014-01-01"^^xsd:date)', f'FILTER( ?date > "{init_pub_date}"^^xsd:date)')
# updated_query = eurlex_src.create_query(earliest_publication_date=init_pub_date)

# while updated_query == '':
# 	time.sleep(1)
#
# res_limit = None

res_limit = input_row1_col2.slider(f"Results to return (1-{max_res_limit})", 1, max_res_limit, 10)

# updated_query = updated_query.replace('LIMIT 10', f'LIMIT {res_limit}')
# updated_query = eurlex_src.create_query(earliest_publication_date=init_pub_date, res_limit=res_limit)

# while res_limit is None:
# 	time.sleep(1)

ordering = input_row2_col1.selectbox("Publications ordering", options=["Descending", "Ascending"])
if ordering == "Ascending" and "DESC(?date)" in updated_query:
	order_by_opt = "asc"
# updated_query = updated_query.replace("DESC(?date)", "ASC(?date)")
# updated_query = eurlex_src.create_query(earliest_publication_date=init_pub_date, order_by="asc", res_limit=res_limit)
elif ordering == "Descending" and "ASC(?date)" in updated_query:
	order_by_opt = "desc"
# updated_query = updated_query.replace("ASC(?date)", "DESC(?date)")
# updated_query = eurlex_src.create_query(earliest_publication_date=init_pub_date, order_by="desc", res_limit=res_limit)

language_opt = input_row2_col2.selectbox("Publications language", options=["EN", "NL"])

st.divider()

st.markdown("<h2 style='color: white;'>SPARQL Query Results</h2>", unsafe_allow_html=True)
st.write("##")

# distinct_opt2 = True
# res_limit_opt2 = 50
# order_by_opt2 = "desc"
# earliest_pub_date_opt2 = "2018-01-01"
# subjects_opt2 = ["investment promotion"]
subjects_opt2 = None
eurlex_src.update_query_settings(distinct=distinct_opt, limit=res_limit, order_by=order_by_opt,
                                 earliest_pub_date=init_pub_date, subjects=subjects_opt2, indent_depth=0)
updated_query = eurlex_src.query_str

if updated_query == '':
	results = get_sparql_query_results(query)
else:
	results = get_sparql_query_results(updated_query)

for i, res in enumerate(results["results"]["bindings"], start=1):
	doc_date = res["date"]["value"]
	doc_title = res["workTitles"]["value"]
	doc_celex_id = res["celexIds"]["value"]
	doc_subjects = res["subjects"]["value"]
	doc_url = res["cellarURIs"]["value"]
	doc_authors = res["authors"]["value"]
	doc_mtypes = res["mtype"]["value"]
	st.markdown(f"<h3 style='color: white;'><b>Document # {i}</b></h3>", unsafe_allow_html=True)
	if len(doc_celex_id) > 11:
		col1, col2, col3 = st.columns((1, 1, 2))
	else:
		col1, col2, col3 = st.columns(3)
	col1.write(f"Date: {doc_date}")
	col2.write(f"Format: {doc_mtypes}")
	col3.write(f"CELEX: {doc_celex_id}")
	st.write(f"<font size='+4'>Title:\n<a href='{doc_url}' id='my-link'>{doc_title}</a>", unsafe_allow_html=True)
	authors_list_formatted = "\n"
	for author in doc_authors.split('|'):
		authors_list_formatted += f"- {author}\n"
	st.markdown(f"""
	Authors:
	{authors_list_formatted}
	""", unsafe_allow_html=True)
	subjects_list_formatted = "\n"
	for subject in list(set(doc_subjects.split('|'))):
		subjects_list_formatted += f"- {subject}\n"
	st.markdown(f"""
		Subjects:
		{subjects_list_formatted}
		""", unsafe_allow_html=True)
	st.write("---")

