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
    table_name="qa_new_demo",
)

directory_path = "docx/"
docx_files = [f for f in os.listdir(directory_path) if f.endswith('.docx')]

doc_paragraphs = []

for docx_file in docx_files:
    docx_file_path = os.path.join(directory_path, docx_file)
    content = docx2txt.process(docx_file_path).strip()
    paragraphs = [p for p in content.split(".") if p]
    doc_paragraphs.extend(paragraphs)
print(doc_paragraphs)


total_paragraphs = len(doc_paragraphs)
print(
    f"Generating embeddings and storing in AstraDb for {total_paragraphs} paragraphs")
myCassandraVStore.add_texts(doc_paragraphs)
print(f"Inserted embeddings for {total_paragraphs} paragraphs")
