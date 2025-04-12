import winrm
from transferAndRemoteRunBase import RemoteConnection


class WinRMConnection(RemoteConnection):
    def connect(self):
        self.conn = winrm.protocol.WinRMClient(
            transport="credssp", url=f"http://{self.host}:5985/wsman", auth=(self.username, self.password)
        )

    def execute_command(self, command):
        result = self.conn.run_cmd(command, ["powershell"])
        return result.status_code, result.std_out, result.std_err
