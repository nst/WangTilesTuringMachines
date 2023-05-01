#!/usr/bin/env python3

from wtm_model import WangTM
from wtm_machines import machines

import unittest

class TestWangTM(unittest.TestCase):

    def test_binary_increment(self):

        tm = machines["Binary increment"]
        step,left_shift,tape,output = tm.run("111")
        self.assertEqual(step, 8)
        self.assertEqual(output, "1000")
        self.assertEqual(len(tape), 6)
        self.assertEqual(left_shift, 2)

        x = tape[0].e
        for t in tape[1:]:
            self.assertEqual(t.w, x)
            x = t.e

    def test_binary_adder(self):

        tm = machines["Binary adder"]
        step,left_shift,tape,output = tm.run("101#11", head=5)
        self.assertEqual(step, 32)
        self.assertEqual(output, "1000#00")

    def test_beaver_2_2(self):

        tm = machines["Beaver 2 2"]
        step,left_shift,tape,output = tm.run("0")
        self.assertEqual(step, 6)
        self.assertEqual(output, "1111")
        self.assertEqual(len(tape), 4)

    def test_beaver_3_2(self):

        tm = machines["Beaver 3 2"]
        step,left_shift,tape,output = tm.run("0")
        self.assertEqual(step, 14)
        self.assertEqual(output, "111111")

    def test_beaver_4_2(self):

        tm = machines["Beaver 4 2"]
        step,left_shift,tape,output = tm.run("0")
        self.assertEqual(step, 107)
        self.assertEqual(output, "10111111111111")
    
if __name__ == "__main__":
    unittest.main()
