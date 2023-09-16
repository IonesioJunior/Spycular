class FatherClass:
    def __init__(self, var1: int, var2: str):
        self.var1 = var1
        self.var2 = var2

    def increment(self, var1: int) -> int:
        self.var1 = self.var1 + var1

    def give_length(self) -> int:
        return len(self.var2)
