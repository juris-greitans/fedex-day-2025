# FedEx Day 2025

This project is a simple implementation of a completely local (on-premise) chatbot using Docling and Ollama.

It was inspired and based on Dave Ebbellar's [example](https://github.com/daveebbelaar/ai-cookbook/tree/main/knowledge/docling) in his AI Cookbook repository (also see his video [How to Get Your Data Ready for AI Agents (Docs, PDFs, Websites)](https://www.youtube.com/watch?v=9lBTS5dM27c)).

## Prerequisites

### Ollama

- Install [Ollama](https://ollama.com/download)
- Pull at least one model [suitable for embeddings](https://ollama.com/search?c=embedding), for example [nomic-embed-text](https://ollama.com/library/nomic-embed-text) or [mxbai-embed-large](https://ollama.com/library/mxbai-embed-large):

  ```shell
    ollama pull mxbai-embed-large
    ollama pull nomic-embed-text
  ```
  
- Pull at least one model that can be used for response generation, for example `granite3.3:2b`:

  ```shell
  ollama pull granite3.3:2b
  ```

### Python

- Install Python 3.
- Create a new virtual environment in current directory:
  
    ```bash
    python -m venv .venv
    ```

### Activate the virtual environment

Open the command prompt (or PowerShell) and activate the virtual environment:

  ```bash
  # For Windows command prompt
  ./.venv/Scripts/activate.bat
  # For Windows PowerShell
  ./.venv/Scripts/Activate.ps1
  # For Bash (Linux, macOS, WSL)
  source .venv/bin/activate
    ```

- Install the required packages:

  ```bash
  pip install -r requirements.txt
  ```

### Configuration

Create a file named `.env` in the root directory of the project and add the following lines:

```bash
OPENAI_API_URL=http://localhost:11434
OPENAI_API_KEY=unused
CHAT_MODEL_NAME=granite3.3:2b
```

You should replace `CHAT_MODEL_NAME` with the model you downloaded for response generation.

`OPENAI_API_KEY` is required by the OpenAI API library, but not used. You can set it to any value.

## Usage

First thing you need is to prepare your knowledge base. To do so, create a directory `input` in the root directory of the project and add your documents there. The documents can be in any format supported by Docling, including PDF, DOCX, TXT, and HTML.

Then run the `create-embeddings.py` script to create the knowledge base:

```bash
python create-embeddings.py
```

This will extract the text from the documents in the `input` directory, create embeddings for each document, and save the embeddings as a vector database in the `data` directory. This script will take longer time first time you run it, because it needs to download additional model used for chunking.

After the embeddings are created, you can run the `chat.py` script to start the chatbot. The chatbot UI is based on Streamlit, so you will run it via the `streamlit` command. Ensure that you have [activated the virtual environment](#activate-the-virtual-environment) before running the command.

```bash
streamlit run chat.py
```

This will start a local web server and open the chatbot UI in your default web browser at [http://localhost:8051](http://localhost:8051).
