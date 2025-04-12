from fabric import Connection
from transferAndRemoteRunBase import RemoteConnection


class SSHConnection(RemoteConnection):

    def connect(self):
        # Establish the connection using Fabric's Connection class
        self.connection = Connection(host=self.host, user=self.username, password=self.password)

    def execute_command(self, command):
        if not self.connection:
            # Connect if not already connected
            self.connect()
        # Execute the command using the established connection
        result = self.connection.run(command)
        return result.return_code, result.stdout, result.stderr

    def execute_batch_commands(self, commands):
        for command in commands:
            result = run(command, hosts=self.host, user=self.username, password=self.password)
            print(f"Command: {command}")
            print(f"Exit code: {result.return_code}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            print("-" * 80)
