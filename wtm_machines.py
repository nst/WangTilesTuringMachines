#!/usr/bin/env python3

from wtm_model import WangTM

machines = {}

machines["Binary increment"] = WangTM(name="Binary increment",
                            states=["A","B","H"],
                            alphabet=["0","1"],
                            blank_symbol="#",
                            transitions_string= "#LB 0RA 1RA 1LH 1LH 0LB")

# https://machinedeturing.com/ang_calculateur.php?page

machines["Binary adder"] = WangTM(name="Binary adder",
                            states=["A","B","C","D","E","F","H"],
                            alphabet=["0","1"],
                            blank_symbol="#",
                            transitions_string=' '.join(["#LA 1LA 0LB", "#LC 0LB 1LB", "1RD 1RD 0LC", "#RE 0RD 1RD", "#RH 0RE 1RF", "#LA 0RF 1RF"]))

machines["Beaver"] = WangTM(name="Beaver nst 41",
                            states=["A","B","C","D","E","H"],
                            alphabet=["1"],
                            blank_symbol="0",
                            transitions_string= "0RC 1LE 0LC 0LA 1RE 1RD 1LH 0RB 1LA 1RB")

# https://webusers.imj-prg.fr/~pascal.michel/bbc.html

machines["Beaver 2 2"] = WangTM(name="Beaver 2 states 2 symbols, S=6",
                            states=["A","B","H"],
                            alphabet=["1"],
                            blank_symbol="0",
                            transitions_string= "1RB 1LB 1LA 1RH")

machines["Beaver 3 2"] = WangTM(name="Busy Beaver 3 states 2 symbols, S=14",
                            states=["A","B","C","H"],
                            alphabet=["1"],
                            blank_symbol="0",
                            transitions_string= "1RB 1RH 0RC 1RB 1LC 1LA")

machines["Beaver 4 2"] = WangTM(name="Beaver 4 states 2 symbols, S=107",
                            states=["A","B","C","D","H"],
                            alphabet=["1"],
                            blank_symbol="0",
                            transitions_string= "1RB 1LB 1LA 0LC 1RH 1LD 1RD 0RA")

machines["Beaver 5 2"] = WangTM(name="Beaver 5 states 2 symbols, S=47176870, Sigma=4098",
                            states=["A","B","C","D","E","H"],
                            alphabet=["1"],
                            blank_symbol="0",
                            transitions_string= "1LB 1RC 1LC 1LB 1LD 0RE 1RA 1RD 1LH 0RA")
