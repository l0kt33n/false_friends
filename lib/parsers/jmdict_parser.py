# lib/parsers/jmdict_parser.py
from xml.etree import ElementTree as ET
from typing import Generator, Tuple, Dict
from collections import defaultdict
from ..config import META_KEYWORDS  # Import from the centralized config

def parse(file_path: str) -> Generator[Tuple[str, str], None, None]:
    """
    Parses the JMDict XML file memory-efficiently, combining definitions for the same character.
    """
    # Dictionary to collect all definitions for each kanji
    word_definitions: Dict[str, list] = defaultdict(list)
    
    context = ET.iterparse(file_path, events=('end',))
    for _, elem in context:
        if elem.tag == 'entry':
            kanji_elements = elem.findall('k_ele/keb')
            if not kanji_elements:
                elem.clear()
                continue
            
            senses = elem.findall('sense')
            all_defs = [gloss.text for sense in senses for gloss in sense.findall('gloss') if gloss.text]
            
            # Use the imported list for filtering
            filtered_defs = [
                d for d in all_defs
                if not any(keyword in d.lower() for keyword in META_KEYWORDS)
            ]

            if filtered_defs:
                for k_ele in kanji_elements:
                    if k_ele.text:
                        word_definitions[k_ele.text].extend(filtered_defs)
            
            elem.clear()
    
    # Yield combined definitions for each character
    for word, defs in word_definitions.items():
        # Remove duplicates while preserving order
        unique_defs = []
        for d in defs:
            if d not in unique_defs:
                unique_defs.append(d)
        
        combined_definition = '; '.join(unique_defs)
        if combined_definition:
            yield (word, combined_definition)