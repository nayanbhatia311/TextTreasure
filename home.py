from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import docx2txt
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import docx2txt
from dotenv import load_dotenv
import os
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from functools import wraps
import models

load_dotenv()

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

home_bp = Blueprint(
    'home',
    __name__
)


@home_bp.get('/')
@jwt_required()
def index():
    message = request.args.get('message')
    csrf_token = get_jwt().get("csrf")

    return render_template('index.html', message=message, csrf_token=csrf_token)


@home_bp.post('/ask_question')
@jwt_required()
def ask_question():
    question = request.form['question']
    vectorIndex = VectorStoreIndexWrapper(vectorstore=myCassandraVStore)
    answer = vectorIndex.query(question, llm=llm).strip()

    relevant_docs = [(doc.page_content, "%0.4f" % score) for doc,
                     score in myCassandraVStore.similarity_search_with_score(question, k=4)]

    csrf_token = get_jwt().get("csrf")
    return render_template('index.html', answer=answer, relevant_docs=relevant_docs, csrf_token=csrf_token)

# @home_bp.post('/add_embeddings')
# def add_embeddings():
#     directory_path = "docx/"
#     docx_files = [f for f in os.listdir(directory_path) if f.endswith('.docx')]
#     doc_paragraphs = []

#     for docx_file in docx_files:
#         docx_file_path = os.path.join(directory_path, docx_file)
#         content = docx2txt.process(docx_file_path).strip()
#         paragraphs = [p for p in content.split("\n") if p]
#         doc_paragraphs.extend(paragraphs)

#     myCassandraVStore.add_texts(doc_paragraphs)

#     return redirect(url_for('index', message="Creating embeddings from docx/ and sending to the online DB."))
