from fastapi import FastAPI

app = FastAPI()
#minor
@app.get("/")
async def health_check():
    return {"status": "healthy"}