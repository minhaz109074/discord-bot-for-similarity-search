# Discord Bot for Similarity Search

This repository hosts a Python-based Discord bot designed for performing similarity searches, answering questions, and summarizing text. It integrates with image databases to find visually similar images and provides intelligent text-based responses.

## Features

- **/ask Command**: Users can ask questions and receive informative responses.
- **/summarise Command**: Provides concise summaries of lengthy texts.
- **/search Command**: Finds similar images in a connected database to enhance visual query capabilities.

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
