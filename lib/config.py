# lib/config.py
import os

# --- Directory Configuration ---
# Get the absolute path of the project's root directory
# This makes all paths work regardless of where the script is run
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DICT_DIR = os.path.join(PROJECT_ROOT, 'dict')

# --- Database Configuration ---
# These credentials match the ones in docker-compose.yml
DB_CONFIG = {
    'dbname': 'lang_db',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost', # 'localhost' because we mapped the port
    'port': '5432'
}

# --- Language & Parser Configuration ---
LANGUAGE_CONFIG = [
    {
        'name': 'Japanese',
        'url': 'http://ftp.edrdg.org/pub/Nihongo/JMdict_e.zip',
        'download_type': 'zip',
        'file_in_zip': 'JMdict_e',
        'local_path': os.path.join(DICT_DIR, 'JMdict_e'),
        'parser_module': 'jmdict_parser'
    },
    {
        'name': 'Chinese',
        'url': 'https://raw.githubusercontent.com/mdbg/cc-cedict/master/cedict_ts.u8',
        'download_type': 'direct',
        'local_path': os.path.join(DICT_DIR, 'cedict_ts.u8'),
        'parser_module': 'cedict_parser'
    }
]
