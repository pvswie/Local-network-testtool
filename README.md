# Local-network-reliability-testtool
This tool is designed to run 24/7/365 logging issues with the (wifi) network being tested.

System requirements:
- A client running the python3 test script. The script has been tested to work on linux and termux/android.
- A iperf2 and/or iperf3 server, preferably inside the local (home) network, e.g. on the internet router.

Why I created this script:

In a small apartment with too many to count wifi networks I experience occasional (monthly - weeky - daily) issues. Such an issue starts with wifi performance dropping until Wifi becomes completely unusable. Some time later things start to work again. My intention is to have a device monitor Wifi 24/7/365 logging all issues. Hopefully the logged date-time stamps lead to identification of the cause.

Remarks:
The test script uses the iperf3 (or 2) protocol to test whether a minimum bandwidth (1.0 Mbit) is achieved across the network. Due to the low bandwidth this does not really impact Wifi performance. Basically it is possible to use an external iperf server but that is not the best idea for many reasons. Some examples: (1) iperf3 servers support only one simulatinous connection; (2) iperf3 servers are not very reliable, if a connection is not properly closed the server remains in a busy state not accepting new connection requests.
An iperf2 server seems to be better but iperf2 is not very well supported anymore. For example on termux/android there is no client available.
