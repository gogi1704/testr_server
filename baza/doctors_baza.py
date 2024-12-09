import baza.baza_util_funs as util_funs
# from langchain.vectorstores.faiss import FAISS
# from langchain.embeddings.openai import OpenAIEmbeddings

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()




doctors_url = "https://docs.google.com/document/d/1Jtxb2sOW_405otvekp4-SrSgjdRveYovpy7Qsn9pqcc/edit?usp=sharing"
file_name = "doctors_baza.txt"

#Вызывается 1 раз при запуске
def load_doctors_baza():
    text = util_funs.load_document_text(doctors_url)

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)
        print("Файл успешно создан - doctors_baza.txt")


async def get_chunks(file_name,prompt, chunks_count = 2):
    text = ''
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()

    documents = await util_funs.split_text(text)

    db = FAISS.from_documents(documents, embeddings)
    chunks = db.similarity_search(prompt, k=chunks_count)
    return chunks

