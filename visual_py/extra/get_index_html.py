import os
import shutil
import requests
from zipfile import ZipFile


# def download_and_extract_artifact():
#     # GitHub repository details
#     owner = "federicocunico"
#     repo = "visual.js"
#     artifact_name = "index"

#     # GitHub API URL to download the artifact
#     api_url = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts"

#     # Get the list of artifacts without authentication
#     response = requests.get(api_url)
#     response.raise_for_status()
#     artifacts = response.json()["artifacts"]

#     # Find the artifact ID by name
#     artifact_id = next(
#         artifact["id"] for artifact in artifacts if artifact["name"] == artifact_name
#     )

#     # Download the artifact without authentication
#     download_url = f"{api_url}/{artifact_id}/zip"
#     response = requests.get(download_url, stream=True)
#     response.raise_for_status()

#     # Extract the artifact
#     with ZipFile(response.raw) as zip_file:
#         zip_file.extractall()

import requests
import tarfile
import os


def download_file(url):
    local_filename = url.split("/")[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return local_filename


def download_and_extract_release(
    dst: str,
    owner: str = "federicocunico",
    repo: str = "visual.js",
    asset_name: str = "index.tar.gz",
    force: bool = False,
):  
    if not force:
        # check if destination folder exists
        if os.path.isdir(dst) and len(os.listdir(dst)) > 0:
            return

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)

    # GitHub API URL to get the latest release
    release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    # Get the release information
    response = requests.get(release_url)
    response.raise_for_status()
    release_info = response.json()

    # Find the asset ID by name
    asset_id, download_url = next(
        (asset["id"], asset["browser_download_url"])
        for asset in release_info["assets"]
        if asset["name"] == asset_name
    )

    # Download the release asset
    # download_url = f"{release_url}/assets/{asset_id}"
    headers = {"Accept": "application/octet-stream"}
    response = requests.get(download_url, headers=headers, stream=True)
    response.raise_for_status()

    # Save the release asset to a file
    asset_path = os.path.join(dst, asset_name)
    with open(asset_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    # Extract the tar.gz archive
    with tarfile.open(asset_path, "r:gz") as tar:
        actual_dst = os.path.realpath(os.path.join(dst, ".."))  # parent folder
        tar.extractall(actual_dst)

    # Remove the release asset
    os.remove(asset_path)

    print(
        f"Release asset '{asset_name}' downloaded and extracted to '{dst}' directory."
    )


if __name__ == "__main__":
    # download_and_extract_artifact()
    download_and_extract_release("src/dist", force=True)
