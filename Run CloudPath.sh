#!/bin/sh

open /Users/Shared/Cloudpath/Cloudpath.app
sleep 5

networksetup -removepreferredwirelessnetwork en0 "Carroll WIFI"

exit 0