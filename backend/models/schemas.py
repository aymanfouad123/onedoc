from typing import Dict, List, Optional
from pydantic import BaseModel, HttpUrl

class DocumentationRequest(BaseModel):
    # Request to scrape documentation from a given URL
    url: HttpUrl
    
class PageRecord(BaseModel):
    # Individual page metadata for tracking what was scraped
    url: str
    title: Optional[str]
    type: str  # api_ref | function | guide | concept | junk
    priority: str = "should"
    content_hash: Optional[str]

class APIParam(BaseModel):
    # Parameter definition for API endpoints and functions
    name: str
    type: str
    required: bool
    location: str
    description: Optional[str]

class CodeSample(BaseModel):
    # Code example with language and source code
    lang: str
    code: str

class EndpointDoc(BaseModel):
    # Structured documentation for API endpoints
    url: str
    method: str
    path: str
    description: Optional[str]
    params: List[APIParam]
    request_schema: Optional[Dict]
    response_schema: Optional[Dict]
    samples: List[CodeSample]

class FunctionDoc(BaseModel):
    # Documentation for functions and methods
    url: str
    name: str
    signature: Optional[str]
    args: List[APIParam]
    returns: Optional[str]
    samples: List[CodeSample]

class GuideChunk(BaseModel):
    # Segmented guide content with heading and markdown text
    url: str
    heading: str
    text_md: str
    samples: List[CodeSample]

class IngestionResult(BaseModel):
    # Complete result of documentation scraping and processing
    inventory: List[PageRecord]
    endpoint_docs: List[EndpointDoc]
    function_docs: List[FunctionDoc]
    guide_chunks: List[GuideChunk]
    coverage: Dict