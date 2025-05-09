from typing import Dict, List, Optional
import json
from pathlib import Path
from ..trimmer.domain_aware import DomainAwareTrimmer

class CICDIntegration:
    def __init__(self, max_tokens: int = 1800, build_failure: bool = True, dictionary_path: str = "data/dicts"):
        self.max_tokens = max_tokens
        self.build_failure = build_failure
        self.trimmer = DomainAwareTrimmer(dictionary_path=dictionary_path)
        
    def check_prompt_budget(self, prompt: str) -> Dict:
        """Check if a prompt exceeds the token budget."""
        token_count = self.trimmer.get_token_count(prompt)
        exceeds_budget = token_count > self.max_tokens
        
        result = {
            "token_count": token_count,
            "max_tokens": self.max_tokens,
            "exceeds_budget": exceeds_budget,
            "build_failure": self.build_failure and exceeds_budget
        }
        
        return result
    
    def generate_report(self, prompts: List[str], report_path: str) -> None:
        """Generate a report of prompt token usage."""
        report = {
            "prompts": [],
            "total_tokens": 0,
            "exceeded_budget": False
        }
        
        for prompt in prompts:
            check_result = self.check_prompt_budget(prompt)
            report["prompts"].append({
                "token_count": check_result["token_count"],
                "exceeds_budget": check_result["exceeds_budget"]
            })
            report["total_tokens"] += check_result["token_count"]
            if check_result["exceeds_budget"]:
                report["exceeded_budget"] = True
        
        # Write report to file
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2) 