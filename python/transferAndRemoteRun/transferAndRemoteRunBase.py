class RemoteConnection:
    def __init__(self, host, username, password=""):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        raise NotImplementedError

    def execute_command(self, command):
        raise NotImplementedError

    def execute_batch_commands_from_file(self, file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()

        self.execute_command(file_content)
