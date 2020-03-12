class State():
    def __init__(self, vars=dict()):
        self.vars = vars

    def set(self, var, value):
        self.vars[var.name] = value

    def get(self, var, if_missing=None):
        return self.vars.get(var, if_missing)

    def __getitem__(self, var):
        return self.vars[var]

    def __contains__(self, var):
        return var in self.vars

    def replace(self, key1, key2):
        """replace item key1 with item key2 in vars"""
        self.vars[key2] = self.vars[key1]
        del self.vars[key1]
        
