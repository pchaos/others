# -*- coding=utf-8 -*-
# Modified: 2025-07-16 20:09:47
try:
    import neovim-remote
except ImportError:
    print("Installing neovim-remote first ...")
    print("pip install neovim-remote")
    exit(1)

# Connect to the Neovim instance
# Replace the path with your actual socket path or server name
neovim_server_path = "/run/user/1000/lvim.956283.0"
nvim = neovim_remote.connect_socket(neovim_server_path)

# Or, if using an existing instance's server name:
# nvim = neovim_remote.connect_server(server_name='VIM') # 'VIM' is a common default

# Open the file
nvim.command(f"edit {neovim_server_path}")

# You can also send other commands, e.g., to go to a specific line:
# nvim.command(f"call cursor(10, 5)") # Go to line 10, column 5
