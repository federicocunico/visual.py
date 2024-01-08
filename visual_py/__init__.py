from .server import server_socket_main_thread
from .cfg import PORT
from .pyplot import PyPlot
from ._version import __version__ as version
from .extra.get_index_html import download_and_extract_release

__version__ = version  # expose version
__all__ = ["server_socket_main_thread", "PyPlot", "PORT"]

download_and_extract_release("visual_py/dist", force=False)
