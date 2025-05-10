"""
Repository Scanner - A module for scanning repositories for prompts and analyzing their usage.
"""

import fnmatch
import json
import logging
import os
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


@dataclass
class FileAnalysis:
    """Analysis result for a single file."""

    file_path: Path
    prompts_found: List[Dict[str, Any]]
    prompt_types: Set[str]
    line_count: int
    prompt_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RepositoryAnalysis:
    """Analysis result for an entire repository."""

    repository_path: Path
    file_analyses: List[FileAnalysis]
    total_files: int
    total_prompts: int
    prompt_type_distribution: Dict[str, int]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScanResult:
    """Result of repository scan."""

    repository_path: Path
    found_prompts: List[Dict[str, Any]]
    file_stats: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class PromptLocation:
    """Data class for storing prompt location information."""

    file_path: str
    line_number: int
    context: str
    prompt_text: str
    language: str


class RepositoryScanner:
    """Scans code repositories for prompts."""

    def __init__(self, max_workers: int = 4):
        """Initialize the repository scanner.

        Args:
            max_workers: Maximum number of parallel workers
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        # Common prompt patterns
        self.prompt_patterns = {
            "python": [
                r'prompt\s*=\s*["\'](.*?)["\']',
                r'prompt_text\s*=\s*["\'](.*?)["\']',
                r'PROMPT\s*=\s*["\'](.*?)["\']',
            ],
            "javascript": [
                r'prompt\s*=\s*["\'](.*?)["\']',
                r'promptText\s*=\s*["\'](.*?)["\']',
                r'PROMPT\s*=\s*["\'](.*?)["\']',
            ],
            "typescript": [
                r'prompt\s*=\s*["\'](.*?)["\']',
                r'promptText\s*=\s*["\'](.*?)["\']',
                r'PROMPT\s*=\s*["\'](.*?)["\']',
            ],
            "java": [
                r'String\s+prompt\s*=\s*["\'](.*?)["\']',
                r'String\s+promptText\s*=\s*["\'](.*?)["\']',
                r'String\s+PROMPT\s*=\s*["\'](.*?)["\']',
            ],
            "kotlin": [
                r'val\s+prompt\s*=\s*["\'](.*?)["\']',
                r'val\s+promptText\s*=\s*["\'](.*?)["\']',
                r'val\s+PROMPT\s*=\s*["\'](.*?)["\']',
            ],
        }

        # File extensions for each language
        self.language_extensions = {
            "python": [".py"],
            "javascript": [".js"],
            "typescript": [".ts", ".tsx"],
            "java": [".java"],
            "kotlin": [".kt"],
        }

    def scan_repository(self, repo_path: str) -> List[PromptLocation]:
        """Scan a repository for prompts.

        Args:
            repo_path: Path to the repository

        Returns:
            List of found prompt locations
        """
        repo_path = Path(repo_path)
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")

        # Find all relevant files
        files_to_scan = []
        for language, extensions in self.language_extensions.items():
            for ext in extensions:
                files_to_scan.extend(repo_path.rglob(f"*{ext}"))

        # Scan files in parallel
        futures = []
        for file_path in files_to_scan:
            futures.append(self.executor.submit(self._scan_file, str(file_path)))

        # Collect results
        prompt_locations = []
        for future in futures:
            prompt_locations.extend(future.result())

        return prompt_locations

    def _scan_file(self, file_path: str) -> List[PromptLocation]:
        """Scan a single file for prompts.

        Args:
            file_path: Path to the file to scan

        Returns:
            List of prompt locations found in the file
        """
        prompt_locations = []

        # Determine language from file extension
        language = self._get_language_from_file(file_path)
        if not language:
            return prompt_locations

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()

                # Check each pattern for the language
                for pattern in self.prompt_patterns[language]:
                    for i, line in enumerate(lines, 1):
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            # Get some context around the prompt
                            start = max(0, i - 2)
                            end = min(len(lines), i + 2)
                            context = "\n".join(lines[start:end])

                            prompt_locations.append(
                                PromptLocation(
                                    file_path=file_path,
                                    line_number=i,
                                    context=context,
                                    prompt_text=match.group(1),
                                    language=language,
                                )
                            )
        except Exception as e:
            print(f"Error scanning file {file_path}: {str(e)}")

        return prompt_locations

    def _get_language_from_file(self, file_path: str) -> Optional[str]:
        """Get the programming language from a file path.

        Args:
            file_path: Path to the file

        Returns:
            Language name if recognized, None otherwise
        """
        ext = os.path.splitext(file_path)[1].lower()
        for language, extensions in self.language_extensions.items():
            if ext in extensions:
                return language
        return None

    def get_scan_stats(self, prompt_locations: List[PromptLocation]) -> Dict[str, Union[int, Dict[str, int]]]:
        """Get statistics about the scan results.

        Args:
            prompt_locations: List of prompt locations found

        Returns:
            Dictionary containing scan statistics
        """
        if not prompt_locations:
            return {}

        # Count prompts by language
        language_counts = {}
        for location in prompt_locations:
            language_counts[location.language] = language_counts.get(location.language, 0) + 1

        return {
            "total_prompts": len(prompt_locations),
            "prompts_by_language": language_counts,
            "unique_files": len(set(loc.file_path for loc in prompt_locations)),
        }

    def scan_repository(
        self,
        repository_path: Union[str, Path],
        scan_params: Optional[Dict[str, Any]] = None,
    ) -> ScanResult:
        """Scan a repository for prompts.

        Args:
            repository_path (Union[str, Path]): Path to repository.
            scan_params (Optional[Dict[str, Any]]): Scan parameters.

        Returns:
            ScanResult: Scan result.
        """
        params = scan_params or {}
        repo_path = Path(repository_path)

        # Get files to scan
        files_to_scan = self._get_files_to_scan(repo_path, params)

        # Scan files for prompts
        found_prompts = []
        file_stats = {
            "total_files": len(files_to_scan),
            "scanned_files": 0,
            "files_with_prompts": 0,
        }

        with ThreadPoolExecutor(max_workers=params.get("max_workers", 4)) as executor:
            futures = [executor.submit(self._scan_file, file_path, params) for file_path in files_to_scan]

            for future in as_completed(futures):
                try:
                    file_result = future.result()
                    if file_result["prompts"]:
                        found_prompts.extend(file_result["prompts"])
                        file_stats["files_with_prompts"] += 1
                    file_stats["scanned_files"] += 1
                except Exception as e:
                    logger.error(f"Error scanning file: {e}")

        # Create result
        result = ScanResult(
            repository_path=repo_path,
            found_prompts=found_prompts,
            file_stats=file_stats,
            metadata={"scan_params": params, "scan_timestamp": self._get_timestamp()},
        )

        self.scan_history.append(result)
        return result

    def get_scan_stats(self) -> Dict[str, Any]:
        """Get statistics about scans.

        Returns:
            Dict[str, Any]: Scan statistics.
        """
        if not self.scan_history:
            return {}

        # Calculate total stats
        total_files = sum(result.file_stats["total_files"] for result in self.scan_history)
        total_prompts = sum(len(result.found_prompts) for result in self.scan_history)

        # Calculate prompt type distribution
        prompt_types = defaultdict(int)
        for result in self.scan_history:
            for prompt in result.found_prompts:
                prompt_types[prompt["type"]] += 1

        return {
            "total_scans": len(self.scan_history),
            "total_files_scanned": total_files,
            "total_prompts_found": total_prompts,
            "prompt_type_distribution": dict(prompt_types),
        }

    def export_results(self, output_path: Path) -> None:
        """Export scan results to a file.

        Args:
            output_path (Path): Path to save results.
        """
        results_data = {
            "statistics": self.get_scan_stats(),
            "results": [
                {
                    "repository_path": str(result.repository_path),
                    "found_prompts": result.found_prompts,
                    "file_stats": result.file_stats,
                    "metadata": result.metadata,
                }
                for result in self.scan_history
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2)

    def _load_prompt_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load prompt patterns.

        Returns:
            Dict[str, Dict[str, Any]]: Prompt patterns.
        """
        return {
            "openai": {
                "pattern": r"(?:system|user|assistant):\s*([^\n]+)",
                "type": "openai",
                "description": "OpenAI chat format",
            },
            "anthropic": {
                "pattern": r"(?:Human|Assistant):\s*([^\n]+)",
                "type": "anthropic",
                "description": "Anthropic chat format",
            },
            "cohere": {
                "pattern": r"(?:User|Assistant):\s*([^\n]+)",
                "type": "cohere",
                "description": "Cohere chat format",
            },
            "generic": {
                "pattern": r"(?:prompt|instruction|query):\s*([^\n]+)",
                "type": "generic",
                "description": "Generic prompt format",
            },
            "code": {
                "pattern": r"```(?:python|javascript|typescript)\n(.*?)\n```",
                "type": "code",
                "description": "Code block",
            },
        }

    def _get_files_to_scan(self, repo_path: Path, params: Dict[str, Any]) -> List[Path]:
        """Get files to scan.

        Args:
            repo_path (Path): Repository path.
            params (Dict[str, Any]): Scan parameters.

        Returns:
            List[Path]: List of files to scan.
        """
        include_patterns = params.get("include_patterns", ["*.py", "*.js", "*.ts"])
        exclude_patterns = params.get("exclude_patterns", ["venv", "__pycache__"])

        files_to_scan = []

        for root, dirs, files in os.walk(repo_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)]

            # Add matching files
            for file in files:
                if any(fnmatch.fnmatch(file, pattern) for pattern in include_patterns):
                    files_to_scan.append(Path(root) / file)

        return files_to_scan

    def _scan_file(self, file_path: Path, params: Dict[str, Any]) -> Dict[str, Any]:
        """Scan a file for prompts.

        Args:
            file_path (Path): File to scan.
            params (Dict[str, Any]): Scan parameters.

        Returns:
            Dict[str, Any]: Scan result.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            prompts = []

            # Check each pattern
            for pattern_name, pattern_info in self.prompt_patterns.items():
                matches = re.finditer(pattern_info["pattern"], content, re.MULTILINE | re.DOTALL)

                for match in matches:
                    prompts.append(
                        {
                            "type": pattern_info["type"],
                            "content": match.group(1).strip(),
                            "line_number": content[: match.start()].count("\n") + 1,
                            "file_path": str(file_path),
                            "pattern": pattern_name,
                        }
                    )

            return {"file_path": str(file_path), "prompts": prompts}

        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            return {"file_path": str(file_path), "prompts": []}

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().isoformat()
