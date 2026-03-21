---
title: "RAG 架构师"
description: "检索增强生成系统架构设计，向量数据库和语义检索优化"
category: "devops"
source: "community"
author: "Community"
tags: ["rag", "architect"]
date: 2026-03-20
---

# RAG Architect

## Core Workflow

1. **Requirements Analysis** — Identify retrieval needs, latency constraints, accuracy requirements, and scale
2. **Vector Store Design** — Select database, schema design, indexing strategy, sharding approach
3. **Chunking Strategy** — Document splitting, overlap, semantic boundaries, metadata enrichment
4. **Retrieval Pipeline** — Embedding selection, query transformation, hybrid search, reranking
5. **Evaluation & Iteration** — Metrics tracking, retrieval debugging, continuous optimization

For each step, validate before moving on (see checkpoints below).

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Vector Databases | `references/vector-databases.md` | Comparing Pinecone, Weaviate, Chroma, pgvector, Qdrant |
| Embedding Models | `references/embedding-models.md` | Selecting embeddings, fine-tuning, dimension trade-offs |
| Chunking Strategies | `references/chunking-strategies.md` | Document splitting, overlap, semantic chunking |
| Retrieval Optimization | `references/retrieval-optimization.md` | Hybrid search, reranking, query expansion, filtering |
| RAG Evaluation | `references/rag-evaluation.md` | Metrics, evaluation frameworks, debugging retrieval |

## Implementation Examples

### 1. Chunking Documents

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Evaluate chunk_size on your domain data — never use 512 blindly
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " "],
)

chunks = splitter.create_documents(
    texts=[doc.page_content for doc in raw_docs],
    metadatas=[{"source": doc.metadata["source"], "timestamp": doc.metadata.get("timestamp")} for doc in raw_docs],
)
```

**Checkpoint:** `assert all(c.metadata.get("source") for c in chunks), "Missing source metadata"`

### 2. Generating Embeddings & Indexing

```python
from openai import OpenAI
import qdrant_client
from qdrant_client.models import VectorParams, Distance, PointStruct

client = OpenAI()
qdrant = qdrant_client.QdrantClient("localhost", port=6333)

# Create collection
qdrant.recreate_collection(
    collection_name="knowledge_base",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

def embed_chunks(chunks: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    response = client.embeddings.create(input=chunks, model=model)
    return [r.embedding for r in response.data]

# Idempotent upsert with deduplication via deterministic IDs
import hashlib, uuid

points = []
for i, chunk in enumerate(chunks):
    doc_id = str(uuid.UUID(hashlib.md5(chunk.page_content.encode()).hexdigest()))
    embedding = embed_chunks([chunk.page_content])[0]
    points.append(PointStruct(id=doc_id, vector=embedding, payload=chunk.metadata))

qdrant.upsert(collection_name="knowledge_base", points=points)
```

**Checkpoint:** `assert qdrant.count("knowledge_base").count == len(set(p.id for p in points)), "Deduplication failed"`

### 3. Hybrid Search (Vector + BM25)

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, SparseVector
from rank_bm25 import BM25Okapi

def hybrid_search(query: str, tenant_id: str, top_k: int = 20) -> list:
    # Dense retrieval
    query_embedding = embed_chunks([query])[0]
    tenant_filter = Filter(must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))])
    dense_results = qdrant.search(
        collection_name="knowledge_base",
        query_vector=query_embedding,
        query_filter=tenant_filter,
        limit=top_k,
    )

    # Sparse retrieval (BM25)
    corpus = [r.payload.get("text", "") for r in dense_results]
    bm25 = BM25Okapi([doc.split() for doc in corpus])
    bm25_scores = bm25.get_scores(query.split())

    # Reciprocal Rank Fusion
    ranked = sorted(
        zip(dense_results, bm25_scores),
        key=lambda x: 0.6 * x[0].score + 0.4 * x[1],
        reverse=True,
    )
    return [r for r, _ in ranked[:top_k]]
```

**Checkpoint:** `assert len(hybrid_search("test query", tenant_id="demo")) > 0, "Hybrid search returned no results"`

### 4. Reranking Top-K Results

```python
import cohere

co = cohere.Client("YOUR_API_KEY")

def rerank(query: str, results: list, top_n: int = 5) -> list:
    docs = [r.payload.get("text", "") for r in results]
    reranked = co.rerank(query=query, documents=docs, top_n=top_n, model="rerank-english-v3.0")
    return [results[r.index] for r in reranked.results]
```

### 5. Retrieval Evaluation

```python
# Run precision@k and recall@k against a labeled evaluation set
# python evaluate.py --metrics precision@10 recall@10 mrr --collection knowledge_base

from ragas import evaluate
from ragas.metrics import context_precision, context_recall, faithfulness, answer_relevancy
from datasets import Dataset

eval_dataset = Dataset.from_dict({
    "question": questions,
    "contexts": retrieved_contexts,
    "answer": generated_answers,
    "ground_truth": ground_truth_answers,
})

results = evaluate(eval_dataset, metrics=[context_precision, context_recall, faithfulness, answer_relevancy])
print(results)
```

**Checkpoint:** Target `context_precision >= 0.7` and `context_recall >= 0.6` before moving to LLM integration.

## Constraints

### MUST DO
- Evaluate multiple embedding models on your domain data before committing
- Implement hybrid search (vector + keyword) for production systems
- Add metadata filters for multi-tenant or domain-specific retrieval
- Measure retrieval metrics (precision@k, recall@k, MRR, NDCG)
- Use reranking for top-k results before passing context to LLM
- Implement idempotent ingestion with deduplication (deterministic IDs)
- Monitor retrieval latency and quality over time
- Version embeddings and plan for model migration

### MUST NOT DO
- Use default chunk size (512) without evaluation on your domain data
- Skip metadata enrichment (source, timestamp, section)
- Ignore retrieval quality metrics in favor of only LLM output quality
- Store raw documents without preprocessing/cleaning
- Use cosine similarity alone for complex multi-domain retrieval
- Deploy without testing on production-like data volumes
- Forget to handle edge cases (empty results, malformed docs)
- Couple the embedding model tightly to application code

## Output Templates

When designing RAG architecture, deliver:
1. System architecture diagram (ingestion + retrieval pipelines)
2. Vector database selection with trade-off analysis
3. Chunking strategy with examples and rationale
4. Retrieval pipeline design (query → results flow)
5. Evaluation plan with metrics, benchmarks, and pass/fail thresholds

---

## Reference: Chunking Strategies

# Chunking Strategies

---

## Strategy Comparison Matrix

| Strategy | Best For | Chunk Quality | Implementation Complexity |
|----------|----------|---------------|---------------------------|
| **Fixed-size** | Simple documents, logs | Low-Medium | Simple |
| **Recursive character** | General text, articles | Medium | Simple |
| **Sentence-based** | Conversational, Q&A | Medium-High | Medium |
| **Semantic** | Technical docs, manuals | High | Medium |
| **Document-aware** | Structured content (MD, HTML) | High | Medium |
| **Agentic/Contextual** | Complex documents | Very High | Complex |
| **Late chunking** | Long-context embeddings | High | Medium |

---

## When to Use Each Strategy

### Fixed-Size Chunking
```
Best For:
- Log files and structured data
- Quick prototyping
- When content has no natural structure
- Baseline comparison

When to Avoid:
- Technical documentation
- Content with semantic units (paragraphs, sections)
- When context preservation matters
```

### Recursive Character Splitting
```
Best For:
- General articles and blog posts
- Mixed content types
- Default starting point for most RAG
- LangChain/LlamaIndex default

When to Avoid:
- Highly structured documents
- Code-heavy content
- Tables and lists
```

### Semantic Chunking
```
Best For:
- Technical documentation
- Research papers
- Content with natural topic boundaries
- When retrieval precision is critical

When to Avoid:
- Real-time ingestion (slower)
- Very short documents
- Cost-sensitive pipelines (requires embeddings)
```

### Document-Aware Chunking
```
Best For:
- Markdown documentation
- HTML pages
- LaTeX papers
- Code files

When to Avoid:
- Plain text without structure
- Inconsistent formatting
```

---

## Fixed-Size Chunking

```python
def fixed_size_chunk(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """Simple fixed-size chunking with overlap."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at word boundary
        if end < len(text):
            last_space = chunk.rfind(' ')
            if last_space > chunk_size * 0.8:  # Only if reasonably far in
                chunk = chunk[:last_space]
                end = start + last_space

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks

# Usage
chunks = fixed_size_chunk(document_text, chunk_size=500, overlap=50)
```

---

## Recursive Character Splitting (LangChain Style)

```python
from typing import Callable

class RecursiveCharacterSplitter:
    """Split text recursively using multiple separators."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: list[str] | None = None,
        length_function: Callable[[str], int] = len
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]
        self.length_function = length_function

    def split_text(self, text: str) -> list[str]:
        """Split text into chunks."""
        return self._split_text(text, self.separators)

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        final_chunks = []
        separator = separators[-1]

        for i, sep in enumerate(separators):
            if sep == "":
                separator = sep
                break
            if sep in text:
                separator = sep
                break

        splits = text.split(separator) if separator else list(text)

        good_splits = []
        for split in splits:
            if self.length_function(split) < self.chunk_size:
                good_splits.append(split)
            else:
                if good_splits:
                    merged = self._merge_splits(good_splits, separator)
                    final_chunks.extend(merged)
                    good_splits = []
                # Recursively split large chunks
                other_chunks = self._split_text(split, separators[separators.index(separator) + 1:])
                final_chunks.extend(other_chunks)

        if good_splits:
            merged = self._merge_splits(good_splits, separator)
            final_chunks.extend(merged)

        return final_chunks

    def _merge_splits(self, splits: list[str], separator: str) -> list[str]:
        """Merge splits into chunks respecting size limits."""
        chunks = []
        current_chunk = []
        current_length = 0

        for split in splits:
            split_length = self.length_function(split)

            if current_length + split_length > self.chunk_size:
                if current_chunk:
                    chunks.append(separator.join(current_chunk))
                    # Keep overlap
                    while current_length > self.chunk_overlap and current_chunk:
                        current_length -= self.length_function(current_chunk[0])
                        current_chunk = current_chunk[1:]

            current_chunk.append(split)
            current_length += split_length

        if current_chunk:
            chunks.append(separator.join(current_chunk))

        return chunks

# Usage
splitter = RecursiveCharacterSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_text(document_text)
```

### Token-Based Splitting

```python
import tiktoken

def create_token_splitter(
    model: str = "gpt-4",
    chunk_size: int = 500,
    chunk_overlap: int = 50
):
    """Create splitter that counts tokens instead of characters."""
    encoding = tiktoken.encoding_for_model(model)

    def token_length(text: str) -> int:
        return len(encoding.encode(text))

    return RecursiveCharacterSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=token_length
    )

# Usage
token_splitter = create_token_splitter(chunk_size=500, chunk_overlap=50)
chunks = token_splitter.split_text(document_text)
```

---

## Sentence-Based Chunking

```python
import re
from dataclasses import dataclass

@dataclass
class SentenceChunk:
    text: str
    sentences: list[str]
    start_sentence: int
    end_sentence: int

def sentence_chunk(
    text: str,
    sentences_per_chunk: int = 5,
    overlap_sentences: int = 1
) -> list[SentenceChunk]:
    """Chunk by sentence count with overlap."""
    # Split into sentences
    sentence_pattern = r'(?<=[.!?])\s+'
    sentences = re.split(sentence_pattern, text)
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    i = 0

    while i < len(sentences):
        end = min(i + sentences_per_chunk, len(sentences))
        chunk_sentences = sentences[i:end]

        chunks.append(SentenceChunk(
            text=" ".join(chunk_sentences),
            sentences=chunk_sentences,
            start_sentence=i,
            end_sentence=end - 1
        ))

        i += sentences_per_chunk - overlap_sentences

    return chunks

# Better sentence splitting with NLTK
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def sentence_chunk_nltk(
    text: str,
    max_chunk_size: int = 1000,
    overlap_sentences: int = 2
) -> list[str]:
    """Chunk by sentences up to max size."""
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_size = len(sentence)

        if current_size + sentence_size > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            # Keep overlap sentences
            current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences else []
            current_size = sum(len(s) for s in current_chunk)

        current_chunk.append(sentence)
        current_size += sentence_size

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
```

---

## Semantic Chunking

```python
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticChunker:
    """Chunk based on semantic similarity between sentences."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.5,
        min_chunk_size: int = 100,
        max_chunk_size: int = 1500
    ):
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size

    def chunk(self, text: str) -> list[str]:
        """Split text at semantic boundaries."""
        # Split into sentences
        sentences = self._split_sentences(text)
        if len(sentences) <= 1:
            return [text]

        # Get embeddings
        embeddings = self.model.encode(sentences)

        # Find breakpoints based on similarity drops
        breakpoints = self._find_breakpoints(embeddings)

        # Create chunks
        chunks = []
        start = 0

        for bp in breakpoints:
            chunk_text = " ".join(sentences[start:bp])

            # Handle size constraints
            if len(chunk_text) > self.max_chunk_size:
                # Split large chunks
                sub_chunks = self._split_large_chunk(sentences[start:bp])
                chunks.extend(sub_chunks)
            elif len(chunk_text) >= self.min_chunk_size:
                chunks.append(chunk_text)
            elif chunks:
                # Merge small chunk with previous
                chunks[-1] += " " + chunk_text
            else:
                chunks.append(chunk_text)

            start = bp

        # Handle remaining sentences
        if start < len(sentences):
            remaining = " ".join(sentences[start:])
            if chunks and len(remaining) < self.min_chunk_size:
                chunks[-1] += " " + remaining
            else:
                chunks.append(remaining)

        return chunks

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _find_breakpoints(self, embeddings: np.ndarray) -> list[int]:
        """Find semantic breakpoints using similarity drops."""
        breakpoints = []

        for i in range(1, len(embeddings)):
            similarity = cosine_similarity(
                embeddings[i-1:i],
                embeddings[i:i+1]
            )[0][0]

            if similarity < self.similarity_threshold:
                breakpoints.append(i)

        return breakpoints

    def _split_large_chunk(self, sentences: list[str]) -> list[str]:
        """Split oversized chunk at midpoint."""
        mid = len(sentences) // 2
        return [
            " ".join(sentences[:mid]),
            " ".join(sentences[mid:])
        ]

# Usage
chunker = SemanticChunker(
    similarity_threshold=0.5,
    min_chunk_size=200,
    max_chunk_size=1000
)
semantic_chunks = chunker.chunk(document_text)
```

### Percentile-Based Breakpoints

```python
def find_breakpoints_percentile(
    embeddings: np.ndarray,
    percentile: int = 25
) -> list[int]:
    """Find breakpoints at similarity drops below percentile threshold."""
    similarities = []

    for i in range(1, len(embeddings)):
        sim = cosine_similarity(
            embeddings[i-1:i],
            embeddings[i:i+1]
        )[0][0]
        similarities.append((i, sim))

    # Dynamic threshold based on distribution
    sim_values = [s[1] for s in similarities]
    threshold = np.percentile(sim_values, percentile)

    return [i for i, sim in similarities if sim < threshold]
```

---

## Document-Aware Chunking

### Markdown Chunking

```python
import re
from dataclasses import dataclass

@dataclass
class MarkdownChunk:
    text: str
    heading: str | None
    heading_level: int
    metadata: dict

def chunk_markdown(
    text: str,
    max_chunk_size: int = 1500,
    include_heading_in_chunk: bool = True
) -> list[MarkdownChunk]:
    """Chunk markdown by headers while respecting structure."""
    # Pattern to match headers
    header_pattern = r'^(#{1,6})\s+(.+)$'

    lines = text.split('\n')
    chunks = []
    current_chunk_lines = []
    current_heading = None
    current_level = 0
    heading_stack = []  # For breadcrumb context

    for line in lines:
        header_match = re.match(header_pattern, line)

        if header_match:
            # Save current chunk if exists
            if current_chunk_lines:
                chunk_text = '\n'.join(current_chunk_lines)
                if len(chunk_text.strip()) > 0:
                    prefix = f"# {current_heading}\n\n" if include_heading_in_chunk and current_heading else ""
                    chunks.append(MarkdownChunk(
                        text=prefix + chunk_text,
                        heading=current_heading,
                        heading_level=current_level,
                        metadata={"breadcrumb": " > ".join(heading_stack)}
                    ))

            # Update heading context
            level = len(header_match.group(1))
            heading = header_match.group(2).strip()

            # Maintain heading stack for breadcrumbs
            while heading_stack and current_level >= level:
                heading_stack.pop()
                current_level -= 1

            heading_stack.append(heading)
            current_heading = heading
            current_level = level
            current_chunk_lines = []

        else:
            current_chunk_lines.append(line)

            # Check chunk size
            current_text = '\n'.join(current_chunk_lines)
            if len(current_text) > max_chunk_size:
                # Split at paragraph boundary
                paragraphs = current_text.split('\n\n')
                if len(paragraphs) > 1:
                    split_point = len('\n\n'.join(paragraphs[:-1]))
                    chunk_text = current_text[:split_point]
                    prefix = f"# {current_heading}\n\n" if include_heading_in_chunk and current_heading else ""
                    chunks.append(MarkdownChunk(
                        text=prefix + chunk_text,
                        heading=current_heading,
                        heading_level=current_level,
                        metadata={"breadcrumb": " > ".join(heading_stack)}
                    ))
                    current_chunk_lines = [current_text[split_point:].strip()]

    # Don't forget the last chunk
    if current_chunk_lines:
        chunk_text = '\n'.join(current_chunk_lines)
        if len(chunk_text.strip()) > 0:
            prefix = f"# {current_heading}\n\n" if include_heading_in_chunk and current_heading else ""
            chunks.append(MarkdownChunk(
                text=prefix + chunk_text,
                heading=current_heading,
                heading_level=current_level,
                metadata={"breadcrumb": " > ".join(heading_stack)}
            ))

    return chunks
```

### Code-Aware Chunking

```python
import re
from dataclasses import dataclass

@dataclass
class CodeChunk:
    text: str
    language: str | None
    chunk_type: str  # "code", "text", "mixed"

def chunk_with_code_blocks(
    text: str,
    max_chunk_size: int = 1500
) -> list[CodeChunk]:
    """Chunk text while keeping code blocks intact."""
    # Pattern to match code blocks
    code_block_pattern = r'```(\w+)?\n(.*?)```'

    chunks = []
    last_end = 0

    for match in re.finditer(code_block_pattern, text, re.DOTALL):
        # Text before code block
        text_before = text[last_end:match.start()].strip()
        if text_before:
            # Chunk the text portion
            text_chunks = recursive_chunk(text_before, max_chunk_size)
            chunks.extend([
                CodeChunk(text=t, language=None, chunk_type="text")
                for t in text_chunks
            ])

        # Code block (keep intact if possible)
        language = match.group(1)
        code_content = match.group(2)
        full_block = match.group(0)

        if len(full_block) <= max_chunk_size:
            chunks.append(CodeChunk(
                text=full_block,
                language=language,
                chunk_type="code"
            ))
        else:
            # Split large code blocks by function/class
            code_chunks = split_code_block(code_content, language, max_chunk_size)
            chunks.extend(code_chunks)

        last_end = match.end()

    # Remaining text after last code block
    remaining = text[last_end:].strip()
    if remaining:
        text_chunks = recursive_chunk(remaining, max_chunk_size)
        chunks.extend([
            CodeChunk(text=t, language=None, chunk_type="text")
            for t in text_chunks
        ])

    return chunks

def split_code_block(code: str, language: str, max_size: int) -> list[CodeChunk]:
    """Split code block at logical boundaries."""
    # Simple function/class boundary splitting for Python
    if language == "python":
        pattern = r'\n(?=def |class |async def )'
    elif language in ["javascript", "typescript"]:
        pattern = r'\n(?=function |class |const |export )'
    else:
        pattern = r'\n\n'

    parts = re.split(pattern, code)
    chunks = []
    current = ""

    for part in parts:
        if len(current) + len(part) > max_size and current:
            chunks.append(CodeChunk(
                text=f"```{language}\n{current}```",
                language=language,
                chunk_type="code"
            ))
            current = part
        else:
            current += part

    if current:
        chunks.append(CodeChunk(
            text=f"```{language}\n{current}```",
            language=language,
            chunk_type="code"
        ))

    return chunks
```

---

## Contextual/Agentic Chunking

```python
from openai import OpenAI

def contextual_chunk(
    document: str,
    max_chunk_size: int = 1500
) -> list[dict]:
    """Use LLM to add context to each chunk."""
    # First, do structural chunking
    base_chunks = recursive_chunk(document, max_chunk_size)

    client = OpenAI()
    contextualized_chunks = []

    for chunk in base_chunks:
        # Generate contextual summary
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Provide a brief context for this document chunk.
                    Include: what topic it covers, how it relates to the broader document,
                    and key concepts mentioned. Keep it under 100 words."""
                },
                {
                    "role": "user",
                    "content": f"Document excerpt:\n\n{chunk}"
                }
            ],
            max_tokens=150
        )

        context = response.choices[0].message.content

        contextualized_chunks.append({
            "text": chunk,
            "context": context,
            "text_with_context": f"Context: {context}\n\nContent: {chunk}"
        })

    return contextualized_chunks
```

### Propositions-Based Chunking

```python
def extract_propositions(text: str) -> list[str]:
    """Extract atomic propositions from text using LLM."""
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Extract atomic propositions from the text.
                Each proposition should:
                - Be a single, complete fact
                - Be self-contained (understandable without context)
                - Include necessary entity references

                Return as a JSON array of strings."""
            },
            {
                "role": "user",
                "content": text
            }
        ],
        response_format={"type": "json_object"}
    )

    import json
    result = json.loads(response.choices[0].message.content)
    return result.get("propositions", [])

# Usage: For very fine-grained retrieval
propositions = extract_propositions(document_text)
# Each proposition becomes its own retrievable unit
```

---

## Late Chunking (for Long-Context Embeddings)

```python
from transformers import AutoTokenizer, AutoModel
import torch

class LateChunker:
    """
    Late chunking: embed full document, then pool token embeddings into chunks.
    Preserves full document context while creating retrievable chunks.
    """

    def __init__(self, model_name: str = "jinaai/jina-embeddings-v2-base-en"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        self.model.eval()

    def chunk_and_embed(
        self,
        text: str,
        chunk_size: int = 512,
        overlap: int = 64
    ) -> list[dict]:
        """
        Embed full document, then create chunk embeddings via mean pooling.
        """
        # Tokenize full document
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=8192  # Model's max context
        )

        # Get token-level embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            token_embeddings = outputs.last_hidden_state[0]  # [seq_len, hidden_dim]

        # Get token-to-text mapping
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

        # Create chunks from token embeddings
        chunks = []
        seq_len = token_embeddings.shape[0]
        start = 0

        while start < seq_len:
            end = min(start + chunk_size, seq_len)

            # Mean pool token embeddings for this chunk
            chunk_embedding = token_embeddings[start:end].mean(dim=0).numpy()

            # Reconstruct text for this chunk
            chunk_token_ids = inputs["input_ids"][0][start:end]
            chunk_text = self.tokenizer.decode(chunk_token_ids, skip_special_tokens=True)

            chunks.append({
                "text": chunk_text,
                "embedding": chunk_embedding,
                "start_token": start,
                "end_token": end
            })

            start = end - overlap

        return chunks

# Usage
late_chunker = LateChunker()
chunks_with_embeddings = late_chunker.chunk_and_embed(
    long_document,
    chunk_size=512,
    overlap=64
)
```

---

## Metadata Enrichment

```python
from dataclasses import dataclass
from datetime import datetime
import hashlib

@dataclass
class EnrichedChunk:
    text: str
    embedding: list[float] | None
    metadata: dict

def enrich_chunk(
    text: str,
    source_file: str,
    chunk_index: int,
    total_chunks: int,
    additional_metadata: dict | None = None
) -> EnrichedChunk:
    """Add comprehensive metadata to chunk."""
    metadata = {
        # Source tracking
        "source": source_file,
        "chunk_index": chunk_index,
        "total_chunks": total_chunks,

        # Content characteristics
        "char_count": len(text),
        "word_count": len(text.split()),
        "content_hash": hashlib.md5(text.encode()).hexdigest()[:12],

        # Temporal
        "indexed_at": datetime.utcnow().isoformat(),

        # Position context
        "position": "start" if chunk_index == 0 else (
            "end" if chunk_index == total_chunks - 1 else "middle"
        )
    }

    if additional_metadata:
        metadata.update(additional_metadata)

    return EnrichedChunk(text=text, embedding=None, metadata=metadata)
```

---

## Chunk Size Selection Guide

| Document Type | Recommended Size | Overlap | Rationale |
|--------------|------------------|---------|-----------|
| FAQ/Q&A | 200-400 tokens | 20-50 | Keep Q&A pairs together |
| Technical docs | 400-600 tokens | 50-100 | Balance context vs precision |
| Legal/contracts | 600-800 tokens | 100-150 | Preserve clause context |
| Code documentation | 300-500 tokens | 50-100 | Keep function docs together |
| Chat transcripts | 150-300 tokens | 25-50 | Natural turn boundaries |
| Research papers | 500-800 tokens | 100-200 | Section-level coherence |

---

## Quick Reference

| Strategy | Use Case | Code Pattern |
|----------|----------|--------------|
| Fixed-size | Logs, baseline | `text[i:i+chunk_size]` |
| Recursive | General text | Split by `["\n\n", "\n", ". "]` |
| Sentence | Q&A content | `sent_tokenize()` + merge |
| Semantic | Technical docs | Similarity-based breaks |
| Markdown | Documentation | Header-aware splitting |
| Late chunking | Long-context models | Embed full, pool chunks |

## Related Skills

- **RAG Architect** - Integration with vector databases
- **Python Pro** - Preprocessing pipelines
- **NLP Engineer** - Tokenization and text processing

---

## Reference: Embedding Models

# Embedding Models

---

## Model Comparison Matrix

| Model | Dimensions | Max Tokens | Strengths | Provider |
|-------|------------|------------|-----------|----------|
| **text-embedding-3-large** | 3072 (or 256-3072) | 8191 | Best quality, flexible dims | OpenAI |
| **text-embedding-3-small** | 1536 (or 256-1536) | 8191 | Cost-effective, good quality | OpenAI |
| **embed-english-v3.0** | 1024 | 512 | Excellent compression, fast | Cohere |
| **embed-multilingual-v3.0** | 1024 | 512 | 100+ languages | Cohere |
| **voyage-large-2** | 1536 | 16000 | Long context, code-aware | Voyage AI |
| **voyage-code-2** | 1536 | 16000 | Code retrieval specialist | Voyage AI |
| **BGE-large-en-v1.5** | 1024 | 512 | Open source, high quality | BAAI |
| **BGE-M3** | 1024 | 8192 | Multi-lingual, multi-granularity | BAAI |
| **E5-large-v2** | 1024 | 512 | Strong benchmark performance | Microsoft |
| **GTE-large** | 1024 | 512 | Good general-purpose | Alibaba |
| **all-MiniLM-L6-v2** | 384 | 256 | Fast, lightweight | Sentence Transformers |
| **nomic-embed-text-v1.5** | 768 | 8192 | Long context, open weights | Nomic AI |

---

## When to Use Each Model

### OpenAI text-embedding-3-large
```
Best For:
- Production RAG requiring highest accuracy
- Enterprise applications with quality SLAs
- Flexible dimension requirements (can reduce to save cost)
- English and major languages

When to Avoid:
- Cost-sensitive high-volume applications
- Air-gapped or offline deployments
- Specialized domains without fine-tuning budget
```

### OpenAI text-embedding-3-small
```
Best For:
- Cost-effective production deployments
- Good quality-to-cost ratio
- General-purpose retrieval tasks
- Quick prototyping with API simplicity

When to Avoid:
- Maximum accuracy requirements
- Specialized technical domains
- When open-source is required
```

### Cohere embed-v3
```
Best For:
- Multi-lingual applications (100+ languages)
- Search-optimized retrieval (search_document/search_query types)
- Compression (int8/binary quantization built-in)
- Production with cost constraints

When to Avoid:
- Very long documents (512 token limit)
- Code-heavy retrieval tasks
```

### Voyage AI
```
Best For:
- Code retrieval and technical documentation
- Long-context documents (16K tokens)
- Domain-specific fine-tuning options
- Legal/financial specialized models

When to Avoid:
- Budget-constrained projects
- Simple general-purpose retrieval
```

### BGE / E5 (Open Source)
```
Best For:
- Self-hosted deployments
- Air-gapped environments
- Cost elimination (no API fees)
- Fine-tuning on custom domains

When to Avoid:
- Teams without GPU infrastructure
- Need for zero maintenance
- Maximum out-of-box quality
```

---

## OpenAI Embeddings

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def get_embedding(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: int | None = None
) -> list[float]:
    """Get embedding with optional dimension reduction."""
    params = {"input": text, "model": model}
    if dimensions:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    return response.data[0].embedding

# Single embedding
embedding = get_embedding("How do I install the software?")

# Batch embeddings (more efficient)
def get_embeddings_batch(
    texts: list[str],
    model: str = "text-embedding-3-small",
    dimensions: int | None = None
) -> list[list[float]]:
    """Batch embed multiple texts."""
    params = {"input": texts, "model": model}
    if dimensions:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    # Sort by index to maintain order
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]

embeddings = get_embeddings_batch(["text1", "text2", "text3"])

# Dimension reduction (cost/storage savings)
# text-embedding-3-large: 3072 -> 1024 (66% storage savings)
reduced_embedding = get_embedding(
    "Installation guide...",
    model="text-embedding-3-large",
    dimensions=1024  # Reduce from 3072
)
```

### Dimension Trade-offs

| Original | Reduced | Quality Loss | Storage Savings |
|----------|---------|--------------|-----------------|
| 3072 | 1536 | ~1-2% | 50% |
| 3072 | 1024 | ~2-4% | 67% |
| 3072 | 512 | ~5-8% | 83% |
| 3072 | 256 | ~10-15% | 92% |

---

## Cohere Embeddings

```python
import cohere

co = cohere.Client(api_key="your-api-key")

# Document embeddings (for indexing)
doc_embeddings = co.embed(
    texts=["Installation guide content...", "Configuration steps..."],
    model="embed-english-v3.0",
    input_type="search_document",  # Use for documents being indexed
    truncate="END"
).embeddings

# Query embeddings (for search)
query_embedding = co.embed(
    texts=["how to install"],
    model="embed-english-v3.0",
    input_type="search_query",  # Use for search queries
).embeddings[0]

# Multilingual
multilingual_embedding = co.embed(
    texts=["Comment installer le logiciel?"],  # French
    model="embed-multilingual-v3.0",
    input_type="search_query"
).embeddings[0]

# Compressed embeddings (int8)
compressed = co.embed(
    texts=["Document content..."],
    model="embed-english-v3.0",
    input_type="search_document",
    embedding_types=["int8"]  # 4x smaller than float32
).embeddings
```

### Cohere Input Types

| Type | Use Case |
|------|----------|
| `search_document` | Documents being indexed in vector DB |
| `search_query` | User search queries |
| `classification` | Text classification tasks |
| `clustering` | Document clustering |

---

## Voyage AI Embeddings

```python
import voyageai

vo = voyageai.Client(api_key="your-api-key")

# General embeddings
result = vo.embed(
    texts=["Installation guide for the software..."],
    model="voyage-large-2",
    input_type="document"
)
embeddings = result.embeddings

# Code embeddings (specialized)
code_result = vo.embed(
    texts=[
        "def install_package(name):\n    subprocess.run(['pip', 'install', name])",
        "How do I install packages in Python?"
    ],
    model="voyage-code-2",
    input_type="document"  # or "query" for search
)

# Long context (up to 16K tokens)
long_doc_embedding = vo.embed(
    texts=[very_long_document],  # Up to 16K tokens
    model="voyage-large-2",
    input_type="document"
).embeddings[0]
```

---

## Open Source Models (Sentence Transformers)

```python
from sentence_transformers import SentenceTransformer

# Load model (downloads on first use)
model = SentenceTransformer("BAAI/bge-large-en-v1.5")

# Single embedding
embedding = model.encode("How do I install the software?")

# Batch encoding (GPU accelerated)
embeddings = model.encode(
    ["doc1", "doc2", "doc3"],
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True  # For cosine similarity
)

# BGE requires instruction prefix for queries
query_embedding = model.encode(
    "Represent this sentence for searching relevant passages: How do I install?"
)

# GPU acceleration
model = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cuda")

# Multi-GPU encoding
pool = model.start_multi_process_pool()
embeddings = model.encode_multi_process(
    sentences=large_corpus,
    pool=pool,
    batch_size=64
)
model.stop_multi_process_pool(pool)
```

### BGE-M3 (Multi-lingual, Multi-granularity)

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

# Dense, sparse, and colbert embeddings in one call
output = model.encode(
    ["Installation guide in English", "Guide d'installation en francais"],
    return_dense=True,
    return_sparse=True,
    return_colbert_vecs=True
)

dense_embeddings = output["dense_vecs"]
sparse_embeddings = output["lexical_weights"]
colbert_embeddings = output["colbert_vecs"]
```

---

## Embedding Fine-Tuning

### When to Fine-Tune

| Scenario | Recommendation |
|----------|----------------|
| Domain-specific jargon (legal, medical) | Fine-tune on domain corpus |
| Low retrieval precision (<80%) | Fine-tune with hard negatives |
| Out-of-distribution queries | Fine-tune with query-doc pairs |
| Cost optimization | Fine-tune smaller model to match larger |

### Fine-Tuning with Sentence Transformers

```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# Prepare training data
train_examples = [
    InputExample(
        texts=["query: how to install", "doc: Installation guide content..."],
        label=1.0  # Relevance score
    ),
    InputExample(
        texts=["query: how to install", "doc: Unrelated content..."],
        label=0.0  # Negative example
    ),
]

# Load base model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Create dataloader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

# Contrastive loss for similarity learning
train_loss = losses.CosineSimilarityLoss(model)

# Fine-tune
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,
    warmup_steps=100,
    output_path="./fine-tuned-model"
)

# Or use Multiple Negatives Ranking Loss (better for retrieval)
train_examples_mnrl = [
    InputExample(texts=["query", "positive_doc", "negative_doc1", "negative_doc2"])
]
train_loss = losses.MultipleNegativesRankingLoss(model)
```

### Hard Negative Mining

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search
import torch

def mine_hard_negatives(
    queries: list[str],
    positives: list[str],
    corpus: list[str],
    model: SentenceTransformer,
    top_k: int = 10
) -> list[InputExample]:
    """Mine hard negatives from corpus for each query-positive pair."""

    query_embeddings = model.encode(queries, convert_to_tensor=True)
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    positive_set = set(positives)

    examples = []
    for i, query in enumerate(queries):
        # Find similar documents that are NOT the positive
        hits = semantic_search(
            query_embeddings[i:i+1],
            corpus_embeddings,
            top_k=top_k + 1
        )[0]

        hard_negatives = [
            corpus[hit["corpus_id"]]
            for hit in hits
            if corpus[hit["corpus_id"]] not in positive_set
        ][:3]  # Top 3 hard negatives

        examples.append(InputExample(
            texts=[query, positives[i]] + hard_negatives
        ))

    return examples
```

---

## Embedding Pipeline Best Practices

### Text Preprocessing

```python
import re
from typing import Callable

def clean_for_embedding(text: str) -> str:
    """Clean text before embedding."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that don't add meaning
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)]', '', text)
    # Truncate to reasonable length (model dependent)
    text = text[:8000]  # Leave room for tokenization expansion
    return text.strip()

def preprocess_for_embedding(
    text: str,
    prefix: str = "",
    max_length: int = 8000
) -> str:
    """Preprocess with optional prefix (for instruction-tuned models)."""
    cleaned = clean_for_embedding(text)
    prefixed = f"{prefix}{cleaned}" if prefix else cleaned
    return prefixed[:max_length]

# BGE-style prefix for queries
query_text = preprocess_for_embedding(
    "how to install",
    prefix="Represent this sentence for searching relevant passages: "
)
```

### Caching Embeddings

```python
import hashlib
import json
from functools import lru_cache
from pathlib import Path

class EmbeddingCache:
    """Disk-based embedding cache."""

    def __init__(self, cache_dir: str = ".embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _hash_key(self, text: str, model: str) -> str:
        content = f"{model}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, text: str, model: str) -> list[float] | None:
        key = self._hash_key(text, model)
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def set(self, text: str, model: str, embedding: list[float]) -> None:
        key = self._hash_key(text, model)
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(embedding))

# Usage
cache = EmbeddingCache()

def get_embedding_cached(text: str, model: str = "text-embedding-3-small") -> list[float]:
    cached = cache.get(text, model)
    if cached:
        return cached

    embedding = get_embedding(text, model)  # Call API
    cache.set(text, model, embedding)
    return embedding
```

### Batching Strategy

```python
from typing import Iterator
import asyncio
from openai import AsyncOpenAI

def batch_texts(texts: list[str], batch_size: int = 100) -> Iterator[list[str]]:
    """Yield batches of texts."""
    for i in range(0, len(texts), batch_size):
        yield texts[i:i + batch_size]

async def get_embeddings_async(
    texts: list[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100,
    max_concurrent: int = 5
) -> list[list[float]]:
    """Async batch embedding with concurrency control."""
    client = AsyncOpenAI()
    semaphore = asyncio.Semaphore(max_concurrent)

    async def embed_batch(batch: list[str]) -> list[list[float]]:
        async with semaphore:
            response = await client.embeddings.create(
                input=batch,
                model=model
            )
            return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]

    batches = list(batch_texts(texts, batch_size))
    results = await asyncio.gather(*[embed_batch(b) for b in batches])

    # Flatten results
    return [emb for batch_result in results for emb in batch_result]
```

---

## Model Selection Flowchart

```
Start
  │
  ├─ Need offline/self-hosted?
  │   └─ Yes → BGE-large or E5-large (open source)
  │
  ├─ Multi-lingual requirement?
  │   └─ Yes → Cohere embed-multilingual-v3 or BGE-M3
  │
  ├─ Code/technical documentation?
  │   └─ Yes → Voyage-code-2
  │
  ├─ Long documents (>8K tokens)?
  │   └─ Yes → Voyage-large-2 or nomic-embed-text
  │
  ├─ Cost is primary concern?
  │   └─ Yes → text-embedding-3-small (reduced dims)
  │
  ├─ Maximum quality needed?
  │   └─ Yes → text-embedding-3-large
  │
  └─ Default → text-embedding-3-small (best balance)
```

---

## Quick Reference

| Task | Recommendation |
|------|----------------|
| Production RAG (English) | text-embedding-3-small/large |
| Multi-lingual | Cohere embed-multilingual-v3 |
| Code retrieval | Voyage-code-2 |
| Self-hosted | BGE-large-en-v1.5 |
| Long documents | Voyage-large-2, nomic-embed-text |
| Prototyping | all-MiniLM-L6-v2 (fast, free) |
| Maximum quality | text-embedding-3-large |
| Cost optimized | text-embedding-3-small @ 512 dims |

## Related Skills

- **RAG Architect** - Vector database integration
- **Python Pro** - Async embedding pipelines
- **ML Pipeline** - Embedding model deployment
- **Fine-Tuning Expert** - Custom embedding training

---

## Reference: Rag Evaluation

# RAG Evaluation

---

## Evaluation Framework Overview

| Framework | Focus | Strengths | Use Case |
|-----------|-------|-----------|----------|
| **RAGAS** | RAG-specific metrics | Faithfulness, relevance | Production RAG evaluation |
| **TruLens** | LLM app observability | Tracing, feedback functions | Debugging and monitoring |
| **LangSmith** | LangChain ecosystem | Traces, datasets, testing | LangChain projects |
| **Custom** | Specific requirements | Full control | Domain-specific needs |

---

## Core Metrics

### Retrieval Metrics

| Metric | Formula | What It Measures |
|--------|---------|------------------|
| **Precision@k** | Relevant in top-k / k | Are retrieved docs relevant? |
| **Recall@k** | Relevant in top-k / Total relevant | Did we get all relevant docs? |
| **MRR** | 1 / Rank of first relevant | How quickly do we find relevant? |
| **NDCG@k** | DCG@k / IDCG@k | Is ranking order correct? |
| **Hit Rate** | Queries with relevant in top-k / Total queries | Binary success rate |

### Generation Metrics

| Metric | What It Measures |
|--------|------------------|
| **Faithfulness** | Is answer grounded in retrieved context? |
| **Answer Relevance** | Does answer address the question? |
| **Context Relevance** | Is retrieved context relevant to question? |
| **Context Utilization** | How much context was actually used? |

---

## Implementing Core Metrics

### Precision, Recall, and Hit Rate

```python
from dataclasses import dataclass
from typing import Set

@dataclass
class RetrievalMetrics:
    precision_at_k: float
    recall_at_k: float
    hit_rate: float
    mrr: float

def calculate_retrieval_metrics(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int
) -> RetrievalMetrics:
    """Calculate core retrieval metrics."""
    top_k = retrieved_ids[:k]
    top_k_set = set(top_k)

    # Precision@k: relevant in top-k / k
    relevant_in_top_k = len(top_k_set & relevant_ids)
    precision = relevant_in_top_k / k if k > 0 else 0

    # Recall@k: relevant in top-k / total relevant
    recall = relevant_in_top_k / len(relevant_ids) if relevant_ids else 0

    # Hit Rate: 1 if any relevant in top-k, else 0
    hit_rate = 1.0 if relevant_in_top_k > 0 else 0.0

    # MRR: 1 / rank of first relevant result
    mrr = 0.0
    for i, doc_id in enumerate(top_k, 1):
        if doc_id in relevant_ids:
            mrr = 1.0 / i
            break

    return RetrievalMetrics(
        precision_at_k=precision,
        recall_at_k=recall,
        hit_rate=hit_rate,
        mrr=mrr
    )

# Usage
retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
relevant = {"doc2", "doc5", "doc7"}  # Ground truth

metrics = calculate_retrieval_metrics(retrieved, relevant, k=5)
print(f"Precision@5: {metrics.precision_at_k:.2f}")  # 2/5 = 0.40
print(f"Recall@5: {metrics.recall_at_k:.2f}")        # 2/3 = 0.67
print(f"MRR: {metrics.mrr:.2f}")                     # 1/2 = 0.50
```

### NDCG (Normalized Discounted Cumulative Gain)

```python
import numpy as np

def dcg_at_k(relevance_scores: list[float], k: int) -> float:
    """Calculate Discounted Cumulative Gain."""
    relevance_scores = np.array(relevance_scores[:k])
    if len(relevance_scores) == 0:
        return 0.0

    # DCG = sum(rel_i / log2(i + 1)) for i in 1..k
    discounts = np.log2(np.arange(2, len(relevance_scores) + 2))
    return np.sum(relevance_scores / discounts)

def ndcg_at_k(
    retrieved_ids: list[str],
    relevance_scores: dict[str, float],
    k: int
) -> float:
    """
    Calculate NDCG@k.
    relevance_scores: dict mapping doc_id to relevance (e.g., 0, 1, 2, 3)
    """
    # Get relevance scores for retrieved docs
    retrieved_relevance = [
        relevance_scores.get(doc_id, 0)
        for doc_id in retrieved_ids[:k]
    ]

    # Calculate DCG for retrieved order
    dcg = dcg_at_k(retrieved_relevance, k)

    # Calculate ideal DCG (perfect ranking)
    ideal_relevance = sorted(relevance_scores.values(), reverse=True)[:k]
    idcg = dcg_at_k(ideal_relevance, k)

    return dcg / idcg if idcg > 0 else 0.0

# Usage with graded relevance
retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
relevance = {
    "doc1": 0,   # Not relevant
    "doc2": 3,   # Highly relevant
    "doc3": 1,   # Somewhat relevant
    "doc5": 2,   # Relevant
    "doc7": 3,   # Highly relevant (not retrieved)
}

ndcg = ndcg_at_k(retrieved, relevance, k=5)
print(f"NDCG@5: {ndcg:.3f}")
```

---

## RAGAS Framework

### Installation and Setup

```python
# pip install ragas

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    context_utilization,
)
from datasets import Dataset

# Prepare evaluation dataset
eval_data = {
    "question": [
        "What is the capital of France?",
        "How do I install Python?"
    ],
    "answer": [
        "The capital of France is Paris.",
        "You can install Python by downloading it from python.org."
    ],
    "contexts": [
        ["Paris is the capital and largest city of France."],
        ["Python can be installed from the official website python.org.",
         "You can also use package managers like brew or apt."]
    ],
    "ground_truth": [
        "Paris is the capital of France.",
        "Install Python from python.org or use a package manager."
    ]
}

dataset = Dataset.from_dict(eval_data)

# Run evaluation
results = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]
)

print(results)
# {'faithfulness': 0.95, 'answer_relevancy': 0.88, ...}
```

### Custom RAGAS Evaluation

```python
from ragas.metrics import Metric
from ragas.llms import LangchainLLM
from langchain_openai import ChatOpenAI

# Use custom LLM
custom_llm = LangchainLLM(llm=ChatOpenAI(model="gpt-4o-mini"))

# Evaluate with custom settings
results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=custom_llm,
    raise_exceptions=False  # Continue on errors
)

# Per-sample scores
for i, row in enumerate(results.to_pandas().itertuples()):
    print(f"Q{i+1}: Faithfulness={row.faithfulness:.2f}, "
          f"Relevancy={row.answer_relevancy:.2f}")
```

### RAGAS Metrics Explained

```python
"""
RAGAS Core Metrics:

1. Faithfulness (0-1):
   - Measures if answer is grounded in context
   - LLM extracts claims from answer, verifies against context
   - High score = answer doesn't hallucinate

2. Answer Relevancy (0-1):
   - Measures if answer addresses the question
   - Generates questions from answer, compares to original
   - High score = answer is on-topic

3. Context Precision (0-1):
   - Measures if retrieved contexts are relevant
   - Ranks contexts by relevance, calculates precision at each rank
   - High score = top contexts are most relevant

4. Context Recall (0-1):
   - Measures if all ground truth info is in context
   - Checks if ground truth sentences are supported by context
   - High score = context contains needed information
"""

# Debugging low scores
def diagnose_ragas_scores(results_df):
    """Identify problematic samples."""
    issues = []

    for idx, row in results_df.iterrows():
        if row.get('faithfulness', 1) < 0.5:
            issues.append({
                "index": idx,
                "issue": "Low faithfulness - answer may contain hallucinations",
                "question": row['question'],
                "answer": row['answer'][:200]
            })

        if row.get('context_recall', 1) < 0.5:
            issues.append({
                "index": idx,
                "issue": "Low context recall - retrieval missing relevant docs",
                "question": row['question']
            })

    return issues
```

---

## TruLens Evaluation

### Setup and Basic Usage

```python
# pip install trulens-eval

from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback import Groundedness
from trulens_eval.feedback.provider import OpenAI as fOpenAI

# Initialize TruLens
tru = Tru()

# Create feedback provider
provider = fOpenAI()

# Define feedback functions
f_groundedness = Feedback(
    provider.groundedness_measure_with_cot_reasons,
    name="Groundedness"
).on(
    TruChain.select_context().node.text  # Retrieved context
).on_output()

f_relevance = Feedback(
    provider.relevance_with_cot_reasons,
    name="Answer Relevance"
).on_input().on_output()

f_context_relevance = Feedback(
    provider.context_relevance_with_cot_reasons,
    name="Context Relevance"
).on_input().on(
    TruChain.select_context().node.text
)

# Wrap your RAG chain
from langchain.chains import RetrievalQA

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever()
)

tru_recorder = TruChain(
    rag_chain,
    app_id="rag-v1",
    feedbacks=[f_groundedness, f_relevance, f_context_relevance]
)

# Run with recording
with tru_recorder as recording:
    response = rag_chain.invoke({"query": "How do I configure authentication?"})

# View results
tru.run_dashboard()  # Opens web UI
# Or get programmatically
records = tru.get_records_and_feedback(app_ids=["rag-v1"])
```

### Custom Feedback Functions

```python
from trulens_eval import Feedback, Select

def custom_citation_check(response: str, context: str) -> float:
    """Check if response cites sources from context."""
    # Extract citations from response (e.g., [1], [Source: X])
    import re
    citations = re.findall(r'\[[\d\w\s:]+\]', response)

    if not citations:
        return 0.0  # No citations

    # Verify citations reference actual context
    valid_citations = sum(1 for c in citations if c.lower() in context.lower())
    return valid_citations / len(citations)

f_citation = Feedback(
    custom_citation_check,
    name="Citation Accuracy"
).on_output().on(Select.RecordCalls.retriever.get_relevant_documents.rets.page_content)
```

---

## Building Custom Evaluation Pipelines

### LLM-as-Judge Evaluation

```python
from openai import OpenAI
from dataclasses import dataclass
from typing import Literal

client = OpenAI()

@dataclass
class EvalResult:
    score: float
    reasoning: str
    criteria: str

def evaluate_with_llm(
    question: str,
    answer: str,
    context: str,
    criteria: Literal["faithfulness", "relevance", "completeness"]
) -> EvalResult:
    """Use LLM as judge for evaluation."""

    criteria_prompts = {
        "faithfulness": """
            Evaluate if the answer is fully supported by the provided context.
            Score 1.0 if every claim in the answer is verifiable from context.
            Score 0.5 if most claims are supported but some are not.
            Score 0.0 if the answer contains significant unsupported claims.
        """,
        "relevance": """
            Evaluate if the answer directly addresses the question.
            Score 1.0 if the answer fully addresses the question.
            Score 0.5 if the answer partially addresses the question.
            Score 0.0 if the answer is off-topic or doesn't address the question.
        """,
        "completeness": """
            Evaluate if the answer covers all aspects of the question.
            Score 1.0 if the answer is comprehensive and complete.
            Score 0.5 if the answer covers main points but misses details.
            Score 0.0 if the answer is significantly incomplete.
        """
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""You are an expert evaluator for RAG systems.
                {criteria_prompts[criteria]}

                Respond in JSON format:
                {{"score": <0.0-1.0>, "reasoning": "<explanation>"}}"""
            },
            {
                "role": "user",
                "content": f"""Question: {question}

Context:
{context}

Answer: {answer}

Evaluate the answer for {criteria}:"""
            }
        ],
        response_format={"type": "json_object"}
    )

    import json
    result = json.loads(response.choices[0].message.content)

    return EvalResult(
        score=result["score"],
        reasoning=result["reasoning"],
        criteria=criteria
    )

# Usage
eval_result = evaluate_with_llm(
    question="How do I configure OAuth2?",
    answer="Configure OAuth2 by setting client_id and client_secret in config.yaml.",
    context="OAuth2 configuration requires client_id, client_secret, and redirect_uri in config.yaml.",
    criteria="faithfulness"
)
print(f"Faithfulness: {eval_result.score:.2f}")
print(f"Reasoning: {eval_result.reasoning}")
```

### Batch Evaluation Pipeline

```python
import asyncio
from tqdm.asyncio import tqdm_asyncio

async def evaluate_batch(
    test_cases: list[dict],
    retriever,
    generator,
    metrics: list[str] = ["precision", "faithfulness", "relevance"]
) -> dict:
    """Run batch evaluation on test cases."""

    results = {
        "per_sample": [],
        "aggregated": {}
    }

    async def evaluate_single(case: dict) -> dict:
        # Retrieve
        retrieved = await retriever.aretrieve(case["question"])
        retrieved_ids = [r.id for r in retrieved]

        # Generate
        answer = await generator.agenerate(
            question=case["question"],
            context=[r.text for r in retrieved]
        )

        # Calculate metrics
        sample_result = {
            "question": case["question"],
            "answer": answer,
            "retrieved_ids": retrieved_ids
        }

        if "relevant_ids" in case and "precision" in metrics:
            retrieval_metrics = calculate_retrieval_metrics(
                retrieved_ids,
                set(case["relevant_ids"]),
                k=5
            )
            sample_result["precision@5"] = retrieval_metrics.precision_at_k
            sample_result["recall@5"] = retrieval_metrics.recall_at_k

        if "faithfulness" in metrics:
            faith_eval = evaluate_with_llm(
                case["question"],
                answer,
                "\n".join([r.text for r in retrieved]),
                "faithfulness"
            )
            sample_result["faithfulness"] = faith_eval.score

        return sample_result

    # Run evaluations concurrently
    tasks = [evaluate_single(case) for case in test_cases]
    results["per_sample"] = await tqdm_asyncio.gather(*tasks)

    # Aggregate results
    for metric in ["precision@5", "recall@5", "faithfulness"]:
        scores = [r.get(metric) for r in results["per_sample"] if r.get(metric) is not None]
        if scores:
            results["aggregated"][metric] = {
                "mean": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores)
            }

    return results
```

---

## Debugging Poor Retrieval

### Retrieval Diagnostics

```python
def diagnose_retrieval(
    query: str,
    retrieved_docs: list,
    expected_docs: list,
    embedding_model
) -> dict:
    """Diagnose why retrieval might be failing."""

    query_embedding = embedding_model.encode(query)
    retrieved_embeddings = [embedding_model.encode(d) for d in retrieved_docs]
    expected_embeddings = [embedding_model.encode(d) for d in expected_docs]

    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    diagnosis = {
        "query": query,
        "issues": []
    }

    # Check query-document similarity
    for i, (doc, emb) in enumerate(zip(retrieved_docs, retrieved_embeddings)):
        sim = cosine_similarity([query_embedding], [emb])[0][0]
        if sim < 0.5:
            diagnosis["issues"].append({
                "type": "low_similarity",
                "doc_index": i,
                "similarity": float(sim),
                "doc_preview": doc[:100]
            })

    # Check if expected docs would score higher
    for i, (doc, emb) in enumerate(zip(expected_docs, expected_embeddings)):
        sim = cosine_similarity([query_embedding], [emb])[0][0]
        retrieved_max_sim = max(
            cosine_similarity([query_embedding], [e])[0][0]
            for e in retrieved_embeddings
        )

        if sim > retrieved_max_sim:
            diagnosis["issues"].append({
                "type": "missed_better_doc",
                "expected_doc_index": i,
                "expected_sim": float(sim),
                "best_retrieved_sim": float(retrieved_max_sim),
                "doc_preview": doc[:100]
            })

    # Check for vocabulary mismatch
    query_terms = set(query.lower().split())
    for i, doc in enumerate(retrieved_docs):
        doc_terms = set(doc.lower().split())
        overlap = query_terms & doc_terms
        if len(overlap) < len(query_terms) * 0.3:
            diagnosis["issues"].append({
                "type": "vocabulary_mismatch",
                "doc_index": i,
                "query_terms": list(query_terms),
                "overlapping_terms": list(overlap)
            })

    return diagnosis

# Usage
diagnosis = diagnose_retrieval(
    query="How to configure OAuth authentication",
    retrieved_docs=retrieved_texts,
    expected_docs=expected_texts,
    embedding_model=sentence_transformer
)

for issue in diagnosis["issues"]:
    print(f"Issue: {issue['type']}")
    print(f"Details: {issue}")
```

### Query Analysis

```python
def analyze_query_performance(
    query_logs: list[dict],
    threshold_precision: float = 0.6
) -> dict:
    """Analyze query patterns to find systematic issues."""

    analysis = {
        "total_queries": len(query_logs),
        "low_performing": [],
        "patterns": {}
    }

    for log in query_logs:
        if log.get("precision@5", 1.0) < threshold_precision:
            analysis["low_performing"].append(log)

    # Analyze low-performing queries
    if analysis["low_performing"]:
        # Check for common patterns
        low_perf_queries = [l["query"] for l in analysis["low_performing"]]

        # Query length analysis
        avg_length = sum(len(q.split()) for q in low_perf_queries) / len(low_perf_queries)
        analysis["patterns"]["avg_low_perf_query_length"] = avg_length

        # Common terms in failing queries
        from collections import Counter
        all_terms = []
        for q in low_perf_queries:
            all_terms.extend(q.lower().split())
        analysis["patterns"]["common_failing_terms"] = Counter(all_terms).most_common(10)

        # Question type analysis
        question_words = ["how", "what", "why", "when", "where", "who"]
        question_types = Counter()
        for q in low_perf_queries:
            for qw in question_words:
                if q.lower().startswith(qw):
                    question_types[qw] += 1
                    break
            else:
                question_types["other"] += 1
        analysis["patterns"]["failing_question_types"] = dict(question_types)

    return analysis
```

---

## Continuous Monitoring

### Production Metrics Dashboard

```python
import time
from dataclasses import dataclass, field
from collections import deque
from threading import Lock

@dataclass
class RAGMetricsCollector:
    """Collect and track RAG metrics in production."""

    window_size: int = 1000
    _latencies: deque = field(default_factory=lambda: deque(maxlen=1000))
    _retrieval_scores: deque = field(default_factory=lambda: deque(maxlen=1000))
    _generation_scores: deque = field(default_factory=lambda: deque(maxlen=1000))
    _lock: Lock = field(default_factory=Lock)

    def record_query(
        self,
        latency_ms: float,
        retrieval_score: float | None = None,
        generation_score: float | None = None
    ):
        """Record metrics for a single query."""
        with self._lock:
            self._latencies.append(latency_ms)
            if retrieval_score is not None:
                self._retrieval_scores.append(retrieval_score)
            if generation_score is not None:
                self._generation_scores.append(generation_score)

    def get_summary(self) -> dict:
        """Get current metrics summary."""
        with self._lock:
            import numpy as np

            summary = {
                "queries_in_window": len(self._latencies),
                "latency": {
                    "p50": np.percentile(self._latencies, 50) if self._latencies else 0,
                    "p95": np.percentile(self._latencies, 95) if self._latencies else 0,
                    "p99": np.percentile(self._latencies, 99) if self._latencies else 0,
                },
                "retrieval_score": {
                    "mean": np.mean(self._retrieval_scores) if self._retrieval_scores else 0,
                    "std": np.std(self._retrieval_scores) if self._retrieval_scores else 0,
                },
                "generation_score": {
                    "mean": np.mean(self._generation_scores) if self._generation_scores else 0,
                    "std": np.std(self._generation_scores) if self._generation_scores else 0,
                }
            }

            return summary

# Usage
metrics = RAGMetricsCollector()

# In your RAG endpoint
start = time.time()
response = rag_pipeline.query(question)
latency = (time.time() - start) * 1000

metrics.record_query(
    latency_ms=latency,
    retrieval_score=response.get("retrieval_score"),
    generation_score=response.get("generation_score")
)

# Periodically check
print(metrics.get_summary())
```

### Alerting on Quality Degradation

```python
class RAGQualityMonitor:
    """Monitor RAG quality and alert on degradation."""

    def __init__(
        self,
        baseline_precision: float = 0.8,
        alert_threshold: float = 0.1,  # Alert if drops by 10%
        window_size: int = 100
    ):
        self.baseline = baseline_precision
        self.threshold = alert_threshold
        self.window_size = window_size
        self.recent_scores = deque(maxlen=window_size)

    def record_score(self, precision: float) -> dict | None:
        """Record score and return alert if quality degraded."""
        self.recent_scores.append(precision)

        if len(self.recent_scores) < self.window_size // 2:
            return None  # Not enough data

        current_mean = sum(self.recent_scores) / len(self.recent_scores)
        degradation = self.baseline - current_mean

        if degradation > self.threshold:
            return {
                "alert": "QUALITY_DEGRADATION",
                "baseline": self.baseline,
                "current": current_mean,
                "degradation": degradation,
                "window_size": len(self.recent_scores)
            }

        return None

# Usage
monitor = RAGQualityMonitor(baseline_precision=0.85)

for query_result in production_queries:
    alert = monitor.record_score(query_result["precision@5"])
    if alert:
        send_alert(alert)  # Slack, PagerDuty, etc.
```

---

## Evaluation Best Practices

| Practice | Description |
|----------|-------------|
| **Golden test set** | Maintain 50-200 curated Q&A pairs with ground truth |
| **Stratified sampling** | Include diverse query types in test set |
| **Human baselines** | Compare LLM judges against human annotators |
| **Version control** | Track evaluation results alongside model versions |
| **Regular re-evaluation** | Re-run golden tests on every retrieval change |
| **A/B testing** | Compare new retrieval strategies on live traffic |

---

## Quick Reference

| Goal | Metric | Target |
|------|--------|--------|
| Are docs relevant? | Precision@5 | > 0.7 |
| Did we get all docs? | Recall@5 | > 0.8 |
| Is ranking good? | NDCG@5 | > 0.7 |
| Is answer grounded? | Faithfulness | > 0.9 |
| Does answer fit question? | Answer Relevance | > 0.8 |
| Is context useful? | Context Relevance | > 0.7 |

| Framework | Best For |
|-----------|----------|
| RAGAS | Quick RAG-specific evaluation |
| TruLens | Production monitoring and tracing |
| Custom LLM-judge | Domain-specific criteria |
| Manual annotation | Ground truth creation |

## Related Skills

- **RAG Architect** - System design
- **ML Pipeline** - Evaluation automation
- **Data Scientist** - Statistical analysis
- **Monitoring Expert** - Production observability

---

## Reference: Retrieval Optimization

# Retrieval Optimization

---

## Optimization Techniques Overview

| Technique | Impact | Complexity | When to Use |
|-----------|--------|------------|-------------|
| **Hybrid Search** | High | Medium | Always for production |
| **Reranking** | High | Low | Top-k refinement |
| **Query Expansion** | Medium | Medium | Ambiguous queries |
| **HyDE** | Medium-High | Medium | Concept-heavy retrieval |
| **Metadata Filtering** | High | Low | Multi-tenant, categorical |
| **Query Decomposition** | Medium | High | Complex questions |
| **Contextual Compression** | Medium | Medium | Long retrieved chunks |

---

## Hybrid Search (Vector + Keyword)

### Reciprocal Rank Fusion (RRF)

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class SearchResult:
    id: str
    text: str
    score: float
    source: str  # "vector" or "keyword"

def reciprocal_rank_fusion(
    vector_results: list[SearchResult],
    keyword_results: list[SearchResult],
    k: int = 60,
    vector_weight: float = 0.5
) -> list[SearchResult]:
    """
    Combine vector and keyword results using RRF.
    k is a constant that reduces the impact of high rankings (typically 60).
    """
    scores: dict[str, float] = {}
    docs: dict[str, SearchResult] = {}

    # Score vector results
    for rank, result in enumerate(vector_results, 1):
        rrf_score = vector_weight * (1 / (k + rank))
        scores[result.id] = scores.get(result.id, 0) + rrf_score
        docs[result.id] = result

    # Score keyword results
    keyword_weight = 1 - vector_weight
    for rank, result in enumerate(keyword_results, 1):
        rrf_score = keyword_weight * (1 / (k + rank))
        scores[result.id] = scores.get(result.id, 0) + rrf_score
        if result.id not in docs:
            docs[result.id] = result

    # Sort by combined score
    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

    return [
        SearchResult(
            id=doc_id,
            text=docs[doc_id].text,
            score=scores[doc_id],
            source="hybrid"
        )
        for doc_id in sorted_ids
    ]

# Usage
hybrid_results = reciprocal_rank_fusion(
    vector_results=vector_search(query_embedding, top_k=20),
    keyword_results=bm25_search(query_text, top_k=20),
    vector_weight=0.6  # Favor semantic similarity
)
```

### BM25 + Vector with Weaviate

```python
from weaviate.classes.query import HybridFusion

collection = client.collections.get("Documents")

# Hybrid search with configurable fusion
results = collection.query.hybrid(
    query="how to configure authentication",
    alpha=0.5,  # 0 = pure BM25, 1 = pure vector
    fusion_type=HybridFusion.RELATIVE_SCORE,  # or RANKED
    limit=10,
    return_metadata=["score", "explain_score"]
)

# Iterate results
for obj in results.objects:
    print(f"Score: {obj.metadata.score}")
    print(f"Explanation: {obj.metadata.explain_score}")
    print(f"Text: {obj.properties['content'][:200]}")
```

### Pinecone Sparse-Dense

```python
from pinecone_text.sparse import BM25Encoder

# Train BM25 encoder on your corpus
bm25 = BM25Encoder()
bm25.fit(corpus_documents)

# Encode query for hybrid search
sparse_vector = bm25.encode_queries(query_text)
dense_vector = get_embedding(query_text)

# Search with both vectors
results = index.query(
    vector=dense_vector,
    sparse_vector=sparse_vector,
    top_k=10,
    include_metadata=True
)
```

---

## Reranking

### Cohere Rerank

```python
import cohere

co = cohere.Client(api_key="your-api-key")

def rerank_results(
    query: str,
    documents: list[str],
    top_n: int = 5,
    model: str = "rerank-english-v3.0"
) -> list[dict]:
    """Rerank documents using Cohere."""
    response = co.rerank(
        query=query,
        documents=documents,
        top_n=top_n,
        model=model,
        return_documents=True
    )

    return [
        {
            "text": result.document.text,
            "relevance_score": result.relevance_score,
            "original_index": result.index
        }
        for result in response.results
    ]

# Pipeline: retrieve more, rerank fewer
initial_results = vector_search(query_embedding, top_k=50)
documents = [r.text for r in initial_results]

reranked = rerank_results(
    query="how to configure OAuth2 authentication",
    documents=documents,
    top_n=5
)

# Use top 5 reranked docs for LLM context
context = "\n\n".join([r["text"] for r in reranked])
```

### Cross-Encoder Reranking (Open Source)

```python
from sentence_transformers import CrossEncoder

class Reranker:
    """Rerank using cross-encoder model."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int = 5
    ) -> list[tuple[str, float]]:
        """Rerank documents by relevance to query."""
        # Create query-document pairs
        pairs = [[query, doc] for doc in documents]

        # Get relevance scores
        scores = self.model.predict(pairs)

        # Sort by score
        doc_scores = list(zip(documents, scores))
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        return doc_scores[:top_k]

# Usage
reranker = Reranker()
top_docs = reranker.rerank(
    query="OAuth2 setup guide",
    documents=retrieved_documents,
    top_k=5
)
```

### ColBERT-Style Late Interaction

```python
from colbert import Searcher
from colbert.infra import Run, RunConfig

# Setup ColBERT index (one-time)
with Run().context(RunConfig(nranks=1)):
    searcher = Searcher(index="path/to/colbert_index")

# Search with late interaction scoring
results = searcher.search(
    query="how to configure authentication",
    k=10
)

# Results include token-level matching scores
for passage_id, rank, score in zip(*results):
    print(f"Rank {rank}: Doc {passage_id}, Score: {score}")
```

---

## Query Expansion

### LLM-Based Query Expansion

```python
from openai import OpenAI

client = OpenAI()

def expand_query(query: str, num_expansions: int = 3) -> list[str]:
    """Generate query variations using LLM."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""Generate {num_expansions} alternative search queries
                that would help find relevant documents for the user's question.
                Include:
                - Synonym variations
                - More specific versions
                - More general versions
                Return as JSON array of strings."""
            },
            {
                "role": "user",
                "content": query
            }
        ],
        response_format={"type": "json_object"}
    )

    import json
    result = json.loads(response.choices[0].message.content)
    return [query] + result.get("queries", [])

# Usage
original_query = "how to fix memory leak"
expanded_queries = expand_query(original_query)
# ["how to fix memory leak", "debug memory issues", "memory leak detection",
#  "troubleshoot high memory usage"]

# Search with all queries and merge results
all_results = []
for q in expanded_queries:
    results = vector_search(get_embedding(q), top_k=10)
    all_results.extend(results)

# Deduplicate and rank by frequency
deduped = deduplicate_by_id(all_results)
```

### Query Rewriting

```python
def rewrite_query_for_retrieval(
    conversational_query: str,
    chat_history: list[dict]
) -> str:
    """Rewrite conversational query to standalone search query."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Rewrite the user's question as a standalone search query.
                Include relevant context from chat history.
                Output only the rewritten query, nothing else."""
            },
            {
                "role": "user",
                "content": f"""Chat history:
{format_chat_history(chat_history)}

User's question: {conversational_query}

Rewritten search query:"""
            }
        ],
        max_tokens=100
    )

    return response.choices[0].message.content.strip()

# Example
history = [
    {"role": "user", "content": "Tell me about Python web frameworks"},
    {"role": "assistant", "content": "Popular Python web frameworks include Django, Flask, and FastAPI..."}
]
query = "Which one is best for APIs?"

rewritten = rewrite_query_for_retrieval(query, history)
# Output: "Best Python web framework for building REST APIs: Django vs Flask vs FastAPI"
```

---

## HyDE (Hypothetical Document Embeddings)

```python
def hyde_search(
    query: str,
    vector_store,
    embedding_model,
    top_k: int = 10
) -> list[SearchResult]:
    """
    Generate hypothetical answer, embed it, and search.
    Aligns query embedding space with document embedding space.
    """
    # Generate hypothetical document
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Write a passage that would answer the user's question.
                Write as if you're an expert documentation author.
                Be specific and technical. About 100-200 words."""
            },
            {
                "role": "user",
                "content": query
            }
        ],
        max_tokens=300
    )

    hypothetical_doc = response.choices[0].message.content

    # Embed hypothetical document
    hyde_embedding = embedding_model.encode(hypothetical_doc)

    # Search with hypothetical doc embedding
    results = vector_store.search(
        vector=hyde_embedding,
        top_k=top_k
    )

    return results

# Usage
results = hyde_search(
    query="How do I handle rate limiting in my API?",
    vector_store=qdrant_client,
    embedding_model=sentence_transformer
)
```

### Multi-HyDE (Multiple Perspectives)

```python
def multi_hyde_search(
    query: str,
    vector_store,
    embedding_model,
    num_hypotheticals: int = 3,
    top_k: int = 10
) -> list[SearchResult]:
    """Generate multiple hypothetical docs for diverse retrieval."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""Generate {num_hypotheticals} different passages
                that could answer the question from different angles:
                1. Technical deep-dive
                2. Beginner-friendly explanation
                3. Best practices summary

                Return as JSON with "passages" array."""
            },
            {
                "role": "user",
                "content": query
            }
        ],
        response_format={"type": "json_object"}
    )

    import json
    passages = json.loads(response.choices[0].message.content)["passages"]

    # Embed all hypotheticals
    all_results = []
    for passage in passages:
        embedding = embedding_model.encode(passage)
        results = vector_store.search(vector=embedding, top_k=top_k)
        all_results.extend(results)

    # Deduplicate and combine scores
    return deduplicate_and_merge(all_results)
```

---

## Metadata Filtering

### Multi-Tenant Filtering

```python
class MultiTenantRetriever:
    """Retriever with mandatory tenant isolation."""

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def search(
        self,
        query_embedding: list[float],
        tenant_id: str,
        top_k: int = 10,
        additional_filters: dict | None = None
    ) -> list[SearchResult]:
        """Search with mandatory tenant filter."""
        # Build filter - tenant is always required
        filters = {"tenant_id": {"$eq": tenant_id}}

        if additional_filters:
            filters = {"$and": [filters, additional_filters]}

        return self.vector_store.search(
            vector=query_embedding,
            filter=filters,
            top_k=top_k
        )

# Usage
retriever = MultiTenantRetriever(pinecone_index)
results = retriever.search(
    query_embedding=embedding,
    tenant_id="acme-corp",
    additional_filters={
        "doc_type": {"$in": ["manual", "faq"]},
        "published": {"$eq": True}
    }
)
```

### Temporal Filtering

```python
from datetime import datetime, timedelta

def search_recent_documents(
    query_embedding: list[float],
    vector_store,
    days_back: int = 30,
    top_k: int = 10
) -> list[SearchResult]:
    """Search documents updated within time window."""
    cutoff_date = datetime.utcnow() - timedelta(days=days_back)

    return vector_store.search(
        vector=query_embedding,
        filter={
            "updated_at": {"$gte": cutoff_date.isoformat()}
        },
        top_k=top_k
    )

def search_with_recency_boost(
    query_embedding: list[float],
    vector_store,
    recency_weight: float = 0.2,
    top_k: int = 10
) -> list[SearchResult]:
    """Boost recent documents in ranking."""
    # Get more results to apply post-filtering
    results = vector_store.search(
        vector=query_embedding,
        top_k=top_k * 3
    )

    now = datetime.utcnow()

    def compute_boosted_score(result):
        doc_date = datetime.fromisoformat(result.metadata["updated_at"])
        days_old = (now - doc_date).days
        recency_score = max(0, 1 - (days_old / 365))  # Decay over 1 year
        return result.score * (1 - recency_weight) + recency_score * recency_weight

    # Rerank with recency boost
    for result in results:
        result.boosted_score = compute_boosted_score(result)

    results.sort(key=lambda x: x.boosted_score, reverse=True)
    return results[:top_k]
```

---

## Query Decomposition

```python
def decompose_complex_query(query: str) -> list[str]:
    """Break complex query into sub-questions."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Break this complex question into simpler sub-questions
                that can be answered independently. Each sub-question should be
                searchable. Return as JSON with "questions" array."""
            },
            {
                "role": "user",
                "content": query
            }
        ],
        response_format={"type": "json_object"}
    )

    import json
    result = json.loads(response.choices[0].message.content)
    return result.get("questions", [query])

def search_with_decomposition(
    complex_query: str,
    vector_store,
    embedding_model,
    top_k_per_subquery: int = 5
) -> dict:
    """Search for each sub-question and aggregate results."""
    sub_questions = decompose_complex_query(complex_query)

    aggregated_results = {
        "sub_questions": [],
        "all_documents": []
    }

    seen_doc_ids = set()

    for sub_q in sub_questions:
        embedding = embedding_model.encode(sub_q)
        results = vector_store.search(vector=embedding, top_k=top_k_per_subquery)

        sub_q_results = []
        for r in results:
            if r.id not in seen_doc_ids:
                seen_doc_ids.add(r.id)
                sub_q_results.append(r)
                aggregated_results["all_documents"].append(r)

        aggregated_results["sub_questions"].append({
            "question": sub_q,
            "results": sub_q_results
        })

    return aggregated_results

# Usage
complex_q = "Compare the security features of OAuth2 and API keys, and explain when to use each"
results = search_with_decomposition(complex_q, vector_store, embedding_model)
```

---

## Contextual Compression

```python
def compress_retrieved_context(
    query: str,
    documents: list[str],
    max_tokens: int = 2000
) -> str:
    """Extract only query-relevant parts from documents."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""Extract only the parts of these documents that are
                relevant to answering the user's question.
                Remove irrelevant information.
                Keep extracted content under {max_tokens} tokens.
                Maintain source attribution."""
            },
            {
                "role": "user",
                "content": f"""Question: {query}

Documents:
{chr(10).join([f'[Doc {i+1}]: {doc}' for i, doc in enumerate(documents)])}

Extracted relevant content:"""
            }
        ],
        max_tokens=max_tokens
    )

    return response.choices[0].message.content
```

### Extractive Compression with Cross-Encoder

```python
from sentence_transformers import CrossEncoder

def extractive_compress(
    query: str,
    document: str,
    cross_encoder: CrossEncoder,
    top_k_sentences: int = 5
) -> str:
    """Extract most relevant sentences from document."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', document)

    if len(sentences) <= top_k_sentences:
        return document

    # Score each sentence
    pairs = [[query, sent] for sent in sentences]
    scores = cross_encoder.predict(pairs)

    # Get top sentences in original order
    scored_sentences = list(zip(range(len(sentences)), sentences, scores))
    top_sentences = sorted(scored_sentences, key=lambda x: x[2], reverse=True)[:top_k_sentences]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Restore order

    return " ".join([s[1] for s in top_sentences])
```

---

## Complete Optimized Pipeline

```python
class OptimizedRetriever:
    """Production retrieval pipeline with all optimizations."""

    def __init__(
        self,
        vector_store,
        embedding_model,
        reranker,
        bm25_index
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.reranker = reranker
        self.bm25_index = bm25_index

    async def retrieve(
        self,
        query: str,
        tenant_id: str,
        top_k: int = 5,
        use_hyde: bool = False,
        use_query_expansion: bool = True
    ) -> list[dict]:
        """Full optimized retrieval pipeline."""
        # Step 1: Query preprocessing
        processed_query = self._preprocess_query(query)

        # Step 2: Optional HyDE
        if use_hyde:
            query_embedding = await self._hyde_embed(processed_query)
        else:
            query_embedding = self.embedding_model.encode(processed_query)

        # Step 3: Hybrid search (vector + BM25)
        vector_results = self.vector_store.search(
            vector=query_embedding,
            filter={"tenant_id": tenant_id},
            top_k=50
        )
        bm25_results = self.bm25_index.search(processed_query, top_k=50)

        # Step 4: Merge with RRF
        merged = reciprocal_rank_fusion(
            vector_results,
            bm25_results,
            vector_weight=0.6
        )[:30]

        # Step 5: Optional query expansion
        if use_query_expansion:
            expanded_queries = await self._expand_query(processed_query)
            for exp_query in expanded_queries[1:]:  # Skip original
                exp_embedding = self.embedding_model.encode(exp_query)
                exp_results = self.vector_store.search(
                    vector=exp_embedding,
                    filter={"tenant_id": tenant_id},
                    top_k=10
                )
                merged.extend(exp_results)
            merged = deduplicate_by_id(merged)[:30]

        # Step 6: Rerank
        documents = [r.text for r in merged]
        reranked = self.reranker.rerank(
            query=processed_query,
            documents=documents,
            top_k=top_k
        )

        return [
            {
                "text": doc,
                "score": score,
                "metadata": merged[i].metadata
            }
            for i, (doc, score) in enumerate(reranked)
        ]

    def _preprocess_query(self, query: str) -> str:
        """Clean and normalize query."""
        import re
        query = re.sub(r'\s+', ' ', query).strip()
        return query

    async def _hyde_embed(self, query: str) -> list[float]:
        """Generate hypothetical document and embed."""
        # Implementation from HyDE section
        pass

    async def _expand_query(self, query: str) -> list[str]:
        """Expand query with variations."""
        # Implementation from Query Expansion section
        pass
```

---

## Performance Benchmarks

| Technique | Latency Impact | Quality Impact | Cost Impact |
|-----------|----------------|----------------|-------------|
| Vector only | Baseline | Baseline | Baseline |
| + BM25 hybrid | +10-20ms | +5-15% precision | Minimal |
| + Reranking | +50-100ms | +10-20% precision | +$0.001/query |
| + Query expansion | +100-200ms | +5-10% recall | +$0.002/query |
| + HyDE | +200-500ms | +10-25% precision | +$0.003/query |

---

## Quick Reference

| Goal | Technique | Implementation |
|------|-----------|----------------|
| Improve precision | Reranking | Cross-encoder or Cohere |
| Improve recall | Query expansion | LLM-generated variations |
| Handle synonyms | Hybrid search | BM25 + vector with RRF |
| Concept search | HyDE | Hypothetical doc embedding |
| Multi-tenant | Metadata filter | Mandatory tenant_id |
| Fresh content | Temporal filter | Date range queries |
| Complex questions | Decomposition | Sub-question retrieval |

## Related Skills

- **RAG Architect** - System design and architecture
- **NLP Engineer** - Query understanding
- **Python Pro** - Async implementation
- **ML Pipeline** - Model serving for rerankers

---

## Reference: Vector Databases

# Vector Databases

---

## Database Comparison Matrix

| Feature | Pinecone | Weaviate | Qdrant | Chroma | pgvector |
|---------|----------|----------|--------|--------|----------|
| **Hosting** | Managed only | Managed + Self-hosted | Managed + Self-hosted | Self-hosted (cloud beta) | Self-hosted |
| **Hybrid Search** | Yes (sparse-dense) | Yes (BM25 + vector) | Yes (sparse vectors) | Limited | Manual (+ pg_trgm) |
| **Filtering** | Excellent | Excellent | Excellent | Basic | SQL-native |
| **Max Dimensions** | 20,000 | Unlimited | 65,535 | Unlimited | 2,000 |
| **Pricing Model** | Per-vector/query | Per-node | Per-node | Free (OSS) | Free (extension) |
| **Multi-tenancy** | Namespaces | Multi-tenant class | Collections + payloads | Collections | Schema/RLS |
| **Best For** | Enterprise SaaS | Semantic apps | High-performance | Prototyping | Postgres shops |

## When to Use Each

### Pinecone
```
Best For:
- Enterprise RAG with strict SLAs
- Teams wanting zero infrastructure management
- Applications needing sparse-dense hybrid search
- High-volume production with predictable costs

When to Avoid:
- Cost-sensitive projects (expensive at scale)
- Need for self-hosting or data residency
- Complex filtering requirements beyond metadata
- Wanting to avoid vendor lock-in
```

### Weaviate
```
Best For:
- Semantic search with built-in vectorization
- Multi-modal (text, image) applications
- GraphQL-native teams
- Hybrid BM25 + vector search requirements

When to Avoid:
- Simple embedding storage only
- Memory-constrained environments
- Teams unfamiliar with GraphQL
```

### Qdrant
```
Best For:
- High-performance, low-latency requirements
- Complex filtering with payload indexes
- Rust/performance-focused teams
- Self-hosted with full control

When to Avoid:
- Teams wanting fully managed simplicity
- GraphQL preference (REST/gRPC only)
```

### Chroma
```
Best For:
- Local development and prototyping
- LangChain/LlamaIndex integration
- Simple RAG proof-of-concepts
- Educational projects

When to Avoid:
- Production workloads at scale
- Multi-tenant applications
- High availability requirements
```

### pgvector
```
Best For:
- Existing PostgreSQL infrastructure
- Transactional + vector in same DB
- SQL-native teams
- Cost optimization (no new infra)

When to Avoid:
- Vectors > 2000 dimensions
- Billions of vectors (scaling limits)
- Sub-millisecond latency requirements
```

---

## Pinecone Setup

```python
from pinecone import Pinecone, ServerlessSpec

# Initialize client
pc = Pinecone(api_key="your-api-key")

# Create index with serverless
pc.create_index(
    name="rag-index",
    dimension=1536,  # OpenAI ada-002
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Get index reference
index = pc.Index("rag-index")

# Upsert vectors with metadata
index.upsert(
    vectors=[
        {
            "id": "doc-1",
            "values": embedding_vector,
            "metadata": {
                "source": "manual.pdf",
                "page": 42,
                "section": "installation",
                "tenant_id": "acme-corp"
            }
        }
    ],
    namespace="production"
)

# Query with metadata filter
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True,
    namespace="production",
    filter={
        "tenant_id": {"$eq": "acme-corp"},
        "section": {"$in": ["installation", "setup"]}
    }
)

# Hybrid search (sparse-dense)
from pinecone_text.sparse import BM25Encoder

bm25 = BM25Encoder()
bm25.fit(corpus)  # Fit on your documents

results = index.query(
    vector=dense_embedding,
    sparse_vector=bm25.encode_queries(query_text),
    top_k=10,
    alpha=0.5  # Balance dense vs sparse
)
```

---

## Weaviate Setup

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

# Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url="https://your-cluster.weaviate.network",
    auth_credentials=weaviate.auth.AuthApiKey("your-api-key")
)

# Or self-hosted
client = weaviate.connect_to_local(
    host="localhost",
    port=8080
)

# Create collection with vectorizer
client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(
        model="text-embedding-3-small"
    ),
    properties=[
        Property(name="content", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
        Property(name="page", data_type=DataType.INT),
        Property(name="tenant_id", data_type=DataType.TEXT, index_filterable=True)
    ]
)

# Insert with auto-vectorization
documents = client.collections.get("Document")
documents.data.insert(
    properties={
        "content": "Installation guide content...",
        "source": "manual.pdf",
        "page": 42,
        "tenant_id": "acme-corp"
    }
)

# Or with pre-computed vector
documents.data.insert(
    properties={"content": "...", "source": "..."},
    vector=precomputed_embedding
)

# Hybrid search (BM25 + vector)
from weaviate.classes.query import MetadataQuery, Filter

results = documents.query.hybrid(
    query="how to install",
    alpha=0.5,  # 0=BM25 only, 1=vector only
    limit=10,
    filters=Filter.by_property("tenant_id").equal("acme-corp"),
    return_metadata=MetadataQuery(score=True, explain_score=True)
)

for obj in results.objects:
    print(f"Score: {obj.metadata.score}, Content: {obj.properties['content'][:100]}")

client.close()
```

---

## Qdrant Setup

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue,
    PayloadSchemaType
)

# Connect to Qdrant Cloud
client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key="your-api-key"
)

# Or local
client = QdrantClient(host="localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE
    )
)

# Create payload index for fast filtering
client.create_payload_index(
    collection_name="documents",
    field_name="tenant_id",
    field_schema=PayloadSchemaType.KEYWORD
)

# Upsert points
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id="doc-1",
            vector=embedding_vector,
            payload={
                "content": "Installation guide...",
                "source": "manual.pdf",
                "page": 42,
                "tenant_id": "acme-corp"
            }
        )
    ]
)

# Search with filter
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="tenant_id",
                match=MatchValue(value="acme-corp")
            )
        ]
    ),
    with_payload=True
)

# Batch upsert for large datasets
from qdrant_client.models import Batch

client.upsert(
    collection_name="documents",
    points=Batch(
        ids=ids_list,
        vectors=vectors_list,
        payloads=payloads_list
    )
)
```

---

## Chroma Setup

```python
import chromadb
from chromadb.config import Settings

# Persistent local storage
client = chromadb.PersistentClient(
    path="./chroma_data",
    settings=Settings(anonymized_telemetry=False)
)

# Create collection with custom embedding function
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

embedding_fn = OpenAIEmbeddingFunction(
    api_key="your-openai-key",
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}
)

# Add documents (auto-embeds)
collection.add(
    ids=["doc-1", "doc-2"],
    documents=["Installation guide...", "Configuration steps..."],
    metadatas=[
        {"source": "manual.pdf", "page": 42},
        {"source": "manual.pdf", "page": 43}
    ]
)

# Or with pre-computed embeddings
collection.add(
    ids=["doc-3"],
    embeddings=[precomputed_vector],
    metadatas=[{"source": "guide.pdf"}],
    documents=["Original text for reference"]
)

# Query
results = collection.query(
    query_texts=["how to install"],
    n_results=10,
    where={"source": "manual.pdf"},
    include=["documents", "metadatas", "distances"]
)

# Update existing document
collection.update(
    ids=["doc-1"],
    documents=["Updated installation guide..."],
    metadatas=[{"source": "manual_v2.pdf", "page": 42}]
)
```

---

## pgvector Setup

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI dimensions
    source VARCHAR(255),
    page INTEGER,
    tenant_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create HNSW index (recommended for most cases)
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Or IVFFlat for very large datasets
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create index on filter columns
CREATE INDEX ON documents (tenant_id);
```

```python
import psycopg2
from pgvector.psycopg2 import register_vector

conn = psycopg2.connect("postgresql://localhost/ragdb")
register_vector(conn)

# Insert with embedding
cur = conn.cursor()
cur.execute(
    """
    INSERT INTO documents (content, embedding, source, page, tenant_id)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    """,
    ("Installation guide...", embedding_vector, "manual.pdf", 42, "acme-corp")
)

# Similarity search with filter
cur.execute(
    """
    SELECT id, content, source, page,
           1 - (embedding <=> %s) AS similarity
    FROM documents
    WHERE tenant_id = %s
    ORDER BY embedding <=> %s
    LIMIT 10
    """,
    (query_embedding, "acme-corp", query_embedding)
)

results = cur.fetchall()

# Hybrid search with pg_trgm
cur.execute(
    """
    SELECT id, content,
           (0.5 * (1 - (embedding <=> %s))) +
           (0.5 * similarity(content, %s)) AS hybrid_score
    FROM documents
    WHERE tenant_id = %s
      AND content %% %s  -- Trigram similarity threshold
    ORDER BY hybrid_score DESC
    LIMIT 10
    """,
    (query_embedding, query_text, "acme-corp", query_text)
)
```

---

## Index Tuning Guide

### HNSW Parameters

| Parameter | Description | Trade-off |
|-----------|-------------|-----------|
| `m` | Connections per node | Higher = better recall, more memory |
| `ef_construction` | Build-time search width | Higher = better index, slower build |
| `ef_search` | Query-time search width | Higher = better recall, slower query |

```python
# Qdrant HNSW tuning
client.update_collection(
    collection_name="documents",
    hnsw_config=HnswConfigDiff(
        m=16,                    # Default: 16, increase for better recall
        ef_construct=100,        # Default: 100, higher for better index
        full_scan_threshold=10000  # Use brute force below this size
    )
)

# Query-time ef adjustment
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    search_params=SearchParams(hnsw_ef=128)  # Higher for better recall
)
```

### Quantization for Scale

```python
# Qdrant scalar quantization (4x memory reduction)
from qdrant_client.models import ScalarQuantization, ScalarQuantizationConfig

client.update_collection(
    collection_name="documents",
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(
            type="int8",
            quantile=0.99,
            always_ram=True
        )
    )
)
```

---

## Multi-Tenancy Patterns

### Namespace Isolation (Pinecone)
```python
# Tenant data in separate namespaces
index.upsert(vectors=[...], namespace="tenant-acme")
index.upsert(vectors=[...], namespace="tenant-globex")

# Query within tenant namespace
results = index.query(
    vector=query_embedding,
    namespace="tenant-acme",
    top_k=10
)
```

### Metadata Filtering (Qdrant/Weaviate)
```python
# Add tenant_id to all documents
point = PointStruct(
    id="doc-1",
    vector=embedding,
    payload={"tenant_id": "acme", "content": "..."}
)

# Always filter by tenant
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[FieldCondition(key="tenant_id", match=MatchValue(value="acme"))]
    )
)
```

### Collection per Tenant (High Isolation)
```python
# Create tenant-specific collection
client.create_collection(
    collection_name=f"docs_{tenant_id}",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)
```

---

## Decision Flowchart

```
Start
  │
  ├─ Need managed service with zero ops?
  │   └─ Yes → Pinecone
  │
  ├─ Have existing PostgreSQL?
  │   └─ Yes → pgvector (if vectors < 2000 dims)
  │
  ├─ Need built-in vectorization?
  │   └─ Yes → Weaviate
  │
  ├─ Need maximum performance + self-host?
  │   └─ Yes → Qdrant
  │
  ├─ Prototyping / local development?
  │   └─ Yes → Chroma
  │
  └─ Default recommendation → Qdrant (balance of features/performance)
```

---

## Quick Reference

| Task | Pinecone | Weaviate | Qdrant | pgvector |
|------|----------|----------|--------|----------|
| Create index/collection | `create_index()` | `collections.create()` | `create_collection()` | `CREATE TABLE` |
| Insert | `upsert()` | `data.insert()` | `upsert()` | `INSERT` |
| Search | `query()` | `query.near_vector()` | `search()` | `ORDER BY <=>` |
| Filter | `filter={}` | `Filter.by_property()` | `query_filter=Filter()` | `WHERE` |
| Delete | `delete()` | `data.delete_by_id()` | `delete()` | `DELETE` |
| Hybrid | sparse_vector param | `query.hybrid()` | sparse vectors | Manual |

## Related Skills

- **Database Optimizer** - Index tuning and query performance
- **Cloud Architect** - Infrastructure decisions for vector DB hosting
- **Python Pro** - Implementation patterns with async clients
