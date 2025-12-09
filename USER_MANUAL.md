# MCard User Manual

> **Version:** 0.1.25  
> **License:** MIT  
> **Author:** Ben Koo  
> **Python:** >=3.9

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [API Reference](#api-reference)
   - [MCard Class](#mcard-class)
   - [CardCollection Class](#cardcollection-class)
   - [File I/O Module](#file-io-module)
   - [Loader Module](#loader-module)
   - [Content Handle System](#content-handle-system)
   - [RAG (Retrieval-Augmented Generation)](#rag-retrieval-augmented-generation)
   - [PTR (Polynomial Type Runtime)](#ptr-polynomial-type-runtime)
   - [REST API](#rest-api)
6. [Configuration](#configuration)
7. [CLI Commands](#cli-commands)
8. [Advanced Usage](#advanced-usage)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

**MCard** is a local-first, content-addressable storage platform with cryptographic integrity, temporal ordering, and a Polynomial Type Runtime (PTR) that orchestrates polyglot execution. It provides a verifiable data backbone without sacrificing developer ergonomics or observability.

### Key Features

- **Hash-verifiable storage**: SHA-256 hashing with handle registry, history tracking, and immutable audit trail
- **Deterministic execution**: PTR mediates 8 polyglot runtimes (Python, JavaScript, Rust, C, WASM, Lean, R, Julia)
- **Enterprise ready**: Structured logging, CI/CD pipeline, security auditing, 99%+ automated test coverage
- **AI-native extensions**: GraphRAG engine, optional LLM runtime, and optimized multimodal vision
- **Developer friendly**: Rich Python API, TypeScript SDK, BMAD-driven TDD workflow

---

## Installation

### Using pip (from PyPI)

```bash
pip install mcard
```

### Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install mcard
uv venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

uv pip install mcard
```

### From Source

```bash
git clone https://github.com/xlp0/MCard_TDD.git
cd MCard_TDD
./activate_venv.sh          # installs uv & dependencies
uv run pytest -q -m "not slow"  # run the fast Python test suite
```

---

## Quick Start

### Basic Usage

```python
from mcard import MCard, default_collection

# Create a card with content
card = MCard("Hello MCard")

# Add the card to the default collection
hash_value = default_collection.add(card)

# Retrieve the card by its hash
retrieved = default_collection.get(hash_value)

# Get the content as text
print(retrieved.get_content(as_text=True))  # Output: Hello MCard
```

### Working with Binary Content

```python
from mcard import MCard, default_collection

# Create a card with binary content
binary_data = b'\x89PNG\r\n\x1a\n...'  # Example PNG header
card = MCard(binary_data)

# Add and retrieve
hash_value = default_collection.add(card)
retrieved = default_collection.get(hash_value)

# Get raw bytes
content = retrieved.get_content()  # Returns bytes
```

---

## Core Concepts

### Content-Addressable Storage

MCard uses content-addressable storage where each piece of content is identified by its cryptographic hash. This means:

- **Immutability**: Content cannot be modified once stored
- **Deduplication**: Identical content always produces the same hash
- **Integrity**: Content can be verified against its hash at any time

### GTime (Global Time)

Each MCard has a `g_time` timestamp that records:
- The hash algorithm used
- The ISO timestamp of creation
- The region/timezone code

Format: `{hash_algorithm}|{ISO_timestamp}|{region_code}`

Example: `sha256|2024-12-09T09:15:30.123456|UTC`

### Hash Algorithms

MCard supports multiple hash algorithms with automatic collision handling:

| Algorithm | Strength | Description |
|-----------|----------|-------------|
| `md5` | 1 | Legacy, not recommended |
| `sha1` | 1 | Legacy, not recommended |
| `sha224` | 2 | SHA-2 family |
| `sha256` | 3 | **Default**, recommended |
| `sha384` | 4 | Higher security |
| `sha512` | 5 | Maximum security |
| `custom` | 6 | User-defined |

---

## API Reference

### MCard Class

The `MCard` class is the fundamental data container for content with computed hash and timestamp.

#### Constructor

```python
MCard(content: Union[str, bytes], hash_function: Union[str, HashAlgorithm] = HashAlgorithm.get_default())
```

**Parameters:**
- `content`: The content to store (string or bytes). Cannot be None or empty.
- `hash_function`: Hash algorithm to use. Defaults to SHA-256.

**Raises:**
- `ValueError`: If content is None or empty

**Example:**
```python
from mcard import MCard
from mcard.model.hash.enums import HashAlgorithm

# Using default hash (SHA-256)
card1 = MCard("Hello World")

# Using specific hash algorithm
card2 = MCard("Hello World", HashAlgorithm.SHA512)

# Using string for hash algorithm
card3 = MCard("Hello World", "sha384")
```

#### Methods

##### `get_content(as_text: bool = False) -> Union[bytes, str]`

Get the content stored in the card.

**Parameters:**
- `as_text`: If `True`, returns content as UTF-8 string. If `False` (default), returns raw bytes.

**Returns:**
- Content as bytes (default) or string

**Example:**
```python
card = MCard("Hello World")

# Get as bytes (default)
raw_content = card.get_content()  # b'Hello World'

# Get as text
text_content = card.get_content(as_text=True)  # 'Hello World'
```

##### `get_hash() -> str`

Get the cryptographic hash of the content.

**Returns:**
- Hexadecimal hash string

**Example:**
```python
card = MCard("Hello World")
print(card.get_hash())  # 64-character hex string for SHA-256
```

##### `get_g_time() -> str`

Get the GTime timestamp string.

**Returns:**
- Formatted timestamp string: `{hash_algorithm}|{ISO_timestamp}|{region_code}`

**Example:**
```python
card = MCard("Hello World")
print(card.get_g_time())  # sha256|2024-12-09T09:15:30.123456|UTC
```

##### `get_content_type() -> str`

Get the detected MIME type of the content.

**Returns:**
- MIME type string (e.g., `text/plain`, `application/json`, `image/png`)

**Example:**
```python
card = MCard('{"key": "value"}')
print(card.get_content_type())  # application/json
```

##### `to_dict() -> dict`

Convert the MCard to a dictionary representation.

**Returns:**
- Dictionary with keys: `content`, `hash`, `g_time`, `content_type`

**Example:**
```python
card = MCard("Hello World")
data = card.to_dict()
# {
#     'content': 'Hello World',
#     'hash': '...',
#     'g_time': 'sha256|2024-12-09T09:15:30.123456|UTC',
#     'content_type': 'text/plain'
# }
```

##### `to_display_dict() -> dict`

Convert the MCard to a display-friendly dictionary.

**Returns:**
- Dictionary with keys: `hash`, `content_type`, `created_at`, `content_preview`, `card_class`

---

### CardCollection Class

The `CardCollection` class provides a high-level interface for managing collections of MCards with SQLite storage.

#### Constructor

```python
CardCollection(engine=None, engine_type: str = 'sqlite', db_path: str = None)
```

**Parameters:**
- `engine`: Optional pre-configured database engine
- `engine_type`: Type of database engine (only 'sqlite' supported)
- `db_path`: Path to database file. Defaults to `./data/DEFAULT_DB_FILE.db`

**Example:**
```python
from mcard import CardCollection

# Use default database
collection = CardCollection()

# Use custom database path
collection = CardCollection(db_path="./my_data/cards.db")

# Use in-memory database (for testing)
collection = CardCollection(db_path=":memory:")
```

#### Methods

##### `add(card: MCard) -> str`

Add a card to the collection.

**Parameters:**
- `card`: The MCard to add

**Returns:**
- The hash of the card

**Behavior:**
- If content already exists: Creates a duplicate event card
- If hash collision occurs: Upgrades hash algorithm and creates collision event

**Example:**
```python
from mcard import MCard, CardCollection

collection = CardCollection()
card = MCard("Hello World")
hash_value = collection.add(card)
print(f"Added card with hash: {hash_value}")
```

##### `get(hash_value: str) -> Optional[MCard]`

Retrieve a card by its hash.

**Parameters:**
- `hash_value`: The hash of the card to retrieve

**Returns:**
- The MCard if found, `None` otherwise

**Example:**
```python
card = collection.get("abc123...")
if card:
    print(card.get_content(as_text=True))
else:
    print("Card not found")
```

##### `delete(hash_value: str) -> bool`

Delete a card by its hash.

**Parameters:**
- `hash_value`: The hash of the card to delete

**Returns:**
- `True` if deleted, `False` if not found

**Example:**
```python
success = collection.delete("abc123...")
print("Deleted" if success else "Not found")
```

##### `count() -> int`

Get the total number of cards in the collection.

**Returns:**
- Integer count of cards

**Example:**
```python
total = collection.count()
print(f"Collection has {total} cards")
```

##### `clear() -> None`

Remove all cards from the collection.

**Example:**
```python
collection.clear()
print(f"Collection now has {collection.count()} cards")  # 0
```

##### `get_page(page_number: int = 1, page_size: int = None) -> Page`

Get a paginated view of cards.

**Parameters:**
- `page_number`: Page number (1-based)
- `page_size`: Items per page (defaults to 10)

**Returns:**
- `Page` object with cards and pagination metadata

**Example:**
```python
page = collection.get_page(page_number=1, page_size=20)
print(f"Page {page.page_number} of {page.total_pages}")
for card in page.items:
    print(card.get_hash()[:8])
```

##### `search_by_content(search_string: str, page_number: int = 1, page_size: int = None) -> Page`

Search for cards containing the given string in their content.

**Parameters:**
- `search_string`: String to search for
- `page_number`: Page number (1-based)
- `page_size`: Items per page

**Returns:**
- `Page` object with matching cards

**Example:**
```python
results = collection.search_by_content("hello", page_number=1)
print(f"Found {results.total_items} cards containing 'hello'")
```

##### `search_by_hash(hash_value: str, page_number: int = 1, page_size: int = None) -> Page`

Search for cards by hash value.

**Parameters:**
- `hash_value`: Hash to search for
- `page_number`: Page number (1-based)
- `page_size`: Items per page

**Returns:**
- `Page` object with matching cards

##### `search_by_string(search_string: str, page_number: int = 1, page_size: int = None) -> Page`

Search for cards by string in content, hash, or g_time.

**Parameters:**
- `search_string`: String to search for
- `page_number`: Page number (1-based)
- `page_size`: Items per page

**Returns:**
- `Page` object with matching cards

##### `get_all_mcards_raw() -> List[MCard]`

Retrieve all MCard objects directly without pagination.

**Returns:**
- List of all MCard objects

**Example:**
```python
all_cards = collection.get_all_mcards_raw()
for card in all_cards:
    print(card.get_hash()[:8], card.get_content_type())
```

##### `get_all_cards(page_size: int = 10, process_callback: Optional[Callable] = None) -> Tuple[List[MCard], int]`

Retrieve all cards with optional processing callback.

**Parameters:**
- `page_size`: Items per page for internal pagination
- `process_callback`: Optional function to process each card

**Returns:**
- Tuple of (list of cards, total count)

**Example:**
```python
def process_card(card):
    return card.to_display_dict()

cards, total = collection.get_all_cards(process_callback=process_card)
```

##### `print_all_cards(db_path: Optional[str] = None, page_size: int = 10) -> None`

Print all cards in a formatted table (static method).

**Parameters:**
- `db_path`: Optional database path
- `page_size`: Items per page

**Example:**
```python
CardCollection.print_all_cards()
```

---

### Content Handle System

Handles provide mutable pointers to immutable MCard content, enabling human-friendly naming and versioning.

#### `add_with_handle(card: MCard, handle: str) -> str`

Add a card and register a handle for it.

**Parameters:**
- `card`: The MCard to add
- `handle`: Human-friendly name (supports Unicode)

**Returns:**
- The hash of the added card

**Handle Rules:**
- Must start with a letter (any language)
- Can contain letters, digits, underscores, hyphens
- Maximum 63 characters
- Case-insensitive (normalized to lowercase)

**Example:**
```python
card = MCard("Document version 1")
hash_value = collection.add_with_handle(card, "my_document")
```

#### `update_handle(handle: str, new_card: MCard) -> str`

Update a handle to point to a new card.

**Parameters:**
- `handle`: The handle to update
- `new_card`: The new MCard

**Returns:**
- The hash of the new card

**Example:**
```python
new_card = MCard("Document version 2")
collection.update_handle("my_document", new_card)
```

#### `get_by_handle(handle: str) -> Optional[MCard]`

Get the card currently pointed to by a handle.

**Parameters:**
- `handle`: The handle to resolve

**Returns:**
- The MCard, or `None` if handle doesn't exist

**Example:**
```python
card = collection.get_by_handle("my_document")
if card:
    print(card.get_content(as_text=True))
```

#### `resolve_handle(handle: str) -> Optional[str]`

Resolve a handle to its current hash.

**Parameters:**
- `handle`: The handle to resolve

**Returns:**
- The current hash, or `None`

#### `get_handle_history(handle: str) -> list`

Get the version history for a handle.

**Returns:**
- List of dicts with `previous_hash` and `changed_at` keys

**Example:**
```python
history = collection.get_handle_history("my_document")
for version in history:
    print(f"Changed at {version['changed_at']}: {version['previous_hash'][:8]}...")
```

---

### File I/O Module

The `file_io` module handles safe file reading, streaming, and directory traversal.

#### `read_file_safely(file_path, allow_pathological=False, max_bytes=None) -> bytes`

Read file content with timeout protection and size limits.

**Parameters:**
- `file_path`: Path to the file
- `allow_pathological`: Bypass long-line/pathological content checks
- `max_bytes`: Cap the number of bytes read

**Returns:**
- File content as bytes

**Raises:**
- `TimeoutError`: If reading takes too long
- `OSError`: If file cannot be read or is too large (>50MB)

**Example:**
```python
from mcard import file_io

content = file_io.read_file_safely("./document.txt")
```

#### `list_files(directory, recursive=False) -> List[Path]`

List all safe files in a directory.

**Parameters:**
- `directory`: Directory path
- `recursive`: Include subdirectories

**Returns:**
- List of Path objects for safe files

**Example:**
```python
from mcard import file_io

files = file_io.list_files("./documents", recursive=True)
for f in files:
    print(f)
```

#### `process_file_content(file_path, force_binary=False, allow_pathological=False, max_bytes=None) -> dict`

Process a file and return its metadata and content.

**Returns:**
- Dictionary with keys: `content`, `filename`, `mime_type`, `extension`, `is_binary`, `size`

**Example:**
```python
from mcard import file_io

info = file_io.process_file_content("./image.png")
print(f"Type: {info['mime_type']}, Size: {info['size']} bytes")
```

#### `is_problematic_file(file_path) -> bool`

Check if a file is likely to cause processing issues.

**Returns:**
- `True` if file should be skipped or handled specially

---

### Loader Module

The `loader` module handles high-level file processing and storage into CardCollections.

#### `load_file_to_collection(path, collection, recursive=False, include_problematic=False, max_bytes_on_problem=2MB, metadata_only=False) -> list`

Load a file or directory of files into a collection.

**Parameters:**
- `path`: Path to file or directory
- `collection`: CardCollection to store MCards in
- `recursive`: Process subdirectories
- `include_problematic`: Process problematic files with safe text streaming
- `max_bytes_on_problem`: Cap bytes for problematic files
- `metadata_only`: Store only metadata for problematic files

**Returns:**
- List of processing info dictionaries

**Example:**
```python
from mcard import loader, CardCollection

collection = CardCollection()
results = loader.load_file_to_collection(
    "./documents",
    collection,
    recursive=True
)
print(f"Processed {len(results)} files")
```

#### `process_and_store_file(file_path, collection, allow_problematic=False, max_bytes_on_problem=None, metadata_only=False) -> Optional[dict]`

Process a single file and store it in the collection.

**Returns:**
- Dictionary with processing info, or `None` if skipped

**Example:**
```python
from mcard import loader, CardCollection

collection = CardCollection()
result = loader.process_and_store_file("./document.pdf", collection)
if result:
    print(f"Stored with hash: {result['hash']}")
```

---

### RAG (Retrieval-Augmented Generation)

MCard includes a powerful RAG system for semantic search and AI-powered queries.

#### MCardRAGEngine

Main interface for RAG operations.

```python
from mcard import default_collection
from mcard.rag import MCardRAGEngine

# Initialize
rag = MCardRAGEngine(default_collection)

# Index all content
stats = rag.index_all()
print(f"Indexed: {stats['indexed']}, Skipped: {stats['skipped']}")

# Semantic search
results = rag.search("What is content-addressable storage?", k=5)
for result in results:
    print(f"Score: {result.score:.4f}, Hash: {result.hash[:8]}")

# RAG query with LLM
response = rag.query("Explain the Cubical Logic Model")
print(response.answer)
print(f"Confidence: {response.confidence:.2%}")
print(f"Sources: {response.sources}")
```

#### PersistentIndexer

Manages automatic indexing with persistent storage.

```python
from mcard.rag import get_indexer, semantic_search, index_mcard

# Get or create the default indexer
indexer = get_indexer()

# Index all MCards
stats = indexer.index_all()

# Semantic search
results = semantic_search("query text", k=5)

# Index a single MCard
from mcard import MCard
card = MCard("New content to index")
index_mcard(card)

# Get indexer statistics
stats = indexer.get_stats()
print(f"Indexed: {stats['indexed_count']}, Vectors: {stats['vector_count']}")
```

#### Semantic Versioning

Track semantic evolution of content across handle versions.

```python
from mcard.rag import (
    link_mcard_to_handle,
    get_handle_version_history,
    compare_versions_by_similarity,
    find_most_similar_version,
    get_semantic_evolution
)

# Link MCard to handle
link_mcard_to_handle(card, "my_document")

# Get version history with embeddings
history = get_handle_version_history("my_document")

# Compare two versions
similarity = compare_versions_by_similarity("doc_v1_hash", "doc_v2_hash")

# Find most similar version to a query
result = find_most_similar_version("my_document", "search query")

# Get semantic evolution over time
evolution = get_semantic_evolution("my_document")
```

---

### PTR (Polynomial Type Runtime)

PTR executes CLM (Cubical Logic Model) specifications across multiple runtimes.

#### CLMRunner

Unified runner for CLM execution.

```python
from mcard.ptr.runner import CLMRunner

runner = CLMRunner()

# Execute a CLM file
report = runner.run_file("chapters/chapter_01_arithmetic/addition.yaml")
print(f"Status: {report['status']}")
print(f"Result: {report['result']}")
```

#### PTREngine

Low-level engine for polyglot execution.

```python
from mcard.ptr import PTREngine, default_engine

# Use default engine
engine = default_engine

# Or create a new one
engine = PTREngine()
```

---

### REST API

MCard provides a FastAPI-based REST API for HTTP access.

#### Starting the API Server

```python
from mcard.api import start_api_server

start_api_server()  # Runs on http://0.0.0.0:28302
```

Or via command line:
```bash
uv run python -m mcard.api
```

#### API Endpoints

##### `POST /content/cards`

Store new content and create an MCard.

**Request:**
- `content`: File upload (multipart/form-data)
- `metadata`: Optional JSON string

**Response:**
```json
{
  "hash": "abc123...",
  "content_type": "text/plain",
  "g_time": "sha256|2024-12-09T09:15:30|UTC",
  "message": "Content stored successfully"
}
```

##### `GET /content/cards`

List content cards with pagination.

**Query Parameters:**
- `query`: Optional search string
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10)

**Response:**
```json
{
  "items": [...],
  "total_items": 100,
  "page_number": 1,
  "page_size": 10,
  "total_pages": 10,
  "has_next": true,
  "has_previous": false
}
```

##### `GET /content/cards/{hash}`

Retrieve a single card by hash.

**Response:**
```json
{
  "hash": "abc123...",
  "content_type": "text/plain",
  "g_time": "sha256|2024-12-09T09:15:30|UTC"
}
```

##### `DELETE /content/cards/{hash}`

Delete a card by hash.

**Response:** 204 No Content

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCARD_DB_PATH` | `./data/DEFAULT_DB_FILE.db` | Database file path |
| `MCARD_HASH_ALGORITHM` | `sha256` | Default hash algorithm |
| `MCARD_API_PORT` | `5320` | API server port |
| `MCARD_API_KEY` | `your_api_key_here` | API authentication key |
| `MCARD_SERVICE_LOG_LEVEL` | `DEBUG` | Logging level |
| `MCARD_STORE_MAX_CONNECTIONS` | `10` | Max database connections |
| `MCARD_STORE_TIMEOUT` | `30.0` | Database timeout (seconds) |
| `MCARD_WRAP_WIDTH_DEFAULT` | `1000` | Default line wrap width |
| `MCARD_MAX_PROBLEM_TEXT_BYTES` | `2097152` | Max bytes for problematic files |
| `MCARD_READ_TIMEOUT_SECS` | `30` | File read timeout |

### Using .env File

Create a `.env` file in your project root:

```env
MCARD_DB_PATH=./my_data/cards.db
MCARD_HASH_ALGORITHM=sha256
MCARD_SERVICE_LOG_LEVEL=INFO
```

### Programmatic Configuration

```python
import os

# Set before importing mcard
os.environ["MCARD_DB_PATH"] = "./custom/path/cards.db"
os.environ["MCARD_HASH_ALGORITHM"] = "sha512"

from mcard import default_collection
```

---

## CLI Commands

### PTR CLI

Execute CLM specifications:

```bash
# Run a CLM file
uv run python -m mcard.ptr.cli run chapters/chapter_01_arithmetic/addition.yaml

# Run with context
uv run python -m mcard.ptr.cli run my_clm.yaml --context '{"a": 1}'

# Run in test mode
uv run python -m mcard.ptr.cli run my_clm.yaml --test

# Show polyglot runtime status
uv run python -m mcard.ptr.cli status

# List available CLM files
uv run python -m mcard.ptr.cli list
```

### RAG CLI

Manage RAG operations:

```bash
# Show RAG system status
uv run python -m mcard.rag.cli status

# Index all MCards
uv run python -m mcard.rag.cli index
uv run python -m mcard.rag.cli index --force  # Re-index existing

# Semantic search
uv run python -m mcard.rag.cli search "query text" -k 10

# RAG query with LLM
uv run python -m mcard.rag.cli query "What is MCard?" --model gemma3:latest

# Clear vector index
uv run python -m mcard.rag.cli clear --yes
```

---

## Advanced Usage

### Custom Hash Functions

```python
from mcard import MCard
from mcard.model.hash.enums import HashAlgorithm

# Use SHA-512 for higher security
card = MCard("Sensitive data", HashAlgorithm.SHA512)
```

### Collision Handling

MCard automatically handles hash collisions by upgrading to a stronger algorithm:

```python
from mcard import MCard, CardCollection

collection = CardCollection()

# If two different contents produce the same hash (extremely rare),
# MCard automatically:
# 1. Creates a collision event card
# 2. Upgrades to a stronger hash algorithm
# 3. Stores the new content with the upgraded hash
```

### Monadic Operations

CardCollection provides monadic versions of operations for functional composition:

```python
from mcard import CardCollection

collection = CardCollection()

# Monadic get
result = collection.get_m("hash_value")
if result.is_just():
    card = result.value
    print(card.get_content(as_text=True))

# Chained operations
content = (
    collection.resolve_handle_m("my_doc")
    .bind(lambda h: collection.get_m(h))
    .bind(lambda card: Maybe.just(card.get_content(as_text=True)))
)
```

### Batch File Processing

```python
from mcard import loader, CardCollection

collection = CardCollection()

# Process entire directory recursively
results = loader.load_file_to_collection(
    "./documents",
    collection,
    recursive=True,
    include_problematic=True,  # Handle problematic files
    max_bytes_on_problem=1024*1024  # 1MB cap for problematic files
)

# Process results
for result in results:
    print(f"File: {result['filename']}")
    print(f"Hash: {result['hash']}")
    print(f"Type: {result['content_type']}")
    print(f"Size: {result['size']} bytes")
    print("---")
```

### GraphRAG

Use knowledge graphs for enhanced retrieval:

```python
from mcard.rag import GraphRAGEngine, GraphExtractor, GraphStore

# Initialize GraphRAG
graph_rag = GraphRAGEngine()

# Extract entities and relationships
extractor = GraphExtractor()
entities, relationships = extractor.extract(text_content)

# Store in graph
store = GraphStore()
store.add_entities(entities)
store.add_relationships(relationships)

# Query with graph context
response = graph_rag.query("How are concepts X and Y related?")
```

---

## Troubleshooting

### Common Issues

#### Database Locked

```
sqlite3.OperationalError: database is locked
```

**Solution:** Ensure only one process accesses the database at a time, or increase timeout:
```python
os.environ["MCARD_STORE_TIMEOUT"] = "60"
```

#### File Too Large

```
OSError: File too large: X bytes (max 52428800)
```

**Solution:** MCard has a 50MB file size limit. For larger files, process in chunks or use streaming.

#### Embedding Model Not Available

```
Error: Embedding model not available
```

**Solution:** Ensure Ollama is running and the model is pulled:
```bash
ollama pull nomic-embed-text
```

#### Invalid Hash Algorithm

```
ValueError: 'xyz' is not a valid HashAlgorithm
```

**Solution:** Use one of the supported algorithms: `md5`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`

### Logging

Enable debug logging for troubleshooting:

```python
from mcard.config.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)
logger.debug("Debug message")
```

Or via environment:
```bash
export MCARD_SERVICE_LOG_LEVEL=DEBUG
```

### Getting Help

- **Documentation:** [docs/](./docs/)
- **Issues:** [GitHub Issues](https://github.com/xlp0/MCard_TDD/issues)
- **Source:** [GitHub Repository](https://github.com/xlp0/MCard_TDD)

---

## Page Object Reference

The `Page` class is returned by pagination methods:

```python
@dataclass
class Page:
    items: List[MCard]      # Cards on this page
    page_number: int        # Current page (1-based)
    page_size: int          # Items per page
    total_items: int        # Total cards in collection
    total_pages: int        # Total number of pages
    has_next: bool          # More pages available
    has_previous: bool      # Previous pages available
    
    @property
    def next_page_number(self) -> Optional[int]
    
    @property
    def previous_page_number(self) -> Optional[int]
```

---

## Content Type Detection

MCard automatically detects content types for:

### Text Formats
- Plain text, HTML, XML, CSV, CSS
- JavaScript, TypeScript, Python, Java, C/C++, SQL
- JSON, YAML, Markdown
- Diagram formats (Mermaid, PlantUML, Graphviz)

### Binary Formats
- Images: PNG, JPEG, GIF, BMP, WebP, SVG, ICO
- Documents: PDF, Word, Excel, PowerPoint
- Archives: ZIP, GZIP, RAR, 7Z
- Audio/Video: WAV, MP4, MOV
- Databases: SQLite, Parquet

---

## Summary

MCard provides a robust, content-addressable storage system with:

1. **Immutable Storage**: Content identified by cryptographic hash
2. **Temporal Ordering**: GTime timestamps for audit trails
3. **Handle System**: Mutable pointers to immutable content
4. **RAG Integration**: Semantic search and AI-powered queries
5. **Polyglot Execution**: PTR for multi-language CLM specifications
6. **REST API**: HTTP access to all functionality

For more detailed information, refer to the architecture documentation in `docs/architecture.md` and the PRD in `docs/prd.md`.
