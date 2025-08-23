from fastapi import APIRouter, UploadFile
import shutil
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from services.vectorstore import vector_store, DATA_DIR

router = APIRouter()

@router.post("/file/")
async def upload_file(file: UploadFile):
    try:
        file_path = os.path.join(DATA_DIR, file.filename)
        
        # Salvar arquivo no disco
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Carregar documento
        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file.filename.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            return {"error": "Formato não suportado. Apenas PDF ou TXT."}
        
        documents = loader.load()
        
        # Dividir em chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(documents)
        
        # Adicionar metadados e IDs customizados
        for i, doc in enumerate(docs):
            doc.metadata["filename"] = file.filename
            doc.metadata["chunk"] = i
        ids = [f"{file.filename}_{i}" for i in range(len(docs))]
        
        vector_store.add_documents(docs, ids=ids)
        
        return {"message": f"{file.filename} adicionado ao banco vetorial!"}
    
    except Exception as e:
        return {"error": str(e)}
