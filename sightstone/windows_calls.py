# Various calls to the windows operating system

import subprocess
import win32gui # pyright: ignore could not find module
import win32process # pyright: ignore could not find module

def execute_cmd_command(command: str) -> str:
    """Execute command in cmd, returns STDOUT"""
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True
        )
        return output
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed with error code {e.returncode}: {e.output}")
        return "Command execution failed."

def search_hndw_by_name(target: str) -> int:
    """Gets window HNDW by name, returns 0 if failed to find"""
    return win32gui.FindWindow(None, target)

def get_thread_id_process_id(target_hndw: int) -> tuple[int, int]:
    """Gets (thread_id, process_id) from `target_hndw`"""
    return win32process.GetWindowThreadProcessId(target_hndw)
