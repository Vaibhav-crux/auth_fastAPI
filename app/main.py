from fastapi import FastAPI
from app.api.user import router as user_router
from app.db.database import engine, Base
from app.utils.logger import get_logger
from app.middleware.corsMiddleware import setup_cors  # Import the CORS setup function

logger = get_logger()

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Apply CORS middleware
setup_cors(app)

app.include_router(user_router)

# Example usage of logger
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")