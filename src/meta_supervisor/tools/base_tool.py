from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class BaseAPITool(BaseTool, ABC):
    """
    Base class for API-based tools in the meta-supervisor.
    """
    
    def __init__(self, client, **kwargs):
        super().__init__(**kwargs)
        self.client = client
    
    @abstractmethod
    async def _arun(self, **kwargs) -> Any:
        """
        Async implementation of the tool.
        """
        pass
    
    def _run(self, **kwargs) -> Any:
        """
        Sync implementation - not supported for async tools.
        """
        raise NotImplementedError("This tool only supports async execution")