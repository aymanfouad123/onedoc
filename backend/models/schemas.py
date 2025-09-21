from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class DocumentationRequest(BaseModel):
    url: HttpUrl

class DocumentationAnalysis(BaseModel):
    api_endpoints: List[str] = []
    code_blocks: int = 0
    sections: List[str] = []
    key_concepts: List[str] = []

class DocumentationResponse(BaseModel):
    success: bool
    url: str
    title: Optional[str] = None
    content_summary: Optional[str] = None
    analysis: DocumentationAnalysis
    error: Optional[str] = None