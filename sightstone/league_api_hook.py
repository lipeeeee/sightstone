"""Hook for league api HACK'ing"""

import re
import requests
import sys
from collections import defaultdict
from typing import DefaultDict
from requests.models import Response
sys.path.append("./") # Fixes unknown import when compiled from repo root 
from lib.background_thread import BackgroundThread
from lib.windows_calls import execute_cmd_command

class LeagueConnection:
    """A hacked hook of `LCA`(League client api)

    Provides riot-access to every `LCA` http/https request

    Attributes:
        cmd_output_dict (Dict): A Dictionary of values of the output of
        `CMD_HACK`

        base_url (str): the base url for the `LCA` interface

        protocol (str): specification of http or https protocols

        username (str): As of patch 13.12 the username used
        in auth is a constant value("riot")

        port (str): the port where `LCA` is
        being hosted on(riot version, normal version is 2999)

        remoting_auth_token (str): Auth key

        connected (bool): connected to `LCA` status

        listener (BackgroundThread): listener for `LCA`'s status

    Constants:
        LCA_NOT_CONNECTED_OUTPUT (str): Output when trying to hack but
        `LCA` is down

        LCA_NOT_CONNECTED_OUTPUT (str): Output after sucesseful hacked connection

        CMD_HACK (str): The cmd command to get LCA's info

        LISTEN_TIMEOUT (str): The time in seconds on how long to wait before
        each try of connection

    Methods:
        get(path: str) -> Response
        post(path: str, data: dict, json: dict) -> Response

    Data:
    Example request:
        GET https://127.0.0.1:2999/liveclientdata/allgamedata
    Example of no connection to `LCA`:
        "No Instance(s) Available"
    """

    cmd_output_dict: DefaultDict
    base_url: str
    protocol: str
    username: str
    connected: bool
    listener: BackgroundThread

    LCA_NOT_CONNECTED_OUTPUT = "No Instance(s) Available"  # starts with
    LCA_CONNECTED_OUTPUT = "CommandLine"  # starts with
    CMD_HACK = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"
    LISTEN_TIMEOUT = 2

    def __init__(self) -> None:
        self.cmd_output_dict: DefaultDict = defaultdict(lambda: "default")
        self.base_url = "127.0.0.1"
        self.protocol = "https"
        self.username = "riot"
        self.connected = False

        # Start LCA Listener
        self.listener = BackgroundThread(
            fn_to_run=self.listen, time_between_runs=self.LISTEN_TIMEOUT, daemon=True
        )
        self.listener.start()

    @property
    def port(self):
        """The port where `LCA` is being hosted on"""
        return self.cmd_output_dict["app-port"]

    @property
    def remoting_auth_token(self):
        """Riot auth key"""
        return self.cmd_output_dict["remoting-auth-token"]

    @property
    def auth(self):
        """Auth tuple (username, remoting_auth_token)"""
        return (self.username, self.remoting_auth_token)

    def build_url(self, path: str) -> str:
        """Build request url"""
        return f"{self.protocol}://{self.base_url}:{self.port}/{path}"

    def listen(self) -> None:
        """Listens to the status of `LCA`

        Loads content of `LCA` into:
            self.cmd_output_dict (defaultdict): the contents

            self.connected (bool): the status of connection
        """
        print("Listening to `LCA`...")

        # Process Output
        cmd_output = execute_cmd_command(self.CMD_HACK)
        #cmd_output = remove_excessive_spaces(remove_newline_chars(cmd_output)) # TODO: Implement
        self.cmd_output_dict = self.parse_cmd_output(cmd_output)
        self.connected = cmd_output.startswith(self.LCA_CONNECTED_OUTPUT)

        print(f"CMD_OUTPUT_DICT: {self.cmd_output_dict}")
        print(f"RAT: {self.remoting_auth_token}")

    def parse_cmd_output(self, output: str) -> DefaultDict:
        """Parses cmd output to a dictionary"""
        variables: DefaultDict = DefaultDict(lambda: "default")

        reg_expr = r'--([\w-]+)=([^"\s]+|"([^"]+))'
        matches = re.findall(reg_expr, output)

        # Dictionary parse
        for entry in matches:
            key = entry[0]
            values = entry[1]
            variables[key] = values

        return variables

    def get(self, path: str) -> Response | None:
        """Get request"""
        if not self.connected:
            return None

        return requests.get(self.build_url(path), auth=self.auth)

    def post(
        self, path: str, data: dict | None = None, json: dict | None = None
    ) -> Response | None:
        """Post into LCA"""
        if not self.connected:
            return None

        return requests.post(
            self.build_url(path),
            data=data, json=json,
            auth=self.auth, verify=False
        )
