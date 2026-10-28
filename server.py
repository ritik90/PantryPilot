from pathlib import Path
import chromadb
from mcp.server import MCPServer

DB_DIR = Path(__file__).parent / "chroma_store"

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(name="secondbrain")

mcp = MCPServer("SecondBrain")

_next_id = [collection.count()]

@mcp.tool()
def add_document(text: str, source: str = "") -> str:
    """Store a piece of text in the knowledge base, tagged with its source."""
    doc_id = str(_next_id[0])
    _next_id[0] += 1
    collection.add(documents=[text], metadatas=[{"source": source}], ids=[doc_id])
    return f"Stored document (id={doc_id}) from source '{source}'."

@mcp.tool()
def search_knowledge(query: str, top_k: int = 5) -> str:
    """Search the knowledge base for text relevant to the query."""
    results = collection.query(query_texts=[query], n_results=top_k)
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    if not docs:
        return "No relevant documents found."

    lines = []
    for doc, meta in zip(docs, metas):
        source = meta.get("source", "unknown")
        lines.append(f"[{source}] {doc}")
    return "\n\n".join(lines)