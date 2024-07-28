# TF-IDF Based Document Retrieval System

This project implements a simple document retrieval system using TF-IDF (Term Frequency-Inverse Document Frequency) to rank documents based on their relevance to a given query.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Example Queries](#example-queries)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

1. Download the project files and place them in your desired directory.

2. Navigate to the project directory:
    ```sh
    cd /path/to/your/project
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Place your documents in the `US_Inaugural_Addresses` directory. Ensure each document is a text file with a `.txt` extension.
2. Run the script:
    ```sh
    python main.py
    ```
3. The script will process the documents and print the TF-IDF weights for specific terms and the most relevant documents for example queries.


- **US_Inaugural_Addresses/**: Directory containing the text documents to be processed.
- **main.py**: Main script for processing documents and handling queries.
- **requirements.txt**: List of required Python packages.
- **README.md**: This file.

## How It Works

1. **Tokenization and Preprocessing**: 
    - The script reads each document, tokenizes the text, removes stopwords, and applies stemming using the Porter stemmer.

2. **TF-IDF Calculation**:
    - **Term Frequency (TF)**: Measures how frequently a term appears in a document.
    - **Inverse Document Frequency (IDF)**: Measures the importance of a term by considering how frequently it appears across all documents.
    - **TF-IDF**: Combines TF and IDF to give a weight that highlights important terms.

3. **Normalization**:
    - Both document vectors and query vectors are normalized to allow for cosine similarity comparison.

4. **Query Processing**:
    - The script processes the query, computes the cosine similarity between the query vector and each document vector, and returns the most relevant document.

## Example Queries

```python
print("(%s, %.12f)" % query("pleasing people"))
print("(%s, %.12f)" % query("british war"))
print("(%s, %.12f)" % query("false public"))
print("(%s, %.12f)" % query("people institutions"))
print("(%s, %.12f)" % query("violated willingly"))




