# # import faiss
# # import numpy as np
# # # from app.llm_engine import embedding_model
# # from sentence_transformers import SentenceTransformer

# # # Load sentence transformer model
# # embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# # index = faiss.IndexFlatL2(384)  # assuming embedding dim = 384
# # stored_chunks = []

# # def add_chunks(chunks):
# #     global stored_chunks
# #     embeddings = embedding_model.encode(chunks)
# #     index.add(np.array(embeddings).astype('float32'))
# #     stored_chunks.extend(chunks)

# # def search(query, top_k=5):
# #     query_vec = embedding_model.encode([query])
# #     D, I = index.search(np.array(query_vec).astype('float32'), top_k)
# #     return [stored_chunks[i] for i in I[0]]


# # import faiss
# # import numpy as np
# # from sentence_transformers import SentenceTransformer

# # # Load SentenceTransformer embedding model
# # embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# # EMBEDDING_DIM = 384  # embedding dimension for all-MiniLM-L6-v2

# # # Initialize FAISS index
# # index = faiss.IndexFlatL2(EMBEDDING_DIM)
# # stored_chunks = []

# # def add_chunks(chunks):
# #     """Embeds and adds chunks to the FAISS index."""
# #     global stored_chunks
# #     if not chunks:
# #         return

# #     embeddings = embedding_model.encode(chunks, convert_to_numpy=True)
# #     index.add(embeddings.astype('float32'))
# #     stored_chunks.extend(chunks)

# # def get_relevant_chunks(query, top_k=5):
# #     """Search FAISS index for chunks relevant to the query."""
# #     if not stored_chunks or index.ntotal == 0:
# #         raise ValueError("Index is empty. Call add_chunks() first.")

# #     query_vec = embedding_model.encode([query], convert_to_numpy=True)
# #     D, I = index.search(query_vec.astype('float32'), top_k)
# #     return [stored_chunks[i] for i in I[0] if i < len(stored_chunks)]


# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# # Load SentenceTransformer embedding model
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# EMBEDDING_DIM = 384  # embedding dimension for all-MiniLM-L6-v2

# # Initialize FAISS index
# index = faiss.IndexFlatL2(EMBEDDING_DIM)
# stored_chunks = []

# def add_chunks(chunks):
#     """Embeds and adds chunks to the FAISS index."""
#     global stored_chunks
#     if not chunks:
#         return

#     embeddings = embedding_model.encode(chunks, convert_to_numpy=True)
#     index.add(embeddings.astype('float32'))
#     stored_chunks.extend(chunks)

# def get_relevant_chunks(query, top_k=5):
#     """Search FAISS index for chunks relevant to the query."""
#     if not stored_chunks or index.ntotal == 0:
#         raise ValueError("Index is empty. Call add_chunks() first.")

#     query_vec = embedding_model.encode([query], convert_to_numpy=True)
#     D, I = index.search(query_vec.astype('float32'), top_k)
#     return [stored_chunks[i] for i in I[0] if i < len(stored_chunks)]

# # Alias for compatibility
# def search(query, top_k=5):
#     """Alias to get_relevant_chunks() for compatibility."""
#     return get_relevant_chunks(query, top_k)


from sentence_transformers import SentenceTransformer
import faiss

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)  # 384 = embedding dim
stored_chunks = []

def add_chunks(chunks):
    global stored_chunks
    embeddings = embedding_model.encode(chunks)
    index.add(embeddings)
    stored_chunks.extend(chunks)

def get_relevant_chunks(query, top_k=5):
    query_embedding = embedding_model.encode([query])
    D, I = index.search(query_embedding, top_k)
    return [stored_chunks[i] for i in I[0]]