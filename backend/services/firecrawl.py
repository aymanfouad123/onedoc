from firecrawl import FirecrawlApp
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")

        self.app = FirecrawlApp(api_key=api_key)

    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from a URL using Firecrawl.
        """
        try:
            result = self.app.scrape(url)

            if not result:
                return {"error": "Failed to scrape URL", "url": url}

            markdown_content = getattr(result, 'markdown', getattr(result, 'content', ''))
            metadata = getattr(result, 'metadata', {})

            return {
                "success": True,
                "url": url,
                "title": getattr(metadata, 'title', 'Unknown') if hasattr(metadata, 'title') else metadata.get('title', 'Unknown'),
                "content": markdown_content,
                "metadata": metadata.__dict__ if hasattr(metadata, '__dict__') else metadata
            }

        except Exception as e:
            return {"error": str(e), "url": url}

    def crawl(self, root_url: str, depth: int = 4) -> List[str]:
        """
        Crawl site and return list of URLs found.
        Uses Firecrawl's official crawl API.
        """
        try:
            # Use Firecrawl's crawl method with correct parameters
            docs = self.app.crawl(
                url=root_url,
                limit=depth * 15,  # Estimate pages based on depth
                scrape_options={
                    'formats': ['markdown'],
                    'onlyMainContent': True
                }
            )

            # Extract URLs from crawled documents
            if not docs:
                return []

            return [doc.get('url', '') for doc in docs if doc.get('url')]

        except Exception as e:
            print(f"Crawl error: {e}")
            return []