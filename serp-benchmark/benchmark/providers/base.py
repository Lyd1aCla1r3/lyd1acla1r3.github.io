from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseProvider(ABC):
    """
    Abstract base class for all SERP API providers.
    Enforces a consistent interface for benchmarking.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the provider."""
        pass

    @abstractmethod
    def search(self, query: str) -> Dict[str, Any]:
        """
        Executes a search query and returns the raw JSON response from the API.
        This handles any two-step logic (like fetching async AI overviews) internally.
        """
        pass

    @abstractmethod
    def extract_ai_overview(self, raw_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extracts the AI Overview from the raw response and normalizes it to a standard schema.
        
        Standard Schema:
        {
            "present": bool,
            "summary": str,
            "text_blocks": list[str],
            "citations": list[dict{"url": str, "title": str, "snippet": str}],
            "related_searches": list[str]
        }
        """
        pass
