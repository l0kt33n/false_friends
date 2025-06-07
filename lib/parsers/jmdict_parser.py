# lib/parsers/cedict_parser.py
import re
from typing import Generator, Tuple
from ..config import META_KEYWORDS  # Import from the centralized config

CEDICT_LINE_RE = re.compile(
    r"^(?P<trad>\S+)\s+(?P<simp>\S+)\s+\[(?P<pinyin>.*?)\]\s+/(?P<english>.*)/$"
)

def parse(file_path: str) -> Generator[Tuple[str, str], None, None]:
    """
    Parses the CC-CEDICT file line by line, filtering out low-quality definitions.
    """
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
                
                if not filtered_defs:
                    continue
                    
                definitions = '; '.join(filtered_defs)

                if simplified_word and definitions:
                    yield (simplified_word, definitions)