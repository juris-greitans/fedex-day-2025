from typing import List
import os;

import docling_core
import docling_core.transforms
import docling_core.transforms.chunker
import docling_core.transforms.chunker.tokenizer
import docling_core.transforms.chunker.tokenizer.base
import docling_core.transforms.chunker.tokenizer.huggingface
import docling_core.transforms.chunker.tokenizer.openai
import docling_core.types
import docling_core.utils
import lancedb
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from docling_core.types import DoclingDocument
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from openai import OpenAI
from transformers import AutoTokenizer

load_dotenv()

OPENAI_API_URL = os.environ.get("OPENAI_API_URL")
# Initialize OpenAI client (make sure you have OPENAI_API_KEY in your environment variables)
client = OpenAI(base_url=OPENAI_API_URL)

# Get the OpenAI embedding function
func = get_registry().get("ollama").create(name="mxbai-embed-large", host=OPENAI_API_URL)


# Define a simplified metadata schema
class ChunkMetadata(LanceModel):
    """
    You must order the fields in alphabetical order.
    This is a requirement of the Pydantic implementation.
    """

    filename: str | None
    page_numbers: List[int] | None
    title: str | None


# Define the main Schema
class Chunks(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()  # type: ignore
    metadata: ChunkMetadata



SUPPORTED_FILE_EXTENSIONS = ['.pdf', '.docx', '.txt', '.md']

def get_files_in_directory(directory: str) -> List[str]:
    """
    Get a list of all files in the specified directory.
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in SUPPORTED_FILE_EXTENSIONS):
                files.append(os.path.join(root, filename))
    return files


def chunk_document(document: DoclingDocument) -> List[Chunks]:
    """
    Chunk the document into smaller pieces using the HybridChunker.
    """

    tokenizer = AutoTokenizer.from_pretrained("mixedbread-ai/mxbai-embed-large-v1")
    MAX_TOKENS = 8191  # text-embedding-3-large's maximum context length
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=MAX_TOKENS,
        merge_peers=True,
    )

    chunk_iter = chunker.chunk(dl_doc=result.document)
    chunks = list(chunk_iter)

    # Create table with processed chunks
    processed_chunks = [
        {
            "text": chunk.text,
            "metadata": {
                "filename": chunk.meta.origin.filename,
                "page_numbers": [
                    page_no
                    for page_no in sorted(
                        set(
                            prov.page_no
                            for item in chunk.meta.doc_items
                            for prov in item.prov
                        )
                    )
                ]
                or None,
                "title": chunk.meta.headings[0] if chunk.meta.headings else None,
            },
        }
        for chunk in chunks
    ]

    return processed_chunks



db = lancedb.connect("data/lancedb")
table = db.create_table("docling", schema=Chunks, mode="overwrite")

converter = DocumentConverter()

input_dir = "input"
files = get_files_in_directory(input_dir)
for file in files:
    print(f"Processing file: {file}")
    # Convert the document to a DoclingDocument
    result = converter.convert(file)

    # Chunk the document and add to the table
    processed_chunks = chunk_document(result.document)
    table.add(processed_chunks)

# --------------------------------------------------------------
# Load the table
# --------------------------------------------------------------

table.to_pandas()
table.count_rows()
