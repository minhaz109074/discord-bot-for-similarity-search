# Discord Bot for Similarity Search

This repository hosts a Python-based Discord bot designed for performing similarity searches, answering questions, and summarizing text. It integrates with image databases to find visually similar images and provides intelligent text-based responses.

## Features

- **/ask Command**: Users can ask questions and receive informative responses.
- **/summarise Command**: Provides concise summaries of lengthy texts.
- **/search Command**: Finds similar images in a connected database to enhance visual query capabilities.

## Vector Database Integration

This bot uses **pgvector**, a PostgreSQL extension for vector similarity search, to efficiently manage and search image vectors within the database. The `pgvector` extension allows for fast and scalable similarity searches, making it ideal for handling large collections of images and other vectorized data.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/minhaz109074/discord-bot-for-similarity-search.git
    cd discord-bot-for-similarity-search
    ```

2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Discord bot and add the token to your environment variables.

## Usage

- **/ask**: Use `/ask [your question]` to get an answer.
- **/summarise**: Use `/summarise [text]` to get a summarized version of the provided text.
- **/search**: Use `/search [image]` to retrieve similar images from the database.
