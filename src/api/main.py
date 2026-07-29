from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

from .routers import health, companies, portfolio, screener, peers, valuation

app = FastAPI(
    title="Nifty100 Financial Intelligence API",
    version="1.0.0"
)

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



@app.middleware("http")
async def log_requests(request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    print(

        request.method,

        request.url.path,

        f"{duration:.3f}s"

    )

    return response


app.include_router(
    health.router,
    prefix="/api/v1"
)

app.include_router(
    companies.router,
    prefix="/api/v1"
)

app.include_router(
    portfolio.router,
    prefix="/api/v1"
)

app.include_router(
    screener.router,
    prefix="/api/v1"
)

app.include_router(
    peers.router,
    prefix="/api/v1"
)

app.include_router(
    valuation.router,
    prefix="/api/v1"
)

