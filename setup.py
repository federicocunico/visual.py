from setuptools import find_namespace_packages, find_packages, setup


get_version = (
    lambda: open("visual_py/_version.py").readlines()[-1].split()[-1].strip('"')
)

DESCRIPTION = "Visualize data in 3D with three.js"
LONG_DESCRIPTION = "Visualize data in 3D with three.js as replacement of matplotlib and open3d for a multi-platform supported visualization."

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="visual_py",
    version=get_version(),
    author="Federico Cunico",
    author_email="<federico@cunico.net>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # packages=find_namespace_packages(),
    install_requires=[
        "flask",
        "flask_cors",
        "flask_socketio",
        "python-socketio",
        "pydantic",
        "requests",
        "numpy",
        "webcolors",
        "wheel",
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


def _post_install_steps():
    # This is performed only when executing python setup.py install in local mode
    try:
        from visual_py.extra.get_index_html import download_and_extract_release

        download_and_extract_release("visual_py/dist", force=True)
        # download_and_extract_release("dist")
    except Exception as e:
        pass


_post_install_steps()
