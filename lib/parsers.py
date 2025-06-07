# lib/parsers.py

import re
from xml.etree import ElementTree as ET
from collections import defaultdict

# --- Specific Parser Implementations ---
# Each parser now 'yields' results one by one to keep memory usage low,
# instead of returning a giant dictionary.

def parse_jmdict(file_path):
    """
    Parses the JMDict XML file and yields (word, definition) tuples.
    This approach is memory-efficient as it doesn't load the whole file at once.
    """
    print(f"Parsing '{file_path}' with JMDict parser...")
    context = ET.iterparse(file_path, events=('end',))
    for _, elem in context:
        if elem.tag == 'entry':
            kanji_elements = elem.findall('k_ele/keb')
            if not kanji_elements:
                elem.clear()
                continue
            
            # Group definitions by entry
            definitions_by_entry = defaultdict(list)
            senses = elem.findall('sense')
            definitions = [gloss.text for sense in senses for gloss in sense.findall('gloss') if gloss.text]

            if definitions:
                # Combine all definitions for a single entry into one string
                full_definition = '; '.join(definitions)
                for k_ele in kanji_elements:
                    if k_ele.text:
                        yield (k_ele.text, full_definition)
            
            # Clear the element from memory after processing
            elem.clear()

def parse_cedict(file_path):
    """
    Parses the CC-CEDICT text file and yields (word, definition) tuples.
    """
    print(f"Parsing '{file_path}' with CC-CEDICT parser...")
    line_regex = re.compile(r'^(\S+)\s+\S+\s+\[.*?\]\s+/(.*)/$')
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            match = line_regex.match(line)
            if match:
                hanzi, gloss_str = match.groups()
                # Join multiple definitions with a semicolon
                full_definition = '; '.join(gloss_str.split('/'))
                yield (hanzi, full_definition)

# --- Parser Registry ---
# This maps the 'parser_key' from the config to the actual parser function.
PARSER_REGISTRY = {
    'jmdict': parse_jmdict,
    'cedict': parse_cedict,
}
