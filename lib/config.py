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
        'url': 'http://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz',
        'download_type': 'gz',
        'file_in_zip': 'JMdict_e',
        'local_path': os.path.join(DICT_DIR, 'JMdict_e'),
        'parser_module': 'jmdict_parser'
    },
    {
        'name': 'Chinese',
        'url': 'https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz',
        'download_type': 'gz',
        'file_in_zip': 'cedict_1_0_ts_utf-8_mdbg.txt',
        'local_path': os.path.join(DICT_DIR, 'cedict_1_0_ts_utf-8_mdbg.txt'),
        'parser_module': 'cedict_parser'
    }
]

# --- Filtering Configuration ---
# Keywords that identify low-quality or "meta" definitions to be filtered out by the parsers.
META_KEYWORDS = [
    'variant of',
    'see ',
    'abbr',
    'surname ',
    'old variant of',
]

# --- Frequency List Configuration ---
# URLs for downloading word frequency lists.
FREQUENCY_CONFIG = [
    {
        'name': 'Japanese',
        # Source: https://github.com/chriskempson/japanese-subtitles-word-kanji-frequency-lists
        'url': 'https://raw.githubusercontent.com/chriskempson/japanese-subtitles-word-kanji-frequency-lists/master/word_freq_report.txt',
        'local_path': os.path.join(DICT_DIR, 'jp_freq.txt'),
    },
    {
        'name': 'Chinese',
        # Source: https://github.com/hermitdave/FrequencyWords/
        'url': 'https://raw.githubusercontent.com/hermitdave/FrequencyWords/refs/heads/master/content/2018/zh_cn/zh_cn_50k.txt',
        'local_path': os.path.join(DICT_DIR, 'zh_freq.txt'),
    }
]
