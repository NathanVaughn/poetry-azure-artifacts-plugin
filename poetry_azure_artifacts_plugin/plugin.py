# https://github.com/semgrep/poetry-codeartifact-plugin/

from typing import Any
from urllib.parse import urlparse

import artifacts_keyring
import requests
from cleo.io.io import IO
from poetry.config.config import Config
from poetry.exceptions import PoetryException
from poetry.plugins import Plugin
from poetry.poetry import Poetry
from poetry.utils.authenticator import Authenticator


def monkeypatch_authenticator(io: IO) -> None:
    old_request = Authenticator.request

    def new_request(
        self: Authenticator, method: str, url: str, *args: Any, **kwargs: Any
    ) -> requests.Response:
        # copy args
        new_kwargs = kwargs.copy()
        # get current raise_for_status value
        raise_for_status = new_kwargs.pop("raise_for_status", True)
        # replace raise_for_status with False
        new_kwargs["raise_for_status"] = False

        response = old_request(self, method, url, *args, **new_kwargs)

        if response.status_code in (401, 403):
            netloc = urlparse(response.url)[1]
            config = self.get_repository_config_for_url(url)

            if (
                ("pkgs.dev.azure.com" in netloc)
                or ("pkgs.visualstudio.com" in netloc)
                or (config is not None and "azure-artifacts" in config.name)
            ) and config:
                io.write_line(
                    f"Getting new Azure Artifacts token for repo {
                        config.name}"
                )

                # get token from credential provider
                username, token = (
                    artifacts_keyring.plugin.CredentialProvider().get_credentials(url)
                )

                # if we didn't get a token
                if username is None or token is None:
                    raise PoetryException(
                        f"Failed getting new Azure Artifacts token for repo {
                            config.name}"
                    )

                # set the new token
                self._password_manager.set_http_password(config.name, username, token)
                self.reset_credentials_cache()
                self._password_manager._config = Config.create(reload=True)

                # Retry the request now that we're authenticated
                return old_request(self, method, url, *args, **kwargs)

        # do original raise_for_status
        if raise_for_status:
            response.raise_for_status()
        return response

    # monkeypatch Authenticator.request
    Authenticator.request = new_request


class AzureArtifactsPlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO) -> None:
        monkeypatch_authenticator(io)
