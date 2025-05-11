"""Repository Scanner - A module for scanning repositories for prompts."""

import fnmatch
import json
import logging
import os
import re
from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Pattern, Set, TypedDict, Union

logger = logging.getLogger(__name__)


class FileAnalysis:
    """A class for analyzing a file."""

    def __init__(self, path: str, prompts: List[Dict[str, Any]]):
        """Initialize file analysis.

        Args:
            path: Path to the file
            prompts: List of prompts found in the file
        """
        self.path = path
        self.prompts = prompts


class RepositoryAnalysis:
    """A class for analyzing a repository."""

    def __init__(self, files: List[FileAnalysis]):
        """Initialize repository analysis.

        Args:
            files: List of analyzed files
        """
        self.files = files


class ScanResult:
    """A class for storing scan results."""

    def __init__(self, analysis: RepositoryAnalysis):
        """Initialize scan result.

        Args:
            analysis: Repository analysis
        """
        self.analysis = analysis


class PromptLocation:
    """A class for storing prompt location information."""

    def __init__(self, file: str, line: int, column: int):
        """Initialize prompt location.

        Args:
            file: Path to the file
            line: Line number
            column: Column number
        """
        self.file = file
        self.line = line
        self.column = column


class PromptPattern(TypedDict):
    """Configuration for a prompt pattern."""

    pattern: str
    description: str


class RepositoryScanner:
    """A class for scanning repositories for prompts."""

    def __init__(self) -> None:
        self.scan_history: List[ScanResult] = []

    def scan_repository(
        self, repo_path: Path, options: Optional[Dict[str, Any]] = None
    ) -> ScanResult:
        """Scan a repository for prompts and analyze them."""
        options = options or {}
        prompt_locations: List[PromptLocation] = []
        file_analyses: List[FileAnalysis] = []

        with ThreadPoolExecutor(max_workers=options.get("max_workers", 4)) as executor:
            futures = []
            for file_path in repo_path.rglob("*"):
                if file_path.is_file():
                    futures.append(
                        executor.submit(self._analyze_file, file_path, options)
                    )

            for future in futures:
                result = future.result()
                if isinstance(result, list):
                    prompt_locations.extend(result)
                elif isinstance(result, dict):
                    file_analyses.append(FileAnalysis(**result))

        analysis = RepositoryAnalysis(
            total_files=len(file_analyses),
            total_prompts=len(prompt_locations),
            file_analyses=file_analyses,
        )

        scan_result = ScanResult(
            repository_analysis=analysis,
            prompt_locations=prompt_locations,
            metadata=options,
        )

        self.scan_history.append(scan_result)
        return scan_result

    def _analyze_file(
        self, file_path: Path, options: Dict[str, Any]
    ) -> Union[List[PromptLocation], Dict[str, Any]]:
        """Analyze a single file for prompts."""
        # Placeholder implementation
        return []

    def get_scan_history(self) -> List[ScanResult]:
        """Get the history of all scans."""
        return self.scan_history

    def _scan_file(
        self, file_path: Path, params: Optional[Dict[str, Any]] = None
    ) -> Union[List[PromptLocation], Dict[str, Any]]:
        """Scan a single file for prompts.

        Args:
            file_path (Path): Path to the file to scan.
            params (Optional[Dict[str, Any]]): Optional parameters for scanning.

        Returns:
            Union[List[PromptLocation], Dict[str, Any]]: List of prompt locations or scan result.
        """
        prompt_locations: List[PromptLocation] = []

        # Determine language from file extension
        language: Optional[str] = self._get_language_from_file(str(file_path))
        if not language:
            return prompt_locations if params is None else {"prompts": [], "stats": {}}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content: str = f.read()
                lines: List[str] = content.splitlines()

                # Check each pattern for the language
                for pattern in self.prompt_patterns[language]:
                    for i, line in enumerate(lines, 1):
                        matches = pattern.finditer(line)
                        for match in matches:
                            # Get some context around the prompt
                            start: int = max(0, i - 2)
                            end: int = min(len(lines), i + 2)
                            context: str = "\n".join(lines[start:end])

                            prompt_locations.append(
                                PromptLocation(
                                    file_path=str(file_path),
                                    line_number=i,
                                    context=context,
                                    prompt_text=match.group(1),
                                    language=language,
                                )
                            )
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {str(e)}")

        if params is None:
            return prompt_locations
        else:
            return {
                "prompts": [loc.__dict__ for loc in prompt_locations],
                "stats": {
                    "total_prompts": len(prompt_locations),
                    "language": language,
                    "line_count": len(lines),
                },
            }

    def _get_language_from_file(self, file_path: str) -> Optional[str]:
        """Get the programming language from a file path.

        Args:
            file_path (str): Path to the file.

        Returns:
            Optional[str]: Language name if recognized, None otherwise.
        """
        ext: str = os.path.splitext(file_path)[1].lower()
        for language, extensions in self.language_extensions.items():
            if ext in extensions:
                return language
        return None

    def get_scan_stats(
        self, prompt_locations: Optional[List[PromptLocation]] = None
    ) -> Dict[str, Any]:
        """Get statistics about the scan results.

        Args:
            prompt_locations (Optional[List[PromptLocation]]): List of prompt locations to analyze.

        Returns:
            Dict[str, Any]: Statistics about the scan results.
        """
        if prompt_locations is None:
            # Return basic stats
            return {
                "total_files_scanned": len(self._get_files_to_scan(Path.cwd(), {})),
                "timestamp": self._get_timestamp(),
            }

        # Calculate statistics from prompt locations
        stats: Dict[str, Any] = {
            "total_prompts": len(prompt_locations),
            "languages": defaultdict(int),
            "files": defaultdict(int),
        }

        for loc in prompt_locations:
            stats["languages"][loc.language] += 1
            stats["files"][loc.file_path] += 1

        return stats

    def export_results(self, output_path: Path) -> None:
        """Export scan results to a file.

        Args:
            output_path (Path): Path to save results.
        """
        results: Dict[str, Any] = {
            "scan_stats": self.get_scan_stats([]),
            "metadata": {"timestamp": self._get_timestamp()},
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            str: ISO format timestamp.
        """
        return datetime.now().isoformat()

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
            dirs[:] = [
                d
                for d in dirs
                if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)
            ]

            # Add matching files
            for file in files:
                if any(fnmatch.fnmatch(file, pattern) for pattern in include_patterns):
                    files_to_scan.append(Path(root) / file)

        return files_to_scan
