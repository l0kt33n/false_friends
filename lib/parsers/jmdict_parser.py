# lib/parsers/jmdict_parser.py
from xml.etree import ElementTree as ET
from typing import Generator, Tuple

def parse(file_path: str) -> Generator[Tuple[str, str], None, None]:
    """
    Parses the JMDict XML file memory-efficiently.

    Yields:
        A tuple containing (word, combined_definition_string).
    """
    context = ET.iterparse(file_path, events=('end',))
    for _, elem in context:
        if elem.tag == 'entry':
            kanji_elements = elem.findall('k_ele/keb')
            if not kanji_elements:
                elem.clear()
                continue
            
            senses = elem.findall('sense')
            definitions = [gloss.text for sense in senses for gloss in sense.findall('gloss') if gloss.text]
            
            if definitions:
                full_definition = '; '.join(definitions)
                for k_ele in kanji_elements:
                    if k_ele.text:
                        yield (k_ele.text, full_definition)
            
            elem.clear()
