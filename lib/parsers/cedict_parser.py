# lib/parsers/cedict_parser.py
import re
from typing import Generator, Tuple

CEDICT_LINE_RE = re.compile(
    r"^(?P<trad>\S+)\s+(?P<simp>\S+)\s+\[(?P<pinyin>.*?)\]\s+/(?P<english>.*)/$"
)

def parse(file_path: str) -> Generator[Tuple[str, str], None, None]:
    """
    Parses the CC-CEDICT file line by line, filtering out low-quality definitions.

    Yields:
        A tuple containing (word, combined_definition_string).
        We use the 'simplified' characters as the canonical word.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue

            match = CEDICT_LINE_RE.match(line)
            if match:
                simplified_word = match.group('simp')
                
                # Get all definitions for the entry
                all_defs = [d.strip() for d in match.group('english').split('/') if d.strip()]
                
                # Filter out unhelpful "meta" definitions
                filtered_defs = [
                    d for d in all_defs 
                    if not d.lower().startswith('surname ') 
                    and not d.lower().startswith('variant of ')
                    and not d.lower().startswith('abbr. for ')
                ]
                
                # If filtering removed all definitions, skip this word entry entirely.
                if not filtered_defs:
                    continue
                    
                definitions = '; '.join(filtered_defs)

                if simplified_word and definitions:
                    yield (simplified_word, definitions)