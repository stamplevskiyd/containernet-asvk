#!/usr/bin/env python

"""
Test for multiping.py
"""

import unittest
from mininet.util import pexpect
from collections import defaultdict


class testMultiPing(unittest.TestCase):
    def testMultiPing(self):
        """Verify that each target is pinged at least once, and
        that pings to 'real' targets are successful and unknown targets fail"""
        p = pexpect.spawn("python -m mininet.examples.multiping")
        opts = [
            "Host (h\d+) \(([\d.]+)\) will be pinging ips: ([\d\. ]+)",
            "(h\d+): ([\d.]+) -> ([\d.]+) \d packets transmitted, (\d) received",
            pexpect.EOF,
        ]
        pings = defaultdict(list)
        while True:
            index = p.expect(opts)
            if index == 0:
                name = p.match.group(1)
                ip = p.match.group(2)
                targets = p.match.group(3).split()
                pings[name] += targets
            elif index == 1:
                name = p.match.group(1)
                ip = p.match.group(2)
                target = p.match.group(3)
                received = int(p.match.group(4))
                if target == "10.0.0.200":
                    self.assertEqual(
                        received,
                        0,
                        p.match.group(0)
                        + "\n"
                        + target
                        + " received %d != 0 packets" % received,
                    )
                else:
                    self.assertEqual(
                        received,
                        1,
                        p.match.group(0)
                        + "\n"
                        + target
                        + " received %d != 1 packets" % received,
                    )
                try:
                    pings[name].remove(target)
                except:
                    pass
            else:
                break
        self.assertTrue(len(pings) > 0, "too few pings")
        for t in pings.values():
            self.assertEqual(len(t), 0, "missed ping target(s): %s" % t)


if __name__ == "__main__":
    unittest.main()
