#!/usr/bin/env python3

# a Turing machine where states and transitions are represented with Wang tiles

from collections import namedtuple

Tile = namedtuple("Tile", "n e s w")

class WangTM:

    def __init__(self, name, states, alphabet, blank_symbol, transitions_string):

        self.name = name
        self.states = states # first state first, halting state last
        self.alphabet = alphabet # without blank symbol
        self.blank_symbol = blank_symbol
        
        # TNF (Tree Normal Form) eg. "1RB 1LB 1LA 1RH 0RA"
        # eg. "1RB 1LB 1LA 1RH 0RA 1LA" for A#, A0, A1, B#, B0, B1
        self.transitions_string = transitions_string

        if not len(alphabet) > 0:
            raise Exception("Alphabet cannot be empty")

        if not len(states) > 0:
            raise Exception("States cannot empty")

        if states[-1] != "H":
            raise Exception("Last state must be the Halting symbol")
        
        if self.blank_symbol in self.alphabet:
            raise Exception("Blank symbol '%s' must not be part of the alphabet" % self.blank_symbol)
        
        self.alphabet.insert(0, blank_symbol) # TNF
        
        # filled before running
        self.tiles_alphabet = {}
        self.tiles_head = {}
        self.tiles_action = {}
        self.tiles_move = {}
        
    def run(self, input_string, head=0):

        tape = []

        for step, left_shifts, tape in self.run_gen(input_string, head):
            pass
        
        output = "".join([t.s for t in tape]).replace(self.states[-1], "").strip(self.blank_symbol)

        return (step, left_shifts, tape, output)

    def run_gen(self, input_string, head=0):

        if len(input_string) == 0:
            raise Exception("Input cannot be empty")

        if len(self.tiles_alphabet) == 0:
            self.create_tileset()

        left_shifts = 0

        step = 0
        
        tape = [self.tiles_alphabet[c] for c in input_string]

        a = self.tiles_alphabet[input_string[head]].s
        tape[head] = self.tiles_head[a]

        yield(step, left_shifts, tape)

        while tape[head].s in self.tiles_action:

            step += 1

            # 1. previous action tile turns into alphabet tile
            
            for h in (head-1, head, head+1):
                if h in range(0, len(tape)) and tape[h].n in self.tiles_action:
                    tape[h] = self.tiles_alphabet[tape[h].s]
            
            # 2. update head with action tile

            t = self.tiles_action[tape[head].s]

            tape[head] = t

            # 3. propagate state left or right with move tile

            move_left = t.w != " "
            move_right = t.e != " "
            
            expand_left = move_left and head == 0
            expand_right = move_right and head == len(tape)-1

            if expand_left:
                t = self.tiles_move[(" ", self.blank_symbol, t.w)]
                tape.insert(0, t)
                head = 0
                left_shifts += 1
            elif expand_right:
                t = self.tiles_move[(t.e, self.blank_symbol, " ")]
                tape.append(t)
                head += 1
            elif move_left:
                head -= 1
                tape[head] = self.tiles_move[(" ", tape[head].s, t.w)]
            elif move_right:
                head += 1
                tape[head] = self.tiles_move[(t.e, tape[head].s, " ")]
            
            yield(step, left_shifts, tape)
        
    def create_tileset(self):
        
        # alphabet tiles
        for a in self.alphabet:
            self.tiles_alphabet[a] = Tile(a, " ", a, " ")
            self.tiles_head[a] = Tile(a, " ", self.states[0]+a, " ")

        # action tiles
        for i,wds in enumerate(self.transitions_string.split(" ")):

            if not len(wds) == 3:
                raise Exception("Use transitions such as 1RB 1LB 1LA 1RH")

            b,d,p = wds # write, dir, state
                        
            q = self.states[int(i/(len(self.alphabet)))] # A A A B B B C ...
            a = self.alphabet[i%(len(self.alphabet))]    # 0 1 # 0 1 # 0 ...

            t = (q,a),(b,d,p)
            
            if d not in "LR":
                raise Exception("Unknown direction to move:", d)
            
            if d == "R":
                t = Tile(q+a, p, b, " ")
            elif d == "L":
                t = Tile(q+a, " ", b, p)
        
            #print(f"In state {q} read {a} -> write {b}, move {d}, state {p}")
        
            self.tiles_action[q+a] = t

        # moving tiles
        # we can come up with a minimal tileset by:
        # - not creating moving tiles for halting state
        # - setting specific strings/colors on south of halting action tiles
        # but it prevents the head from finishing in the expected position
        # as defined in the transtions string
        for s in self.states:
            for a in self.alphabet:                
                self.tiles_move[(" ", a, s)] = Tile(a, s, s+a, " ")
                self.tiles_move[(s, a, " ")] = Tile(a, " ", s+a, s)
