import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
import re
from collections import defaultdict
import spacy

class BatchOptimizer:
    def __init__(self, scan_paths: List[str], macro_threshold: int = 2):
        self.scan_paths = [Path(p) for p in scan_paths]
        self.macro_threshold = macro_threshold
        self.patterns = defaultdict(int)
        self.files = []
        self.macros = {}
        self.nlp = spacy.load('en_core_web_sm')
    
    def _parse_file_content(self, file_path: Path) -> str:
        """Parse file content based on its format."""
        content = file_path.read_text()
        suffix = file_path.suffix.lower()
        
        if suffix == '.json':
            try:
                data = json.loads(content)
                return json.dumps(data, indent=None)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON content in {file_path}")
        elif suffix in ['.yaml', '.yml']:
            try:
                data = yaml.safe_load(content)
                return yaml.dump(data)
            except yaml.YAMLError:
                raise ValueError(f"Invalid YAML content in {file_path}")
        elif suffix == '.py':
            # Remove comments and normalize whitespace
            lines = [line.strip() for line in content.split('\n') if not line.strip().startswith('#')]
            return ' '.join(lines)
        else:
            return content
    
    def _analyze_file(self, content: str) -> None:
        """Analyze file content for repeated patterns using NLP."""
        doc = self.nlp(content)
        for sent in doc.sents:
            if len(str(sent).split()) >= 3:  # Only consider phrases of 3+ words
                self.patterns[str(sent).strip()] += 1
    
    def scan_repository(self) -> Dict[str, Any]:
        """Scan repository for patterns."""
        for path in self.scan_paths:
            for file_path in path.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    try:
                        content = self._parse_file_content(file_path)
                        self._analyze_file(content)
                        self.files.append(str(file_path))
                    except Exception as e:
                        raise ValueError(f"Error processing {file_path}: {str(e)}")
        
        return {
            'files': self.files,
            'patterns': dict(self.patterns)
        }
    
    def _get_top_patterns(self) -> List[str]:
        """Get patterns that appear more than the threshold times."""
        return [p for p, count in self.patterns.items() 
                if count >= self.macro_threshold]
    
    def generate_macros(self) -> Dict[str, str]:
        """Generate macro definitions for repeated patterns."""
        top_patterns = self._get_top_patterns()
        for i, pattern in enumerate(top_patterns):
            macro_name = f"MACRO_{i + 1}"
            self.macros[macro_name] = pattern
        return self.macros
    
    def apply_macros(self, content: str) -> str:
        """Apply macros to content."""
        result = content
        for macro_name, pattern in self.macros.items():
            result = result.replace(pattern, f"${macro_name}")
        return result
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate optimization report."""
        return {
            'scan_paths': [str(p) for p in self.scan_paths],
            'macro_threshold': self.macro_threshold,
            'files_processed': len(self.files),
            'patterns_found': len(self.patterns),
            'macros_generated': len(self.macros),
            'macros': self.macros,
            'pattern_counts': dict(self.patterns)
        } 