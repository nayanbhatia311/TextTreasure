from dotenv import load_dotenv
import os
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import docx2txt

load_dotenv()

# Connect to astra db
ASTRA_DB_SECURE_BUNDLE_PATH = os.getenv("ASTRA_DB_SECURE_BUNDLE_PATH")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_CLIENT_ID = os.getenv("ASTRA_DB_CLIENT_ID")
ASTRA_DB_SECRET = os.getenv("ASTRA_DB_SECRET")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

cloud_config = {
    'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
}

auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astraSession = cluster.connect()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
myEmbedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

myCassandraVStore = Cassandra(
    embedding=myEmbedding,
    session=astraSession,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name="qa_mini_demo",
)

directory_path = "docx/"
docx_files = [f for f in os.listdir(directory_path) if f.endswith('.docx')]

doc_contents = {}

# Loop through each file and extract its content
for docx_file in docx_files:
    docx_file_path = os.path.join(directory_path, docx_file)
    content = docx2txt.process(docx_file_path).strip()
    doc_contents[docx_file] = content

# Load data from local .docx file

for doc_name,content in doc_contents.items():

	headlines = content

	print(f"Generate embedding and store in AstraDb for {doc_name}")
	myCassandraVStore.add_texts(headlines)

print(f"Inserted {len(headlines)} headlines")
vectorIndex = VectorStoreIndexWrapper(vectorstore=myCassandraVStore)

while True:
    query_text = input("\nEnter question (type 'quit' to exit)\n")

    if query_text.lower() == "quit":
        break

    print("Question: ", query_text)
    answer = vectorIndex.query(query_text, llm=llm).strip()
    print(f"Answer:{answer}")

    print("Document by relevance:")
    for doc, score in myCassandraVStore.similarity_search_with_score(query_text, k=2):
        print(score, doc.page_content)
