# pybaseball-api-service

A FastAPI-based service layer for querying datasets available through [pybaseball](https://github.com/jldbc/pybaseball).

## Getting Started

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Visit http://localhost:8000/docs for interactive Swagger docs.

### Attribution

This project uses data provided by [pybaseball](https://github.com/jldbc/pybaseball), which sources information from Baseball Savant, FanGraphs, Baseball Reference, and other public sources. We are not affiliated with MLB or any of these data providers.
