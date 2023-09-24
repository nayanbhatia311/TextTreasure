ASTRA_DB_SECURE_BUNDLE_PATH=""
ASTRA_DB_APPLICATION_TOKEN=""
ASTRA_DB_CLIENT_ID=""
ASTRA_DB_SECRET=""
ASTRA_DB_KEYSPACE=""
OPENAI_API_KEY=""

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from datasets import load_datasets

#connect to astra db

cloud_config = {
'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
}

auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID,ASTRA_DB_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astraSession= cluster.connect()

llm = OPENAI(openai_api_key=OPENAI_API_KEY)
myEmbedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

myCassandraVStore = Cassandra(
	embedding=myEmbedding,
	session=astraSession,
	keyspace=ASTRA_DB_KEYSPACE,
	table_name="qa_mini_demo",

)
