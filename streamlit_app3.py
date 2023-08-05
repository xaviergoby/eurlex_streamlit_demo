import json
import time
import data_src
from utils import get_sparql_query_results
import streamlit as st
import pprint


eurlex_src = data_src.DataSrc(sparql_query_name="financial_domain_eurlex_sparql_query_non_distinct_grouping")
query = eurlex_src.query_str

results = get_sparql_query_results(query)
pprint.pprint(results)
