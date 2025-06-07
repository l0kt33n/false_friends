# lib/data_loader.py
import requests
import zipfile
import io
import time
import os
import importlib
from psycopg2.extras import execute_values

from lib.config import LANGUAGE_CONFIG, DICT_DIR
from lib.database import get_db_connection, init_db

def _download_file(url, local_path):
    print(f"Downloading to '{os.path.basename(local_path)}'...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def _extract_zip(zip_path, extract_to_dir):
    print(f"Extracting '{os.path.basename(zip_path)}'...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)

def populate_database():
    """Orchestrates the full data loading pipeline."""
    if not os.path.exists(DICT_DIR):
        os.makedirs(DICT_DIR)
        
    init_db() # Create a clean database
    
    with get_db_connection() as conn:
        for lang_conf in LANGUAGE_CONFIG:
            name = lang_conf['name']
            parser_module_name = lang_conf['parser_module']
            
            print(f"\n--- Processing: {name} ---")
            start_time = time.time()
            
            try:
                # Download and extract
                if lang_conf['download_type'] == 'zip':
                    zip_download_path = lang_conf['local_path'] + ".zip"
                    _download_file(lang_conf['url'], zip_download_path)
                    _extract_zip(zip_download_path, DICT_DIR)
                    file_to_parse = lang_conf['local_path'] # The extracted file path
                else: # 'direct'
                    _download_file(lang_conf['url'], lang_conf['local_path'])
                    file_to_parse = lang_conf['local_path']
                
                # Dynamically import the correct parser
                parser_module = importlib.import_module(f".parsers.{parser_module_name}", package="lib")
                
                with conn.cursor() as cursor:
                    # Get the generator from the parser and prepare for batch insert
                    word_generator = parser_module.parse(file_to_parse)
                    data_to_insert = ((name, word, definition) for word, definition in word_generator)
                    
                    # Use psycopg2's execute_values for high-performance batch inserting
                    page_size = 2000 # Insert in batches of 2000
                    execute_values(
                        cursor,
                        "INSERT INTO words (language, word, definition) VALUES %s",
                        data_to_insert,
                        page_size=page_size
                    )
                    count = cursor.rowcount
                    
                duration = time.time() - start_time
                print(f"Inserted {count} entries for {name} in {duration:.2f} seconds.")

            except Exception as e:
                print(f"An error occurred while processing {name}: {e}")
