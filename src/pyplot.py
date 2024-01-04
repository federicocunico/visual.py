import time
import webbrowser
import numpy as np
from socketio import Client

from .models import Color, Skeleton, CurrentState, Vector3
from .cfg import PORT


class PyPlot:
    model: CurrentState
    _msgs_sent: int = 0

    def __init__(self, title: str | None, host: str = "localhost", port: int = PORT):
        self.model = CurrentState(title=title)

        self._socket_url = f"http://{host}:{port}"
        self.client = Client(
            reconnection_attempts=10,
        )

    def __health_check(self, xs: list[float], ys: list[float], zs: list[float]):
        assert len(xs) == len(ys), "xs and ys must have the same length"
        if len(zs) > 0:
            assert len(xs) == len(zs) and len(ys) == len(
                zs
            ), "xs, ys and zs must have the same length if zs is not empty"

    def figure(self):
        self._ensure_connection()
        self.clear()

    def scatter(
        self,
        xs: list[float],
        ys: list[float],
        zs: list[float] = [],
        size: int = 1,
        color="blue",
    ):
        self.__health_check(xs, ys, zs)
        pts = np.asarray([[xs[i], ys[i], zs[i]] for i in range(len(xs))])

        self.model.add_points(points=pts, size=size, color=color)

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

    def clear(self, send_now: bool = False):
        self.model.clear()
        if send_now:
            self._send()

    def show(self, include_wait: bool = False, open_browser: bool = False) -> None:
        self._ensure_connection()
        self._send(include_wait=include_wait)
        if open_browser:
            self._open_browser()

    def pause(self, time_seconds: int):
        time.sleep(time_seconds)

    def close(self):
        if self.client.connected:
            self.client.disconnect()

    def _ensure_connection(self, max_retry: int = 10):
        if not self.client.connected:
            attempts = 0
            while True:
                if attempts > max_retry:
                    raise ConnectionError("Cannot connect to Socket.IO server")
                try:
                    self.client.connect(
                        url=self._socket_url, wait_timeout=10, wait=True
                    )
                    break
                except ConnectionError as e:
                    print("Connection error", e)
                    print("Retrying...")
                    time.sleep(1)
                attempts += 1
        elif self._msgs_sent != 0 and self._msgs_sent % 1000 == 0:
            # Reconnect every 1000 messages, I don't know why but sometimes the client lose connection without notification or errors.
            self.client.disconnect()
            self.client.connect(url=self._socket_url, wait_timeout=10, wait=True)
            self._msgs_sent = 0  # reset counter

    def _send(self, include_wait: bool = False):
        json_data = self.model.model_dump()
        try:
            self.client.emit("update", json_data)
        except Exception as e:
            print("Error sending data", e)
        if include_wait:
            time.sleep(0.1)  # wait for sending

        self._msgs_sent += 1

    def _open_browser(self):
        webbrowser.open(self._socket_url)