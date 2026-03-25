import json
from app.services.path_service import generate_path
from app.core.database import SessionLocal
from app.models.trajectory import Trajectory
from app.utils.logger import logger

def process_trajectory(width, height, obstacles):
    logger.info("Worker started processing...")

    db = SessionLocal()

    try:
        path = generate_path(width, height, obstacles)

        traj = Trajectory(
            width=width,
            height=height,
            obstacles=json.dumps(obstacles),
            path=json.dumps(path)
        )

        db.add(traj)
        db.commit()
        db.refresh(traj)

        logger.info(f"Trajectory saved with ID {traj.id}")

        return {"id": traj.id, "path": path}

    finally:
        db.close()