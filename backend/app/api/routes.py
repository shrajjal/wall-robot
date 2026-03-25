from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.schemas.trajectory import WallRequest
from app.models.trajectory import Trajectory
from app.services.path_service import generate_path
from app.core.database import SessionLocal
from app.utils.logger import logger

router = APIRouter()


# -------------------------------
# DB Dependency
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# CREATE TRAJECTORY (SYNC)
# -------------------------------
@router.post("/trajectory")
def create_trajectory(req: WallRequest, db: Session = Depends(get_db)):
    try:
        logger.info("Generating path...")

        path = generate_path(req.width, req.height, req.obstacles)

        traj = Trajectory(
            width=req.width,
            height=req.height,
            obstacles=json.dumps([obs.dict() for obs in req.obstacles]),
            path=json.dumps(path)
        )

        db.add(traj)
        db.commit()
        db.refresh(traj)

        return {
            "id": traj.id,
            "path": path
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Error generating path")


# -------------------------------
# GET SINGLE
# -------------------------------
@router.get("/trajectory/{traj_id}")
def get_trajectory(traj_id: int, db: Session = Depends(get_db)):
    traj = db.query(Trajectory).filter(Trajectory.id == traj_id).first()

    if not traj:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "id": traj.id,
        "width": traj.width,
        "height": traj.height,
        "obstacles": json.loads(traj.obstacles),
        "path": json.loads(traj.path)
    }


# -------------------------------
# GET ALL
# -------------------------------
@router.get("/trajectories")
def get_all(db: Session = Depends(get_db)):
    data = db.query(Trajectory).all()

    return [
        {
            "id": t.id,
            "width": t.width,
            "height": t.height,
            "obstacles": json.loads(t.obstacles),
            "path": json.loads(t.path)
        }
        for t in data
    ]