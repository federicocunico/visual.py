import numpy as np
from .vector3 import Vector3
from .skeleton import Skeleton
from ..pydantic_ext import BaseModel


class CurrentState(BaseModel):
    title: str | None = None
    points: list[Vector3] = []
    skeletons: list[Skeleton] = []

    ### Clear function
    def clear(self):
        self.clear_points()
        self.clear_skeletons()

    def clear_points(self):
        self.points = []

    def clear_skeletons(self):
        self.skeletons = []

    ### Add to state
    def add_points(self, points: np.ndarray):
        points = [Vector3.from_numpy(p) for p in points]
        self.points.extend(points)

    def add_skeleton(self, skeleton: Skeleton):
        self.skeletons.append(skeleton)

    ### Dumping data to frontend
    def dump(self):
        return self.model_dump()
