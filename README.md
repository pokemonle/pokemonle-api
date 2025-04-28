# Pokemonle API

## Deploy Guide

1. Create a `.env` file and add the following environment variables.
2. Install dependencies.
    ```bash
    uv sync --all-groups 
    uv pip install -e .  
    ```
3. Run api with uvicorn.
    ```bash
    uvicorn main:app --reload --port 9000
    ```