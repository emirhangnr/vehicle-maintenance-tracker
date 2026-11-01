from fastapi import FastAPI

app = FastAPI(title="Vehicle Maintenance Tracker")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
