# lib/parsers/jmdict_parser.py
from xml.etree import ElementTree as ET
from typing import Generator, Tuple
from ..config import META_KEYWORDS  # Import from the centralized config

def parse(file_path: str) -> Generator[Tuple[str, str], None, None]:
    """
    Parses the JMDict XML file memory-efficiently, filtering out low-quality definitions.
    """
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
                full_definition = '; '.join(filtered_defs)
                for k_ele in kanji_elements:
                    if k_ele.text:
                        yield (k_ele.text, full_definition)
            
            elem.clear()