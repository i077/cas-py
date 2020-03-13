class State():
    def __init__(self, vars=dict()):
        self.vars = [vars]

    def __setitem__(self, var, value):
        self.vars[0][var.name] = value
        
    def __getitem__(self, var_name):
        for layer in self.vars:
            if var_name in layer:
                return layer[var_name]

        raise KeyError(var_name)

    def get(self, var_name, if_missing=None):
        for layer in self.vars:
            if var_name in layer:
                return layer[var_name]

        return if_missing

    def push_layer(self):
        self.vars.insert(0, dict())

    def pop_layer(self):
        self.vars.pop(0)


    def __contains__(self, var_name):
        return any(var_name in layer for layer in self.vars)

    def replace(self, key1, key2):
        """replace item key1 with item key2 in vars"""
        for layer in self.vars:
            if key1 in layer:
                layer[key2] = layer[key1]
                del layer[key1]
                return
        raise KeyError(key1)
        
