import requests
from typing import Dict, Any, Optional
from .base import BaseProvider

class SerperProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "Serper"

    def search(self, query: str) -> Dict[str, Any]:
        """
        Serper endpoint.
        Historically, Serper has focused on speed/cost and may not deeply parse AI overviews.
        We make a standard search request to see if it returns anything resembling it.
        """
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            "q": query,
            "gl": "us",
            "hl": "en"
        }
        response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def extract_ai_overview(self, raw_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Sometimes returned as answerBox or a specific aiOverview block if supported.
        if "answerBox" in raw_response and "ai" in str(raw_response.get("answerBox", {}).get("title", "")).lower():
            # A fallback if they map it to answerBox
            aio = raw_response["answerBox"]
            return {
                "present": True,
                "summary": aio.get("snippet", ""),
                "text_blocks": [],
                "citations": [],
                "related_searches": []
            }
            
        if "aiOverview" in raw_response: # Hypothetical standard key for Serper
            aio = raw_response["aiOverview"]
            return {
                "present": True,
                "summary": aio.get("snippet", ""),
                "text_blocks": [],
                "citations": [],
                "related_searches": []
            }

        return {"present": False, "summary": "", "text_blocks": [], "citations": [], "related_searches": []}
