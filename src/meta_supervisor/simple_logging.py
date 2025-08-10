import json
import logging
import time
import uuid
from typing import Callable, Optional
from datetime import datetime, timezone

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Setup logger
logger = logging.getLogger("http_middleware")
logger.setLevel(logging.INFO)

# Add console handler if not already present
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class SimpleLoggingMiddleware(BaseHTTPMiddleware):
    """Simple HTTP request/response logging middleware for FastAPI."""
    
    def __init__(self, app, exclude_paths: Optional[list] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/health", "/", "/docs", "/redoc", "/openapi.json"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip logging for health checks and docs
        if request.url.path in self.exclude_paths:
            return await call_next(request)
        
        # Generate correlation ID
        correlation_id = f"req-{uuid.uuid4().hex[:8]}"
        
        # Start timer
        start_time = time.perf_counter()
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Log request
        request_body = await self._get_request_body(request)
        request_log = {
            "timestamp": timestamp,
            "correlation_id": correlation_id,
            "event": "request",
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", "unknown")[:100],
            "body": self._filter_sensitive_data(request_body)
        }
        logger.info(json.dumps(request_log, ensure_ascii=False))
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        # Log response
        response_body = await self._get_response_body(response)
        response_log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "correlation_id": correlation_id,
            "event": "response", 
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
            "body": self._filter_sensitive_data(response_body)
        }
        
        # Log at appropriate level
        log_level = logging.ERROR if response.status_code >= 400 else logging.INFO
        logger.log(log_level, json.dumps(response_log, ensure_ascii=False))
        
        # Add correlation ID to response headers
        response.headers["x-correlation-id"] = correlation_id
        
        return response
    
    async def _get_request_body(self, request: Request) -> Optional[str]:
        """Get request body safely."""
        try:
            if request.method in ["POST", "PUT", "PATCH"]:
                body_bytes = await request.body()
                if body_bytes:
                    body_str = body_bytes.decode("utf-8", errors="ignore")
                    # Limit body size for logging
                    return body_str[:500] + "..." if len(body_str) > 500 else body_str
        except Exception:
            pass
        return None
    
    async def _get_response_body(self, response: Response) -> Optional[str]:
        """Get response body safely."""
        try:
            if hasattr(response, 'body') and response.body:
                body_str = response.body.decode("utf-8", errors="ignore")
                # Limit body size for logging  
                return body_str[:500] + "..." if len(body_str) > 500 else body_str
        except Exception:
            pass
        return None
    
    def _filter_sensitive_data(self, data: Optional[str]) -> Optional[str]:
        """Simple filter for sensitive data."""
        if not data:
            return data
        
        # Simple replacements for common sensitive patterns
        import re
        sensitive_patterns = [
            (r'("password"\s*:\s*")[^"]*(")', r'\1***\2'),
            (r'("api_key"\s*:\s*")[^"]*(")', r'\1***\2'), 
            (r'("token"\s*:\s*")[^"]*(")', r'\1***\2'),
            (r'("secret"\s*:\s*")[^"]*(")', r'\1***\2'),
        ]
        
        filtered_data = data
        for pattern, replacement in sensitive_patterns:
            filtered_data = re.sub(pattern, replacement, filtered_data, flags=re.IGNORECASE)
        
        return filtered_data
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check forwarded headers first
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check real IP header
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
            
        # Fall back to client host
        if hasattr(request, "client") and request.client:
            return request.client.host
            
        return "unknown"