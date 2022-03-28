# HP打印机
## 驱动安装

dnf install -y hplip hplip-gui

## 下载plugin
https://developers.hp.com/hp-linux-imaging-and-printing/binary_plugin.html

Most Linux distributions include HPLIP with their software, but most do not include the plug-in.  Therefore, it is a safe practice to run a utility called "hp-setup", which, will install the printer into the CUPS spooler, download, and install the plug-in at the appropriate time. 

To install the plug-in using the GUI you can follow these procedures:

1.  Launch a command-line window and enter:

       hp-setup

2.  Select your connection type and click "Next".

3.  Select your printer from "Selected Devices" list and click "Next".

4.  Enter your root password when prompted and click "Next".

5.  Use the recommended installation method and click "Next".

6.  Check the box to accept with the "Driver Plug-In License Agreement" and click "Next".

7.  Finish the installation of the printer as normal, however you may be prompted to re-enter your user name and password.

If you run into any additional install problems you can go to our known issues page and check for a solution.

For advanced users who wish to install HPLIP components manually, a utility exists (hp-plugin) which will download and install the plugin file, but it does not also install a printer queue like hp-setup does.

Do the following:

1.  Launch a command-line window and enter:

       hp-plugin

2. Follow the directions above for navigating the GUI but remember that the printer que will not be installed through this process.

---
hp-plugin 下载驱动组件(可能需要proxy)
