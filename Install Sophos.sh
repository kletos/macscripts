#!/bin/sh

sudo chmod a+x /Users/Shared/Sophos\ Installer.app/Contents/MacOS/Sophos\ Installer
sudo chmod a+x /Users/Shared/Sophos\ Installer.app/Contents/MacOS/tools/com.sophos.bootstrap.helper

sudo /Users/Shared/Sophos\ Installer.app/Contents/MacOS/Sophos\ Installer --install

sudo rm -r /Users/Shared/Sophos\ Installer.app
sudo rm -r /Users/Shared/Sophos\ Installer\ Components 