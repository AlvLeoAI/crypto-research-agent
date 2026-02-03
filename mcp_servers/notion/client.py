"""
Notion API Client

Client for interacting with Notion API to save research reports.
"""

import os
from typing import Optional
from datetime import datetime

import httpx


class NotionClient:
    """
    Async client for Notion API.
    
    Used to save crypto research reports to a Notion database.
    """
    
    BASE_URL = "https://api.notion.com/v1"
    NOTION_VERSION = "2022-06-28"
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        database_id: Optional[str] = None
    ):
        """
        Initialize the Notion client.
        
        Args:
            api_key: Notion integration token (or set NOTION_API_KEY env var)
            database_id: Default database ID for saving reports (or set NOTION_DATABASE_ID)
        """
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")
        
        if not self.api_key:
            raise ValueError(
                "Notion API key required. Set NOTION_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Notion-Version": self.NOTION_VERSION,
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
    
    async def create_page(
        self,
        title: str,
        content: str,
        database_id: Optional[str] = None,
        properties: Optional[dict] = None
    ) -> dict:
        """
        Create a new page in Notion.
        
        Args:
            title: Page title
            content: Markdown content for the page
            database_id: Database to create page in (uses default if not specified)
            properties: Additional database properties
            
        Returns:
            Created page object from Notion API
        """
        db_id = database_id or self.database_id
        
        if not db_id:
            raise ValueError("Database ID required. Set NOTION_DATABASE_ID or pass database_id.")
        
        # Build the page payload
        payload = {
            "parent": {"database_id": db_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": title}}]
                }
            },
            "children": self._markdown_to_blocks(content)
        }
        
        # Add any additional properties
        if properties:
            payload["properties"].update(properties)
        
        response = await self.client.post("/pages", json=payload)
        response.raise_for_status()
        
        return response.json()
    
    async def create_report_page(
        self,
        token: str,
        report_content: str,
        confidence: str = "Medium",
        sentiment: str = "Neutral",
        database_id: Optional[str] = None
    ) -> dict:
        """
        Create a research report page with standard properties.
        
        Args:
            token: Cryptocurrency token (e.g., "BTC", "ETH")
            report_content: Full markdown report
            confidence: Confidence level (High/Medium/Low)
            sentiment: Overall sentiment (Bullish/Neutral/Bearish)
            database_id: Optional override for database ID
            
        Returns:
            Created page object
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        title = f"{token.upper()} Research Report - {timestamp}"
        
        # Standard properties for crypto research database
        properties = {
            "Token": {
                "select": {"name": token.upper()}
            },
            "Confidence": {
                "select": {"name": confidence}
            },
            "Sentiment": {
                "select": {"name": sentiment}
            },
            "Date": {
                "date": {"start": datetime.utcnow().isoformat()}
            }
        }
        
        return await self.create_page(
            title=title,
            content=report_content,
            database_id=database_id,
            properties=properties
        )
    
    def _markdown_to_blocks(self, markdown: str) -> list[dict]:
        """
        Convert markdown content to Notion blocks.
        
        This is a simplified converter that handles common patterns.
        """
        blocks = []
        lines = markdown.split("\n")
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip empty lines
            if not line.strip():
                i += 1
                continue
            
            # Headers
            if line.startswith("# "):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]
                    }
                })
            elif line.startswith("## "):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:].strip()}}]
                    }
                })
            elif line.startswith("### "):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:].strip()}}]
                    }
                })
            # Bullet points
            elif line.strip().startswith("- ") or line.strip().startswith("• "):
                content = line.strip()[2:].strip()
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                })
            # Numbered lists
            elif line.strip() and line.strip()[0].isdigit() and ". " in line:
                content = line.strip().split(". ", 1)[1] if ". " in line else line.strip()
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                })
            # Horizontal rule
            elif line.strip() in ["---", "***", "___"]:
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
            # Code blocks
            elif line.strip().startswith("```"):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": "\n".join(code_lines)}}],
                        "language": "plain text"
                    }
                })
            # Tables (simplified - convert to text)
            elif line.strip().startswith("|"):
                # Collect all table lines
                table_lines = [line]
                while i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
                    i += 1
                    table_lines.append(lines[i])
                
                # Convert to simple text representation
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "\n".join(table_lines)}}]
                    }
                })
            # Regular paragraph
            else:
                # Collect consecutive non-special lines into one paragraph
                para_lines = [line]
                while (i + 1 < len(lines) and 
                       lines[i + 1].strip() and 
                       not lines[i + 1].startswith("#") and
                       not lines[i + 1].strip().startswith("-") and
                       not lines[i + 1].strip().startswith("•") and
                       not lines[i + 1].strip().startswith("|") and
                       not lines[i + 1].strip().startswith("```") and
                       not lines[i + 1].strip() in ["---", "***", "___"]):
                    i += 1
                    para_lines.append(lines[i])
                
                content = " ".join(para_lines).strip()
                if content:
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": content[:2000]}}]  # Notion limit
                        }
                    })
            
            i += 1
        
        return blocks
    
    async def search(self, query: str) -> list[dict]:
        """
        Search Notion for pages matching query.
        
        Args:
            query: Search query
            
        Returns:
            List of matching pages
        """
        response = await self.client.post(
            "/search",
            json={"query": query, "page_size": 10}
        )
        response.raise_for_status()
        return response.json().get("results", [])
    
    async def get_database(self, database_id: Optional[str] = None) -> dict:
        """
        Get database metadata.
        
        Args:
            database_id: Database ID (uses default if not specified)
            
        Returns:
            Database object
        """
        db_id = database_id or self.database_id
        if not db_id:
            raise ValueError("Database ID required")
        
        response = await self.client.get(f"/databases/{db_id}")
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.close()