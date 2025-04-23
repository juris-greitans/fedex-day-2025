# Fedex Day

## Prerequisites

### Ollama

- Install [Ollama](https://ollama.com/download)
- Pull at least one model [suitable for embeddings](https://ollama.com/search?c=embedding), for example [nomic-embed-text](https://ollama.com/library/nomic-embed-text) or [mxbai-embed-large](https://ollama.com/library/mxbai-embed-large):

  ```
  ollama pull nomic-embed-text
  ollama pull mxbai-embed-large
  ```

### Python

- Install Python 3.
- Create a new virtual environment in current directory:
  
    ```
    python -m venv .venv
    ```

- Open the command prompt (or PowerShell) and activate the virtual environment:

  ```
  # For Windows command prompt
  ./.venv/Scripts/activate.bat
  # For Windows PowerShell
  ./.venv/Scripts/Activate.ps1
  ```

- Install the required packages:

  ```
  pip install -r requirements.txt
  ```
