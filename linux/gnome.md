# GNOME

## How do you create a custom application launcher in Gnome Shell?
Try to create a eclipse.desktop file under /usr/share/applications (or ~/.local/share/applications or directly in ~/Desktop) with the following content:

[Desktop Entry]
Encoding=UTF-8
Name=Eclipse IDE
Exec=/path/to/eclipse/executable
Icon=/path/to/eclipse/icon
Type=Application
Categories=Development;
