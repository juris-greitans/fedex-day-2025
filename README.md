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
  
    ```bash
    python -m venv .venv
    ```

- Open the command prompt (or PowerShell) and activate the virtual environment:

  ```bash
  # For Windows command prompt
  ./.venv/Scripts/activate.bat
  # For Windows PowerShell
  ./.venv/Scripts/Activate.ps1
  ```

- Install the required packages:

  ```bash
  pip install -r requirements.txt
  ```

### Configuration

Create a file named `.env` in the root directory of the project and add the following lines:

```bash
OPENAI_API_URL=http://localhost:11434/v1
OPENAI_API_KEY=unused
```
