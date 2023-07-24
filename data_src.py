import os
import re
import src_utils
import settings
# from eurlex_regtech_webapp_demo import settings


class DataSrc:
	
	def __init__(self, sparql_query_name=None, base_sparql_query_name="eurlex_base_financial_domain_sparql_query"):
		self.sparql_query_name = sparql_query_name
		self.sparql_query_path = os.path.join(settings.SPARQL_QUERIES_DIR, f"{self.sparql_query_name}.rq")
		self.base_sparql_query_name = base_sparql_query_name
		self.base_sparql_queries_dir = os.path.join(settings.SPARQL_QUERIES_DIR, "base_queries")
		self.base_sparql_query_file_path = os.path.join(self.base_sparql_queries_dir, f"{self.base_sparql_query_name}.rq")
		self.__query_str = None
		
		
	@property
	def query_str(self):
		if self.__query_str is None:
			if self.sparql_query_name is not None:
				self.__query_str = src_utils.text_to_str(self.sparql_query_path)
			else:
				self.__query_str = src_utils.text_to_str(self.base_sparql_query_file_path)
		return self.__query_str
		
	@property
	def query_limit(self):
		numerics = re.findall(r'\d+', self.query_str[19363:])
		limit = list(map(int, numerics))
		return limit[0]
		
