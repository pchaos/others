# tracker-store and tracker-miner-fs eating up my CPU on every startup
Whenever I start my laptop the process tracker-store and tracker-miner-fs eats up my CPU between 30-40% for 10-15 minutes. I am on ubuntu 12.04.

What does these processes do? How to get rid of processes?
```
echo -e "\nHidden=true\n" | sudo tee --append /etc/xdg/autostart/tracker-extract.desktop /etc/xdg/autostart/tracker-miner-apps.desktop /etc/xdg/autostart/tracker-miner-fs.desktop /etc/xdg/autostart/tracker-miner-user-guides.desktop /etc/xdg/autostart/tracker-store.desktop > /dev/null

gsettings set org.freedesktop.Tracker.Miner.Files crawling-interval -2  # Default: -1
gsettings set org.freedesktop.Tracker.Miner.Files enable-monitors false # Default: true

tracker reset --hard   
```
* What does these processes do?
  Tracker is a synergy of technologies that are designed to provide a highly sophisticated, innovative and integrated desktop.

  Tracker provides the following:

  Indexer for desktop search (for more details see this spec : https://wiki.ubuntu.com/IntegratedDesktopSearch)
  Tag database for doing keyword tagging of any object
  Extensible metadata database for apps like gedit and rhythmbox which need to add custom metadata to files
  Database for first class objects allows using tracker's database for storage and implementation of First Class Objects and the Gnome 3.0 Model.
