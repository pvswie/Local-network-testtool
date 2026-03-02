#!/usr/bin/env python3
# NW-test-iperf.py
# Continuous iperf2/3 network monitor

import argparse
import os
import pty
import shutil
import subprocess
import sys
import time
import select
import platform
import socket

VERSION = "V1"

SPINNER = ["|", "/", "-", "\\"]

# -----------------------------
# Helpers
# -----------------------------

def ts():
    return time.strftime("%y%m%d-%H%M%S")

def is_tty():
    return sys.stdout.isatty()

def is_android():
    return "android" in platform.system().lower() or "ANDROID_ROOT" in os.environ

def engine_available(engine):
    cmd = "iperf3" if engine == "iperf3" else "iperf"
    return shutil.which(cmd) is not None

def resolve_host(host):
    try:
        socket.getaddrinfo(host, None)
        return True
    except socket.gaierror:
        return False

# -----------------------------
# State classification
# -----------------------------

def classify_output(line):
    l = line.lower()

    if "busy running a test" in l:
        return "TEST_ISSUE"

    if "unable to connect" in l or "unknown host" in l:
        return "ISSUE"

    if "broken pipe" in l or "connection refused" in l:
        return "ISSUE"

    if "0.00 bits/sec" in l or "0.000 bits/sec" in l:
        return "ISSUE"

    if "bits/sec" in l:
        return "OK"

    return None

# -----------------------------
# Output
# -----------------------------

def print_line(msg):
    print(f"{ts()} {msg}", flush=True)

def print_rotator(idx):
    sys.stdout.write("\r" + SPINNER[idx])
    sys.stdout.flush()

def clear_rotator():
    sys.stdout.write("\r")
    sys.stdout.flush()

# -----------------------------
# Run loop
# -----------------------------

def run_loop(cmd, debug):
    state = None
    spinner_idx = 0
    last_spin = 0
    last_output = time.time()

    quiet = not debug

    while True:
        try:
            master, slave = pty.openpty()
        except OSError:
            print_line("ERROR: PTY allocation failed")
            time.sleep(3)
            continue

        try:
            proc = subprocess.Popen(
                cmd,
                stdin=slave,
                stdout=slave,
                stderr=slave,
                close_fds=True,
            )
        except FileNotFoundError:
            engine = "iperf3" if "iperf3" in cmd[0] else "iperf2"
            print_line(f"ERROR: {engine} not installed")
            return

        os.close(slave)

        while True:
            if quiet and is_tty():
                now = time.time()
                if now - last_spin >= 0.25:
                    print_rotator(spinner_idx)
                    spinner_idx = (spinner_idx + 1) % len(SPINNER)
                    last_spin = now

            r, _, _ = select.select([master], [], [], 0.5)

            if master in r:
                try:
                    data = os.read(master, 4096)
                except OSError:
                    break

                if not data:
                    break

                last_output = time.time()
                text = data.decode(errors="ignore")

                for raw in text.splitlines():
                    line = raw.strip()
                    if not line:
                        continue

                    if debug:
                        clear_rotator()
                        print_line(line)

                    new_state = classify_output(line)
                    if new_state and new_state != state:
                        clear_rotator()
                        if new_state == "OK":
                            print_line("CONNECTION OK")
                        elif new_state == "ISSUE":
                            print_line("CONNECTION ISSUE")
                        elif new_state == "TEST_ISSUE":
                            print_line("CONNECTION TEST ISSUE")
                        state = new_state

            if proc.poll() is not None:
                break

        try:
            os.close(master)
        except OSError:
            pass

        if debug:
            print_line("INFO: iperf exited")

        time.sleep(1)

# -----------------------------
# CLI
# -----------------------------

def build_cmd(engine, server, port, udp, bw, duration):
    if engine == "iperf3":
        cmd = ["iperf3", "-c", server, "-p", str(port), "-i", "1", "-b", bw]
        if duration == 0:
            cmd += ["-t", "0"]
        else:
            cmd += ["-t", str(duration)]
        if udp:
            cmd.append("-u")
    else:
        cmd = ["iperf", "-c", server, "-p", str(port), "-i", "1", "-b", bw]
        if duration == 0:
            cmd += ["-t", "0"]
        else:
            cmd += ["-t", str(duration)]
        if udp:
            cmd.append("-u")
    return cmd

# -----------------------------
# Main
# -----------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Continuous network monitor using iperf2/3"
    )

    parser.add_argument("server")
    parser.add_argument("port", nargs="?", type=int)
    parser.add_argument("--engine", choices=["iperf2", "iperf3"])
    parser.add_argument("--udp", action="store_true")
    parser.add_argument("-t", "--time", type=int, default=0)
    parser.add_argument("-b", "--bandwidth", default="1M")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(VERSION)
        return

    # Engine selection
    if args.engine:
        engine = args.engine
    else:
        if is_android():
            engine = "iperf3"
        else:
            engine = "iperf2" if engine_available("iperf2") else "iperf3"

    if not engine_available(engine):
        print_line(f"ERROR: {engine} not installed")
        return

    # Port defaults
    if args.port:
        port = args.port
    else:
        port = 5201 if engine == "iperf3" else 5001

    # UDP default
    udp = args.udp
    if not args.udp and not is_android():
        udp = True

    # Startup DNS check
    if not resolve_host(args.server):
        print_line("CONNECTION ISSUE")
        return

    duration = args.time if args.time else 0

    proto = "UDP" if udp else "TCP"

    print_line(
        f"START server={args.server} port={port} engine={engine} proto={proto} bw={args.bandwidth} time={'forever' if duration==0 else duration}"
    )

    cmd = build_cmd(engine, args.server, port, udp, args.bandwidth, duration)

    try:
        run_loop(cmd, args.debug)
    except KeyboardInterrupt:
        clear_rotator()
        print_line("STOP")

if __name__ == "__main__":
    main()
