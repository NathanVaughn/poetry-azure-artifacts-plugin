import json
import os
import urllib.parse
import urllib.request


def main():
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    # read minimum poetry version from pyproject.toml
    with open("pyproject.toml", "rb") as fp:
        pyproject = tomllib.load(fp)
        poetry_version = (
            pyproject["tool"]["poetry"]["dependencies"]["poetry"]
            .removeprefix("^")
            .removeprefix(">")
            .removeprefix("=")
        )

    # get all stable releases of poetry
    url = "https://api.github.com/repos/python-poetry/poetry/releases"
    req = urllib.request.Request(url)
    if os.getenv("GITHUB_TOKEN"):
        req.add_header("Authorization", f'Bearer {os.environ["GITHUB_TOKEN"]}')

    with urllib.request.urlopen(req) as response:
        data = json.load(response)

    stable_releases = [release["name"] for release in data if not release["prerelease"]]

    # filter out older releases
    valid_releases = [
        release for release in stable_releases if poetry_version <= release
    ]

    # save output
    print(json.dumps(valid_releases))
    if github_output := os.getenv("GITHUB_OUTPUT"):
        with open(github_output, "w") as fp:
            fp.write(f"poetry_versions={json.dumps(valid_releases)}")


if __name__ == "__main__":
    main()
