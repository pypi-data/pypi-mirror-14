class State(object):
    def __init__(self):
        self.lhs_arity = self.rhs_arity = self.config_arity = 1

    def start_config(self, input):
        pass
    def accept_configs(self, input):
        pass

    def apply(self, lhs, rhs, config):
        if lhs != config:
            raise ValueError()
        return rhs

class Tape(object):
    def __init__(self):
        self.lhs_arity = 1
        self.config_arity = 2
        self.rhs_arity = 2

    def start_config(self, input):
        pass
    def accept_configs(self, input):
        pass

    def apply(self, lhs, rhs, config):
        read, = lhs
        write, move = rhs
        if move == 'L': 
            move = -1
        elif move == 'R':
            move = +1
        else:
            raise ValueError("invalid move: {}".format(move))
        symbols, position = config
        if read != symbols[position]:
            raise ValueError()
        return (symbols[:position] + (write,) + symbols[position+1:], position+move)

class Reader(object):
    def __init__(self):
        self.lhs_arity = self.config_arity = 1
        self.rhs_arity = 0

    def start_config(self, input):
        pass
    def accept_configs(self, input):
        pass

    def apply(self, lhs, rhs, config):
        if lhs != config[:len(lhs)]:
            raise ValueError()
        return config[len(lhs):]

class Stack(object):
    def __init__(self):
        self.lhs_arity = self.rhs_arity = self.config_arity = 1

    def start_config(self, input):
        pass
    def accept_configs(self, input):
        pass

    def apply(self, lhs, rhs, config):
        if lhs != config[:len(lhs)]:
            raise ValueError()
        return rhs + config[len(lhs):]

class Machine(object):
    def __init__(components):
        self.components = tuple(components)

    def apply(self, lhs, rhs, config):
        li = ri = 0
        newconfig = []
        for component in self.components:
            clhs = lhs[li:li+component.lhs_arity]
            cconfig = config[li:li+component.config_arity]
            crhs = rhs[ri:ri+component.rhs_arity]
            newconfig.extend(component.apply(clhs, crhs, cconfig))
            li += component.lhs_arity
            ri += component.rhs_arity
        return tuple(newconfig)

