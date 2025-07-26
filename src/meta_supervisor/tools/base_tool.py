from abc import ABC, abstractmethod
from typing import Any
from langchain.tools import BaseTool
from pydantic import Field


class BaseAPITool(BaseTool, ABC):
    """
    Base class for API-based tools in the meta-supervisor.
    """
    
    client: Any = Field(default=None, exclude=True)
    
    def __init__(self, client=None, **kwargs):
        super().__init__(**kwargs)
        self.__dict__['client'] = client
    
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