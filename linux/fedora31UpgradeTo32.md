# How to upgrade Fedora 31 to 32
tags: #fedora #upgrade

If you're running Fedora 31 and want to upgrade to the latest release, Jack Wallen walks you through the process.

![](https://tr3.cbsistatic.com/hub/i/r/2019/10/28/bcb562eb-930a-4270-a5ea-dd46c1afa604/thumbnail/768x432/618a1e3761974345218b719444ccd091/f31.jpg)

If you're a Fedora user, you're probably aware that the latest, greatest release is now available. For those who prefer to do a clean install, the process I'm about to explain is not for you. For those who like to do an actual upgrade of your operating system keep watching, because I'm going to walk you through the process of upgrading your trusty Fedora 31 release, to the latest iteration, 32. 

It's not hard, but it does take a bit of time. Depending on the speed of your network and hardware, you can have this done in less than thirty minutes. Let's get to work. We're going to do this completely from the command line. 

Because, why not? 

The first thing to do is open a terminal window and update Fedora 31 so it has the latest software. To do that, open a terminal window and issue the command:

sudo dnf upgrade --refresh

When that completes, we must then install the DNF upgrade plugin with the command:

 sudo dnf system-upgrade download --releasever=32

 This command will download all of the necessary upgrades needed to migrate from 31 to 32. 

When the system-upgrade command completes, you need to reboot your machine with the command:

 sudo dnf system-upgrade reboot

This command will reboot the system and then run all of the necessary upgrades. This is the portion of the upgrade that will take the most time, so walk away from the machine and take on another task. 

When this task completes, the system will automatically restart and present to you the newest version of Fedora. Enjoy the smell of a fresh operating system. 
