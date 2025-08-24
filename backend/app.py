from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import joblib
from pathlib import Path
from datetime import datetime
import time
import os
from typing import Optional
from dotenv import load_dotenv
import traceback
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# env vars from .env - DB host, user, password and name
load_dotenv()

# Database settings from env
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DB_PORT = os.getenv("DB_PORT", "5432")  # default to 5432 if missing

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# SQLAlchemy to set up connection to RDS
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# logging predictions
class PredictionLog(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_text = Column(String, nullable=False)
    predicted = Column(String, nullable=False)
    true_label = Column(String, nullable=True)
    prediction_latency_ms = Column(Float, nullable=True)


# create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Set up API
# FastAPI app
app = FastAPI()

# load ml model
MODEL_PATH = Path(__file__).parent / "toxicity_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")


# pydantic
class TextInput(BaseModel):
    text: str = Field(..., min_length=1)
    true_label: Optional[str] = None


class PredictionResponse(BaseModel):
    prediction: str


# get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API ENDPOINTS -----
@app.get("/")
def root():
    return {"message": "Welcome to the Toxic Comment Classification API!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(input: TextInput, db: Session = Depends(get_db)):
    try:
        start_time = time.time()
        # use model to make predicitons
        pred_raw = model.predict([input.text])[0]
        pred = str(pred_raw)
        # latency to graph later in monitoring dashboard
        latency = (time.time() - start_time) * 1000

        log_entry = PredictionLog(
            input_text=input.text,
            predicted=pred,
            true_label=input.true_label,
            prediction_latency_ms=latency,
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        # return prediction
        return {"prediction": pred}

    except Exception as e:
        # log traceback error to help w debugging
        tb = traceback.format_exc()
        print(f"Error during prediction or DB commit:\n{e}\n{tb}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
