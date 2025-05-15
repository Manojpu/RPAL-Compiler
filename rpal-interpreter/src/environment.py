class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            raise Exception(f"Variable '{name}' not found")

    def define(self, name, value):
        if name not in self.variables:
            self.set(name, value)
        else:
            raise Exception(f"Variable '{name}' already defined")

    def assign(self, name, value):
        if name in self.variables:
            self.set(name, value)
        elif self.parent is not None:
            self.parent.assign(name, value)
        else:
            raise Exception(f"Variable '{name}' not found for assignment")