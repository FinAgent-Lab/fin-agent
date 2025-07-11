#!/bin/bash
uv run uvicorn src.meta_supervisor.main:app --host 0.0.0.0 --port 8000 --reload 