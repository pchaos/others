import telnetlib

from transferAndRemoteRunBase import RemoteConnection


class TelnetConnection(RemoteConnection):
    def connect(self):
        self.tn = telnetlib.Telnet(self.host)
        self.tn.expect(b"login: ")
        self.tn.write(self.username.encode("ascii") + b"\n")
        self.tn.expect(b"Password: ")
        self.tn.write(self.password.encode("ascii") + b"\n")

    def execute_command(self, command):
        self.tn.write(command.encode("ascii") + b"\n")
        result = self.tn.read_until(b"\n").decode()
        return 0, result, ""
