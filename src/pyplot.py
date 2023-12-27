import numpy as np
from socketio import Client
from pydantic_ext import BaseModel
from src.models.color import Color
from src.models.skeleton import Skeleton
from .models.current_state import CurrentState


class PyPlot(BaseModel):
    model: CurrentState

    def __init__(self, title: str | None, host: str = "localhost", port: int = 11000):
        self.model = CurrentState(title)

        self._socket_url = f"http://{host}:{port}"
        self.client = Client()

    def __health_check(self, xs: list[float], ys: list[float], zs: list[float]):
        assert len(xs) == len(ys), "xs and ys must have the same length"
        if zs:
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
        links = np.asarray([[i, i + 1] for i in range(len(xs) - 1)])

        # Create colors
        c = (
            Color.from_string(color)
            if isinstance(color, str)
            else Color.from_tuple(color)
        )
        colors = [c] * len(pts)

        # Create skeleton
        sk = Skeleton(name="plot", points=pts, colors=colors, links=links)

        self.model.add_skeleton(sk)

    def show(self):
        self._ensure_connection()
        self._send()

    def close(self):
        if self.client.connected:
            self.client.disconnect()

    def _ensure_connection(self):
        if not self.client.connected:
            self.client.connect(self._socket_url)

    def _send(self):
        json_data = self.model.model_dump_json()
        self.client.emit("update", json_data)
