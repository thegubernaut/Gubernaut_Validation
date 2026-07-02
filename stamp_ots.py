#!/usr/bin/env python3
"""Minimal OpenTimestamps stamper — calendar-only, no Bitcoin node required.

Usage: python stamp_ots.py <file1> [file2 ...]
Each file gets a <file>.ots receipt alongside it.
"""
import sys
import threading
from queue import Queue

from opentimestamps.core.op import OpSHA256
from opentimestamps.core.timestamp import Timestamp, DetachedTimestampFile
from opentimestamps.core.serialize import StreamSerializationContext
import opentimestamps.calendar

CALENDARS = [
    'https://a.pool.opentimestamps.org',
    'https://b.pool.opentimestamps.org',
    'https://a.pool.eternitywall.com',
    'https://ots.btc.catallaxy.com',
]
TIMEOUT = 20  # seconds per calendar

def _submit(url, digest, q, timeout):
    cal = opentimestamps.calendar.RemoteCalendar(url, user_agent="gcc-validation-stamper/1.0")
    try:
        q.put(cal.submit(digest, timeout=timeout))
    except Exception as e:
        q.put(e)

def stamp_file(filepath):
    print(f"Stamping: {filepath}")
    with open(filepath, 'rb') as f:
        detached = DetachedTimestampFile.from_fd(OpSHA256(), f)

    q = Queue()
    threads = []
    for url in CALENDARS:
        t = threading.Thread(target=_submit, args=(url, detached.timestamp.msg, q, TIMEOUT), daemon=True)
        t.start()
        threads.append(t)

    merged = 0
    for _ in range(len(CALENDARS)):
        try:
            result = q.get(timeout=TIMEOUT + 5)
            if isinstance(result, Timestamp):
                detached.timestamp.merge(result)
                merged += 1
                print(f"  + attestation received")
            else:
                print(f"  - calendar error: {result}")
        except Exception as e:
            print(f"  - timeout: {e}")

    if merged == 0:
        raise RuntimeError("No calendars responded — check network connectivity")

    ots_path = filepath + '.ots'
    with open(ots_path, 'wb') as f:
        detached.serialize(StreamSerializationContext(f))

    print(f"  => wrote {ots_path}  ({merged}/{len(CALENDARS)} calendars)")
    return ots_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python stamp_ots.py <file1> [file2 ...]")
        sys.exit(1)
    for path in sys.argv[1:]:
        try:
            stamp_file(path)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
    print("\nDone. Receipts are PENDING — Bitcoin block anchoring takes ~1 hour.")
    print("Verify later with: ots verify <file.ots>")
