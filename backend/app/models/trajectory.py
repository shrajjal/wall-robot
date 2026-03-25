from sqlalchemy import Column, Integer, Text
from app.core.database import Base

class Trajectory(Base):
    __tablename__ = "trajectories"

    id = Column(Integer, primary_key=True, index=True)
    width = Column(Integer)
    height = Column(Integer)
    obstacles = Column(Text)
    path = Column(Text)