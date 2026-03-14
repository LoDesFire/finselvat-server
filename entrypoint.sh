#!/bin/bash
alembic upgrade head &&
exec uvicorn src.web.main:app --host 0.0.0.0 --port 8000