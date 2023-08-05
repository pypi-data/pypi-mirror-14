m = Machine(num_stores, state, input, oneway)

input is required
  determines where run puts input string

oneway
  causes run nodes to be ranked
  causes add_transition supplies empty rhs

state enables the following shortcuts:
  m.set_start_state(q)
  m.add_accept_state(q)
    supplies _ for input if oneway

m.set_start_config(c)
m.add_accept_config(c)
m.add_transition(t)

-----

FA:  m = Machine((State, Reader))
PDA: m = Machine((State, Reader, Stack))
TM:  m = Machine((State, InputTape))

m.set_start_state(q)
m.add_accept_state(q)

FA:  m.add_transition((q, a?, r))
PDA: m.add_transition((q, a?, x?, r, y?))
TM:  m.add_transition((q, a?, r, b?, "L" or "R"))

m.states
m.start_state
m.accept_states
m.transitions

class Machine(object):
    def apply(self, lhs, rhs, config):
        apply each store

class State(object):
    def __init__(self):
        self.lhs_arity = self.rhs_arity = 1

    def start(self):
        pass

    def apply(self, lhs, rhs, config):
        if config[0] == lhs[0]:
            return (rhs,)

class Reader(object):
    def __init__(self):
        self.lhs_arity = 1
        self.rhs_arity = 0

    def apply(self, lhs, rhs, config):
        if lhs[0] == None:
            return config
        if config[0] == lhs[0]:
            return config[1:]

class Stack(object):
    def __init__(self):
        self.lhs_arity = self.rhs_arity = 1

class Tape(object):
    def __init__(self):
        self.lhs_arity = self.rhs_arity = 1

Definitions of store types:

tape: len(lhs) == len(rhs)
  bounded: if rhs != & then lhs != _
    cell: lhs and rhs always length 1, position 0
    readonly: lhs = rhs
    oneway: rhs position >= lhs position

  reverse stack: always one past the end
    writer: lhs == &

stack: always at position 0
  reader: rhs == &; accept == _

