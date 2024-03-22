# -*- encoding: utf-8 -*-
# main1.py
import os


class Platform:
    def __init__(self):
        self.loadPlugins()

    def sayHello(self, from_):
        print("hello from %s." % from_)

    def loadPlugins(self):
        for filename in os.listdir("plugins"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            self.runPlugin(filename)

    def runPlugin(self, filename):
        pluginName = os.path.splitext(filename)[0]
        plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
        # Errors may be occured. Handle it yourself.
        plugin.run(self)


if __name__ == "__main__":
    platform = Platform()
