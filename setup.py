from setuptools import find_packages, setup

VERSION = "0.0.1"
DESCRIPTION = "Visualize data in 3D with three.js"
LONG_DESCRIPTION = "Visualize data in 3D with three.js as replacement of matplotlib and open3d for a multi-platform supported visualization."

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="visual_py",
    version=VERSION,
    author="Federico Cunico",
    author_email="<federico@cunico.net>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask_cors",
        "flask_socketio",
        "python-socketio",
        "pydantic",
        "requests",
        "numpy",
        "webcolors",
        "socketio",
        "websocket-client",
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=[
        "python",
        "visualization",
        "three.js",
        "matplotlib",
        "open3d",
        "3d",
        "plot",
        "scatter",
        "plot3d",
        "scatter3d",
        "visualize",
        "visualisation",
        "visualize3d",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
)
