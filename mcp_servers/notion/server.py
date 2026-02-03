"""
Notion MCP Server

MCP server for saving crypto research reports to Notion.
"""

import asyncio
import json
import sys
from typing import Any, Optional

from mcp_servers.notion.client import NotionClient


# Tool definitions
TOOLS = [
    {
        "name": "save_report_to_notion",
        "description": """Save a crypto research report to Notion database.

Creates a new page in the configured Notion database with the report content,
token symbol, confidence level, and sentiment rating.

Requires NOTION_API_KEY and NOTION_DATABASE_ID environment variables.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "Cryptocurrency token symbol (e.g., 'BTC', 'ETH')"
                },
                "report_content": {
                    "type": "string",
                    "description": "Full markdown report content"
                },
                "confidence": {
                    "type": "string",
                    "enum": ["High", "Medium", "Low"],
                    "description": "Confidence level of the analysis"
                },
                "sentiment": {
                    "type": "string",
                    "enum": ["Bullish", "Neutral", "Bearish"],
                    "description": "Overall sentiment from the analysis"
                }
            },
            "required": ["token", "report_content"]
        }
    },
    {
        "name": "search_notion_reports",
        "description": """Search for existing crypto research reports in Notion.

Searches the connected Notion workspace for pages matching the query.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g., token symbol or topic)"
                }
            },
            "required": ["query"]
        }
    }
]


class NotionMCPHandler:
    """
    MCP request handler for Notion operations.
    """
    
    def __init__(self, api_key: Optional[str] = None, database_id: Optional[str] = None):
        """
        Initialize the handler.
        
        Args:
            api_key: Notion API key
            database_id: Default database ID for reports
        """
        self.api_key = api_key
        self.database_id = database_id
        self._client: Optional[NotionClient] = None
    
    @property
    def client(self) -> NotionClient:
        """Lazy initialization of the client."""
        if self._client is None:
            self._client = NotionClient(self.api_key, self.database_id)
        return self._client
    
    @property
    def is_configured(self) -> bool:
        """Check if Notion is properly configured."""
        import os
        return bool(
            (self.api_key or os.getenv("NOTION_API_KEY")) and
            (self.database_id or os.getenv("NOTION_DATABASE_ID"))
        )
    
    async def close(self):
        """Close the client connection."""
        if self._client is not None:
            await self._client.close()
            self._client = None
    
    def list_tools(self) -> list[dict]:
        """Return list of available tools."""
        return TOOLS
    
    async def handle_tool_call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Handle a tool call request.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool result as a dictionary
        """
        if not self.is_configured:
            return {
                "error": "Notion not configured",
                "message": "Set NOTION_API_KEY and NOTION_DATABASE_ID environment variables"
            }
        
        try:
            if tool_name == "save_report_to_notion":
                return await self._save_report(arguments)
            elif tool_name == "search_notion_reports":
                return await self._search_reports(arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def _save_report(self, args: dict) -> dict:
        """Save a research report to Notion."""
        token = args.get("token")
        report_content = args.get("report_content")
        confidence = args.get("confidence", "Medium")
        sentiment = args.get("sentiment", "Neutral")
        
        if not token or not report_content:
            return {"error": "Missing required arguments: token and report_content"}
        
        try:
            result = await self.client.create_report_page(
                token=token,
                report_content=report_content,
                confidence=confidence,
                sentiment=sentiment
            )
            
            return {
                "success": True,
                "page_id": result.get("id"),
                "url": result.get("url"),
                "message": f"Report saved to Notion: {result.get('url')}"
            }
        except Exception as e:
            return {"error": f"Failed to save to Notion: {str(e)}"}
    
    async def _search_reports(self, args: dict) -> dict:
        """Search for existing reports in Notion."""
        query = args.get("query")
        
        if not query:
            return {"error": "Missing required argument: query"}
        
        try:
            results = await self.client.search(query)
            
            pages = []
            for result in results:
                if result.get("object") == "page":
                    title = ""
                    if "properties" in result and "Name" in result["properties"]:
                        title_prop = result["properties"]["Name"]
                        if "title" in title_prop and title_prop["title"]:
                            title = title_prop["title"][0].get("plain_text", "")
                    
                    pages.append({
                        "id": result.get("id"),
                        "title": title,
                        "url": result.get("url"),
                        "created": result.get("created_time"),
                    })
            
            return {
                "success": True,
                "query": query,
                "results": pages,
                "count": len(pages)
            }
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}


def format_tools_for_claude() -> list[dict]:
    """Format tools for Claude's tool_use feature."""
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["input_schema"]
        }
        for tool in TOOLS
    ]