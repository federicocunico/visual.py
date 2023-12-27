import time
import numpy as np
from socketio import Client

from src.models.vector3 import Vector3
from .pydantic_ext import BaseModel
from .models import Color, Skeleton, CurrentState


class PyPlot:
    model: CurrentState

    def __init__(self, title: str | None, host: str = "localhost", port: int = 11000):
        self.model = CurrentState(title=title)

        self._socket_url = f"http://{host}:{port}"
        self.client = Client()

    def __health_check(self, xs: list[float], ys: list[float], zs: list[float]):
        assert len(xs) == len(ys), "xs and ys must have the same length"
        if len(zs) > 0:
            assert len(xs) == len(zs) and len(ys) == len(
                zs
            ), "xs, ys and zs must have the same length if zs is not empty"

    def figure(self):
        self._ensure_connection()

    def scatter(self, xs: list[float], ys: list[float], zs: list[float] = []):
        self.__health_check(xs, ys, zs)
        pts = np.asarray([[xs[i], ys[i], zs[i]] for i in range(len(xs))])

        self.model.add_points(pts)

    def plot(self, xs: list[float], ys: list[float], zs: list[float], color="blue"):
        self.__health_check(xs, ys, zs)
        pts = np.asarray([[xs[i], ys[i], zs[i]] for i in range(len(xs))])

        # Create links
        links = [[i, i + 1] for i in range(len(xs) - 1)]

        # Create colors
        c = (
            Color.from_string(color)
            if isinstance(color, str)
            else Color.from_tuple(color)
        )
        colors = [c] * len(pts)

        # Create skeleton
        pts_vector3 = [Vector3.from_numpy(p) for p in pts]
        sk = Skeleton(name="plot", joints=pts_vector3, colors=colors, links=links)

        self.model.add_skeleton(sk)

    def clear(self):
        self.model.clear()
        self._send()

    def show(self):
        self._ensure_connection()
        self._send()

    def pause(self, time_seconds: int):
        time.sleep(time_seconds)

    def close(self):
        if self.client.connected:
            self.client.disconnect()

    def _ensure_connection(self):
        if not self.client.connected:
            self.client.connect(self._socket_url)

    def _send(self):
        json_data = self.model.model_dump()
        self.client.emit("update", json_data)
        time.sleep(0.1) # wait for sending
