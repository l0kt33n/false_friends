# lib/analysis.py
import re
import pandas as pd
from .database import get_db_connection

def jaccard_similarity(text1, text2):
    """Calculates Jaccard similarity between the sets of words in two strings."""
    set1 = set(re.findall(r'\b\w+\b', text1.lower()))
    set2 = set(re.findall(r'\b\w+\b', text2.lower()))
    if not set1 and not set2: return 1.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0

def find_all_false_friends(base_language, target_language, similarity_threshold=0.1):
    """Finds false friends by querying the database."""
    print(f"\nFinding false friends between '{base_language}' and '{target_language}'...")
    
    with get_db_connection() as conn:
        # The SQL query is the heart of the low-memory analysis
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
        
        # Use pandas to read directly from the database query
        df = pd.read_sql_query(query, conn, params=params)
    
    print(f"Found {len(df)} common words to analyze.")
    if df.empty:
        return pd.DataFrame()

    # Calculate similarity for each row
    df['Similarity'] = df.apply(
        lambda row: jaccard_similarity(row['base_def'], row['target_def']),
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
