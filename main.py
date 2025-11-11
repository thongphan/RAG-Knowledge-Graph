import uvicorn
from fastapi import FastAPI
from api.v1 import healthcare_router

app = FastAPI(
    title="Healthcare Graph API",
    version="1.0.0",
    description="API to manage healthcare graph ingestion using Neo4j & PostgreSQL"
)

app.include_router(healthcare_router.router)

@app.get("/api/v1/health")
async def health_check():
    return {"status": "OK", "version": app.version}

@app.get("/api/v1")
async def root():
    return {"message": "Hello from HealthCare"}

if __name__ == "__main__":
      uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
