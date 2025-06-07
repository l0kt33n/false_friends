# lib/parsers/cedict_parser.py
import re
from typing import Generator, Tuple, Dict
from collections import defaultdict
from ..config import META_KEYWORDS  # Import from the centralized config

CEDICT_LINE_RE = re.compile(
    r"^(?P<trad>\S+)\s+(?P<simp>\S+)\s+\[(?P<pinyin>.*?)\]\s+/(?P<english>.*)/$"
)

def parse(file_path: str) -> Generator[Tuple[str, str], None, None]:
    """
    Parses the CC-CEDICT file, combining definitions for the same character.
    """
    # Dictionary to collect all definitions for each simplified character
    word_definitions: Dict[str, list] = defaultdict(list)
    
    # First pass: collect all definitions
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue

            match = CEDICT_LINE_RE.match(line)
            if match:
                simplified_word = match.group('simp')
                all_defs = [d.strip() for d in match.group('english').split('/') if d.strip()]
                
                # Use the imported list for filtering
                filtered_defs = [
                    d for d in all_defs 
                    if not any(keyword in d.lower() for keyword in META_KEYWORDS)
                ]
                
                # Only add if we have valid definitions after filtering
                if filtered_defs:
                    word_definitions[simplified_word].extend(filtered_defs)
    
    # Second pass: yield combined definitions for each character
    for word, defs in word_definitions.items():
        # Remove duplicates while preserving order
        unique_defs = []
        for d in defs:
            if d not in unique_defs:
                unique_defs.append(d)
        
        combined_definition = '; '.join(unique_defs)
        if word and combined_definition:
            yield (word, combined_definition)