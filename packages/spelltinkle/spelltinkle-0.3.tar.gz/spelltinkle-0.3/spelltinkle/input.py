class Input:
    def __init__(self, string=''):
        self.c = len(string)
        self.update(string)

    def update(self, string=None):
        if string is not None:
            self.string = string
        
    def insert_character(self, chr):
        s = self.string[:self.c] + chr + self.string[self.c:]
        self.c += 1
        self.update(s)
        
    def bs(self):
        if self.c > 0:
            s = self.string[:self.c - 1] + self.string[self.c:]
            self.c -= 1
            self.update(s)
        
    def delete(self):
        s = self.string[:self.c] + self.string[self.c + 1:]
        self.update(s)
        
    def left(self):
        self.c = max(0, self.c - 1)
        self.update()

    def right(self):
        self.c = min(len(self.string), self.c + 1)
        self.update()

    def home(self):
        self.c = 0
        self.update()

    def end(self):
        self.c = len(self.string)
        self.update()
