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

print("load data from huggingface")
myDataset=load_dataset("Biddls/Onion_News", split="train")
headlines = myDatasets["text"][:50]

print("Generate embedding and store in AstraDb")
myCassandraVStore.add_texts(headlines)

print(f"Inserted {len(headlines} headlines")
vectorIndex= VectorStoreIndexWrapper(vectorstore=myCassandraVStore)


while True:
	query_text=input("Enter question (type 'quit' to exit")
	
	if query_text.lower()=="quit":
		break

	print("Question: ",query_text)
	answer=vectorIndex.query(quert_text,llm=llm).strip()
	print(f"Answer:{answer}")

	print("Document by relevance:")
	for doc,store in myCassandraVStore.similarity_search_with_score(query_text,k=4):
		print(score,doc.page_content)
