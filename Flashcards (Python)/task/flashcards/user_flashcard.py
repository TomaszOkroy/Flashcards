class Flashcard:
    def __init__(self, term, definition):
        self.term = term
        self.definition = definition
        self.mistakes = 0

    def __str__(self):
        return f"{self.term} {self.definition} {self.mistakes}"

    def __eq__(self, other):
        if not isinstance(other, Flashcard):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.term == other.term

    def set_mistakes(self, number):
        self.mistakes = number

    def update_mistakes(self):
        self.mistakes += 1