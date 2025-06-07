# lib/analysis.py
import pandas as pd
import spacy  # Import the new library
from .database import get_db_connection

# --- spaCy Model Loading ---
# Load the model once when the module is imported for efficiency.
# This will raise a helpful error if the model isn't downloaded.
try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    print(
        "\n--- Spacy Model Not Found ---"
        "\nPlease install the model by running this command in your terminal:"
        "\npython -m spacy download en_core_web_sm\n"
    )
    NLP = None  # Set to None to avoid further errors during import

def get_cosine_similarity(text1, text2):
    """Calculates semantic similarity using word embeddings from spaCy."""
    # Ensure the NLP model was loaded successfully
    if NLP is None:
        return 0.0

    # Create spaCy "document" objects
    doc1 = NLP(text1)
    doc2 = NLP(text2)
    
    # Handle cases where a doc has no vector or the vector is all zeros
    if not doc1.has_vector or not doc2.has_vector or doc1.vector_norm == 0 or doc2.vector_norm == 0:
        return 0.0

    # Return the built-in similarity score, which is based on the cosine
    # similarity of the averaged vectors of the words in each text.
    return doc1.similarity(doc2)


def find_all_false_friends(base_language, target_language, similarity_threshold=0.1):
    """Finds false friends by querying the database."""
    print(f"\nFinding false friends between '{base_language}' and '{target_language}'...")
    
    with get_db_connection() as conn:
        query = """
            SELECT
                T1.word,
                T1.definition AS base_def,
                T2.definition AS target_def
            FROM words T1
            JOIN words T2 ON T1.word = T2.word
            WHERE T1.language = %(base_lang)s AND T2.language = %(target_lang)s
        """
        params = {'base_lang': base_language, 'target_lang': target_language}
        
        df = pd.read_sql_query(query, conn, params=params)
    
    print(f"Found {len(df)} common words to analyze.")
    if df.empty:
        return pd.DataFrame()

    # Calculate similarity for each row using the new cosine similarity function
    print("Calculating semantic similarity using spaCy (this may take a moment)...")
    df['Similarity'] = df.apply(
        lambda row: get_cosine_similarity(row['base_def'], row['target_def']),
        axis=1
    )

    # Filter by the threshold
    false_friends_df = df[df['Similarity'] < similarity_threshold].copy()
    
    # Rename columns for final presentation
    false_friends_df.rename(columns={
        'word': 'Word',
        'base_def': f'{base_language} Definition',
        'target_def': f'{target_language} Definition'
    }, inplace=True)
    
    print(f"Analysis complete. Found {len(false_friends_df)} potential false friends.")
    return false_friends_df