from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.prediction import Prediction
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserLogin, UserOut
from app.schemas.news import AnalyticsSummary, NewsRequest, NewsPredictionResponse
from app.services.model_service import model_service

router = APIRouter()


@router.post("/auth/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/auth/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return Token(access_token=create_access_token(user.email))


@router.post("/predict", response_model=NewsPredictionResponse)
def predict_news(
    payload: NewsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = model_service.predict(payload.title, payload.content)
    prediction = Prediction(
        title=payload.title,
        content=payload.content,
        label=result["label"],
        confidence=result["confidence"],
        user_id=current_user.id,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("/analytics", response_model=AnalyticsSummary)
def analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Prediction).filter(Prediction.user_id == current_user.id)
    total = q.count()
    fake_count = q.filter(Prediction.label == "FAKE").count()
    real_count = q.filter(Prediction.label == "REAL").count()
    avg_conf = q.with_entities(func.avg(Prediction.confidence)).scalar() or 0.0
    return AnalyticsSummary(
        total_predictions=total,
        fake_count=fake_count,
        real_count=real_count,
        fake_ratio=(fake_count / total) if total else 0.0,
        average_confidence=float(avg_conf),
    )


@router.post("/train")
def train_model(
    dataset: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if not dataset.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload CSV only")

    tmp_path = f"/tmp/{dataset.filename}"
    with open(tmp_path, "wb") as file_out:
        file_out.write(dataset.file.read())

    metrics = model_service.train(tmp_path)
    return {"message": "Model retrained successfully", "metrics": metrics, "user": current_user.email}
