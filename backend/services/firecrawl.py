from firecrawl import FirecrawlApp
import os
from typing import Dict, Any
import re

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")
        
        self.app = FirecrawlApp(api_key=api_key)
    
    def scrape_documentation(self, url: str) -> Dict[str, Any]:
        """
        Scrape a documentation page and extract meaningful content.
        """
        try:
            scrape_params = {
                'formats': ['markdown'],  
                'onlyMainContent': True,  # Skip navigation, ads, etc.
                'includeTags': [
                    'article', 'main', '.content', '.documentation', 
                    '.docs', '.markdown-body'
                ],
                'excludeTags': [         
                    'nav', 'footer', '.sidebar', '.menu', '.breadcrumb'
                ],
                'waitFor': 2000          # Wait 2s for JavaScript to load
            }
            
            result = self.app.scrape_url(url, params=scrape_params)
            
            if not result or not result.get('success'):
                return {"error": "Failed to scrape URL", "url": url}
            
            data = result.get('data', {})
            markdown_content = data.get('markdown', '')
            metadata = data.get('metadata', {})
            
            # Analyze the content to extract API-specific information
            analysis = self._analyze_content(markdown_content)
            
            return {
                "success": True,
                "url": url,
                "title": metadata.get('title', 'Unknown'),
                "content": markdown_content,
                "content_length": len(markdown_content),
                "analysis": analysis,
                "metadata": metadata
            }
            
        except Exception as e:
            return {"error": str(e), "url": url}
    
    def _analyze_content(self, content: str) -> Dict[str, Any]:
        """
        Extract key information from documentation content.
        
        This method looks for patterns common in API documentation:
        - HTTP methods and endpoints (GET /api/users)
        - Code blocks (examples, snippets)
        - Section headers (structure understanding)
        - Important terms (usually in bold)
        """
        analysis = {
            "api_endpoints": [],
            "code_blocks": 0,
            "sections": [],
            "key_concepts": []
        }
        
        # Find API endpoints using common patterns
        endpoint_patterns = [
            r'(?:GET|POST|PUT|DELETE|PATCH|OPTIONS)\s+[/\w\-\{\}\.]+',  # HTTP method + path
            r'https?://[^\s]+/api[^\s]*',                                # Full API URLs
            r'/api/[v\d/]*\w+[/\w\-\{\}]*'                              # API paths
        ]
        
        for pattern in endpoint_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            analysis["api_endpoints"].extend(matches)
        
        # Remove duplicates and limit results
        analysis["api_endpoints"] = list(set(analysis["api_endpoints"]))[:20]
        
        # Count code blocks (indicates how example-heavy the docs are)
        analysis["code_blocks"] = len(re.findall(r'```[\s\S]*?```', content))
        # Extract section headers (document structure)
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        analysis["sections"] = headers[:15]
        # Find key concepts (terms emphasized with bold)
        bold_text = re.findall(r'\*\*(.*?)\*\*', content)
        # Filter out single characters and common words
        key_concepts = [
            term.strip() for term in bold_text 
            if len(term.strip()) > 2 and not term.strip().lower() in ['the', 'and', 'for', 'with']
        ]
        analysis["key_concepts"] = list(set(key_concepts))[:10]
        
        return analysis