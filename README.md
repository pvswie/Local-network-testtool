# Local-network-reliability-testtool
This tool is designed to run 24/7/365 logging issues with the (wifi) network being tested.

System requirements:
- Python3 to run this test script. The script has been tested to work on linux and termux/android.
- A iperf2 and/or iperf3 server, preferably inside the local (home) network, e.g. on the internet router.

Why I created this script:

In a small apartment with too many to count wifi networks I experience occasional (monthly - weeky - daily) issues. Such an issue starts with wifi performance dropping until Wifi becomes completely unusable. Some time later things start to work again. My intention is to have a device monitor Wifi 24/7/365 logging all issues. Hopefully the logged date-time stamps lead to identification of the cause.

Remarks:
The test script uses the iperf3 (or 2) protocol to test whether a minimum bandwidth (1.0 Mbit) is achieved across the network. Due to the low bandwidth this does not really impact Wifi performance. Basically it is possible to use an external iperf3 server but that is not the best idea for many reasons such as: (1) iperf3 servers support only one simulatinous connection; (2) iperf3 servers are not very reliable, if a connection is not properly closed the server remains in a busy state rejecting any new connection requests.
An iperf2 server seems to be better but iperf2 is not very well supported anymore. For example on termux/android there is no client available.

==================
Details:
# NW-test-iperf

**24/7 Wi-Fi stability monitoring tool using iperf2 / iperf3**

NW-test-iperf is a lightweight network monitoring tool designed to continuously verify real network connectivity and throughput.  
It repeatedly runs iperf tests against a chosen server and reports connection health in real time.

The tool is optimized for long-term unattended monitoring on Linux and Android/Termux systems.

---

## Features

- Continuous 24/7 iperf testing
- Supports **iperf2 and iperf3**
- Automatic stall detection
- Distinguishes:
  - CONNECTION OK
  - CONNECTION ISSUE
  - CONNECTION TEST ISSUE
- Works on:
  - Linux
  - Android / Termux
- Minimal terminal output (normal mode)
- Detailed diagnostics (debug mode)
- Rotating activity indicator in normal mode
- Optional background/daemon mode
- Robust recovery from:
  - server restarts
  - Wi-Fi drops
  - DNS loss
  - iperf crashes
  - stalled sessions

---

## Requirements

Install at least one of the following:

- iperf3  
- iperf2  

Examples:

### Linux
```bash
sudo apt install iperf3
```

### Android / Termux
```bash
pkg install iperf3
```

---

## Usage

```
NW-test-iperf.py [options] <server> [port]
```

Example:

```bash
./NW-test-iperf.py router.lan
```

---

## Options

| Option | Description |
|--------|-------------|
| `--engine {iperf2,iperf3}` | Select iperf version (default: iperf2 on Linux, iperf3 on Android/Termux) |
| `--udp` | Use UDP instead of TCP |
| `-t SECONDS` | Test duration per iperf run (default: continuous) |
| `-b RATE` | Target bandwidth (default: 1M) |
| `-d` | Debug mode (verbose output) |
| `--background` | Run in background (daemon mode) |
| `--version` | Show version |

---

## Output modes

### Normal mode
Minimal status only:

```
260204-111554 START server=router.lan ...
260204-111623 CONNECTION OK
260204-111824 CONNECTION ISSUE
260204-111900 CONNECTION OK
260204-112100 STOP
```

Plus rotating activity indicator showing tool is alive.

---

### Debug mode (`-d`)
Shows full iperf output and diagnostics.

---

## Status meanings

| Status | Meaning |
|--------|--------|
| CONNECTION OK | Throughput ≥ expected |
| CONNECTION ISSUE | Real connectivity problem |
| CONNECTION TEST ISSUE | iperf server busy/unavailable |
| START / STOP | Tool lifecycle |

---

## Background mode

Run detached:

```bash
./NW-test-iperf.py --background router.lan
```

Safe to start over SSH and logout — monitoring continues.

---

## Typical deployment

Wi-Fi stability monitor:

```bash
./NW-test-iperf.py router.lan
```

Internet path monitor:

```bash
./NW-test-iperf.py iperf.example.net
```

Daemonized monitoring:

```bash
./NW-test-iperf.py --background router.lan
```

---

## Reliability notes

The tool handles:

- Wi-Fi down/up
- server reboot
- DNS loss
- iperf termination
- stalled transfers
- server busy conditions

It is intended for unattended long-term operation.

---

## License

MIT License

---

## Acknowledgements

This tool was developed with architectural and implementation assistance from **ChatGPT (OpenAI)**.

ChatGPT helped with:

- design decisions
- cross-platform behavior
- stall detection logic
- terminal handling
- iperf behavior modeling
- robustness improvements

All testing, requirements, and real-world validation were performed by the author.

---

## Project status

Stable and used for continuous Wi-Fi monitoring in a high-density RF environment.

Contributions and feedback welcome.
