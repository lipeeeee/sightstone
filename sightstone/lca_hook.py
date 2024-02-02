"""Hook for league api HACK'ing"""

import sys
import re
import requests
import urllib3
from requests.models import Response
from win32api import GetFileVersionInfo, LOWORD, HIWORD
from collections import defaultdict
from typing import DefaultDict

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
        put(path: str, data: dict, json: dict) -> Response
        delete(path: str, data: dict, json: dict) -> Response

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
    CMD_DICT_DEFAULT_VAL = "LCA_NOT_FOUND_VALUE"
    LISTEN_TIMEOUT = 2
    SLOW_LISTEN_TIMEOUT = 15

    def __init__(self) -> None:
        self.cmd_output_dict: DefaultDict = defaultdict(lambda: self.CMD_DICT_DEFAULT_VAL)
        self.base_url = "127.0.0.1"
        self.protocol = "https"
        self.username = "riot"
        self.connected = False

        # Disable insecure HTTPS request warning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        """LCU auth key"""
        return self.cmd_output_dict["remoting-auth-token"]

    @property
    def auth(self):
        """Auth tuple (username, remoting_auth_token)"""
        return (self.username, self.remoting_auth_token)

    @property
    def install_dir(self):
        """League install directory"""
        return self.cmd_output_dict["install-directory"]

    @property
    def locale(self):
        """League locale"""
        return self.cmd_output_dict["locale"]

    @property
    def region(self):
        """League region"""
        return self.cmd_output_dict["region"]

    @property
    def app_name(self):
        """League executable"""
        return self.cmd_output_dict["app-name"]

    @property
    def riot_port(self):
        """Riot acess port"""
        return self.cmd_output_dict["riotclient-app-port"]

    @property
    def riot_token(self):
        """Riot acess token"""
        return self.cmd_output_dict["riotclient-auth-token"]

    @property
    def riot_auth(self):
        """Riot auth tuple"""
        return (self.username, self.riot_token)

    @property
    def league_version(self) -> tuple[int, int, int, int] | None:
        """Get's league executable file version"""
        if not self.connected:
            return None
        try:
            info = GetFileVersionInfo(f"{self.install_dir} Games\\League of Legends\\{self.app_name}.exe", "\\")
            ms = info["FileVersionMS"]
            ls = info["FileVersionLS"]
            return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
        except Exception as e:
            print(f"ERROR: COULD NOT GET LEAGUE VERSION: {e}")

    def build_url(self, path: str) -> str:
        """Build request url"""
        return f"{self.protocol}://{self.base_url}:{self.port}/{path}"

    def listen(self) -> None:
        """Listens to the status of `LCA`

        Loads content of `LCA` into:
            self.cmd_output_dict (defaultdict): the contents

            self.connected (bool): the status of connection
        """
        # Process Output
        cmd_output = execute_cmd_command(self.CMD_HACK)
        self.cmd_output_dict = self.parse_cmd_output(cmd_output)
        self.connected = cmd_output.startswith(self.LCA_CONNECTED_OUTPUT)
        if True:
            print(f"AUTH: {self.auth}")
            print(f"RIOT-AUTH: {self.riot_auth}")
            print(f"PORT: {self.port}")
            print(f"RIOT-PORT: {self.riot_port}")
            print(f"INSTALL-DIR: {self.install_dir}")
            print(f"LEAGUE-EXE: {self.app_name}")
            print(f"FILEINFO: {self.league_version}")
            print("--------")
        
        # Slow down requests if we are connected
        if self.connected:
            self.listener.time_between_runs = self.SLOW_LISTEN_TIMEOUT
        else:
            self.listener.time_between_runs = self.LISTEN_TIMEOUT


    def parse_cmd_output(self, output: str) -> DefaultDict:
        """Parses cmd output to a dictionary"""
        variables: DefaultDict = DefaultDict(lambda: "default")

        reg_expr = r'--([\w-]+)=([^"\s]+|"([^"]+))'
        matches = re.findall(reg_expr, output)

        # Regex to dictionary parse
        for entry in matches:
            key = entry[0]
            values = entry[1]
            variables[key] = values

        return variables

    def get(self, path: str) -> Response | None:
        """Get request"""
        if not self.connected:
            return None

        try:
            return requests.get(self.build_url(path), auth=self.auth, verify=False)
        except Exception:
            return None

    def post(self, path: str, data: dict | None = None, json: dict | None = None) -> Response | None:
        """Post into LCA"""
        if not self.connected:
            return None

        try:
            return requests.post(
                self.build_url(path),
                data=data, json=json,
                auth=self.auth, verify=False
            )
        except Exception:
            return None

    def put(self, path: str, data: dict | None = None, json: dict | None = None) -> Response | None:
        """Put into LCA"""
        if not self.connected:
            return None

        try:
            return requests.put(
                self.build_url(path),
                data=data, json=json,
                auth=self.auth, verify=False
            )
        except Exception:
            return None

    def delete(self, path: str, data: dict | None = None, json: dict | None = None) -> Response | None:
        """Delete to LCA"""
        if not self.connected:
            return None

        try:
            return requests.delete(
                self.build_url(path),
                data=data, json=json,
                auth=self.auth, verify=False)
        except Exception:
            return None
