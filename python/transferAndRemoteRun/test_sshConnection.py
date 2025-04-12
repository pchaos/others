import unittest
from unittest.mock import patch

from sshConnection import SSHConnection


class SSHConnectionTest(unittest.TestCase):

    def setUp(self):
        self.host = "localhost"
        self.username = "username"
        self.password = "password"
        self.ssh_connection = SSHConnection(self.host, self.username, self.password)

    def test_init(self):
        self.assertEqual(self.ssh_connection.host, self.host)
        self.assertEqual(self.ssh_connection.username, self.username)
        self.assertEqual(self.ssh_connection.password, self.password)
        self.assertIsNone(self.ssh_connection.connection)

    @patch.object(SSHConnection, 'connect')
    def test_execute_command(self, mock_connect):
        command = "ls -lah"
        expected_return_code = 0
        expected_stdout = "drwxr-xr-x  2 user group 4096 Mar 16 17:55 . \n"
        expected_stderr = ""

        # Mock the connect method to avoid actually connecting
        mock_connect.return_value = None

        result = self.ssh_connection.execute_command(command)

        self.assertEqual(result[0], expected_return_code)
        self.assertEqual(result[1], expected_stdout)
        self.assertEqual(result[2], expected_stderr)

        # Verify that connect was called
        mock_connect.assert_called_once()

    def test_execute_batch_commands_from_list(self):
        commands_list = ["ls -lah", "cd /path/to/project", "git pull"]
        expected_results = [
            (0, "drwxr-xr-x  2 user group 4096 Mar 16 17:55 . \n", ""),
            (0, "[remote_server_host]\n/path/to/project\n", ""),
            (0, "Already up-to-date.\n", ""),
        ]

        # Mock the execute_command method to return expected results
        with patch.object(SSHConnection, 'execute_command') as mock_execute_command:
            for result in expected_results:
                mock_execute_command.return_value = result

            self.ssh_connection.execute_batch_commands_from_list(commands_list)

        # Verify that execute_command was called with each command
        mock_execute_command.assert_called_with(commands_list[0])
        mock_execute_command.assert_called_with(commands_list[1])
        mock_execute_command.assert_called_with(commands_list[2])

    def test_execute_batch_commands_from_file(self):
        file_path = "commands.txt"
        expected_results = [
            (0, "drwxr-xr-x  2 user group 4096 Mar 16 17:55 . \n", ""),
            (0, "[remote_server_host]\n/path/to/project\n", ""),
            (0, "Already up-to-date.\n", ""),
        ]

        # Mock the execute_batch_commands_from_list method to return expected results
        with patch.object(SSHConnection, 'execute_batch_commands_from_list') as mock_execute_batch_commands_from_list:
            mock_execute_batch_commands_from_list.return_value = expected_results

            self.ssh_connection.execute_batch_commands_from_file(file_path)

        # Verify that execute_batch_commands_from_list was called with the file path
        mock_execute_batch_commands_from_list.assert_called_with(file_path)


if __name__ == "__main__":
    unittest.main()
