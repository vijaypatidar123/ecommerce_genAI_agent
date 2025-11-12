# Simple local RAG with sentence-transformers + FAISS (no internet needed)
import os, glob
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

_model = SentenceTransformer(os.getenv("EMBED_MODEL","all-MiniLM-L6-v2"))
_index = None
_chunks = []

def _load_docs():
    texts=[]
    for fp in glob.glob("rag_corpus/*.pdf"):
        try:
            pdf = PdfReader(fp)
            txt = "\n".join(p.extract_text() or "" for p in pdf.pages)
            texts.append((os.path.basename(fp), txt))
        except: pass
    return texts

def _build_index():
    global _index, _chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = _load_docs()
    for name, txt in docs:
        for ch in splitter.split_text(txt):
            _chunks.append((name, ch))
    if not _chunks:
        _index = None
        return
    embs = _model.encode([c[1] for c in _chunks], convert_to_numpy=True, show_progress_bar=True)
    _index = faiss.IndexFlatIP(embs.shape[1])
    faiss.normalize_L2(embs)
    _index.add(embs)

_build_index()

def search_docs(query, k=4):
    if _index is None:
        return "No external docs indexed."
    q = _model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q)
    D, I = _index.search(q, k)
    out=[]
    for idx in I[0]:
        name, ch = _chunks[idx]
        out.append(f"[{name}] {ch[:800]}...")
    return "\n\n".join(out)
