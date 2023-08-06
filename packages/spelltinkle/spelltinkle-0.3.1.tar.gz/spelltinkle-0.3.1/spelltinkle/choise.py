class Choise:
    def __init__(self, doc, lines):
        self.doc = doc
        n = max(len(line) for line in lines)
        self.choises = ['{:{}}'.format(line, n) for line in lines]
        self.continuation = None
        doc.changes = 42
        self.r = 0
        
    def up(self):
        if self.r:
            self.r -= 1
        self.doc.changes = 42
        
    def down(self):
        if self.r + 1 < len(self.choises):
            self.r += 1
        self.doc.changes = 42
        
    def enter(self):
        self.doc.handler = None
        self.continuation.send(self.r)

    def esc(self):
        self.doc.handler = None
