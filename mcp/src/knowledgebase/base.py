"""Base knowledge base class for WeavScope documentation."""

from pathlib import Path
from typing import Any, Dict, List


class WeavScopeKnowledgeBase:
    """Knowledge base containing WeavScope documentation and examples."""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent.parent
        self._docs_cache = None
        self._examples_cache = None
    
    def get_documentation(self) -> Dict[str, Any]:
        """Get comprehensive WeavScope documentation."""
        if self._docs_cache is None:
            self._docs_cache = self._load_documentation()
        return self._docs_cache
    
    def get_examples(self) -> List[Dict[str, Any]]:
        """Get WeavScope usage examples."""
        if self._examples_cache is None:
            self._examples_cache = self._load_examples()
        return self._examples_cache
    
    def get_api_reference(self) -> Dict[str, Any]:
        """Get API reference for WeavScope."""
        docs = self.get_documentation()
        return docs.get("api_reference", {})
    
    def get_configuration_guide(self) -> Dict[str, Any]:
        """Get configuration guide."""
        docs = self.get_documentation()
        return docs.get("configuration", {})
    
    def _load_documentation(self) -> Dict[str, Any]:
        """Load documentation from various sources."""
        from .documentation import load_documentation
        return load_documentation(self.base_path)
    
    def _load_examples(self) -> List[Dict[str, Any]]:
        """Load usage examples."""
        from .examples import load_examples
        return load_examples()
