import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from api.product_api import product_router
from core.database import Base, engine
from core.limiter import limiter

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(product_router)

# "Create all tables registered under this Base metadata"
# like spring.jpa.hibernate.ddl-auto=update
# creates ALL tables automatically.
Base.metadata.create_all(bind=engine)


@app.get("/")
async def greeting():
    return {"message": "Welcome to home page"}
#--------------------------------------------

#   lifespan events (startup/shutdown) in FastAPI

@app.on_event("startup")
def startup_event():
   print("Application started........")

@app.on_event("shutdown")
def shutdown_event():
   print("Application stopped........")

# ----------------------------------------
# Rate limiting with slowapi
app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

#---------------
#    middleware in FastAPI - A middleware is a function that runs before and after each request.
#    It can be used to perform tasks such as logging, authentication, and rate limiting.
@app.middleware("http")
async def log_request_time(request: Request, call_next):
   start_time = time.time()
   response = await call_next(request)
   process_time = time.time() - start_time
   response.headers["X-Process-Time"] = str(process_time)
   print("Request processing time: {} seconds".format(process_time))
   return response
#-----------------------------