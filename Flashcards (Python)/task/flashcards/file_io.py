
import os
from user_flashcard import Flashcard

def file_exists(file_name):
    return os.path.isfile(file_name)


def save_to_file(items, filename):

   with open(f"{filename}", "w") as outfile:
       for item in items:
           outfile.write(item.__str__() + "\n")

def read_flashcards(filename):
    flashcards = []
    with open(f"{filename}", "r") as file:
        for line in file:
           stripped_line = line.strip()
           parsed_lnie = stripped_line.split(" ")
           loaded_flashcard = Flashcard(parsed_lnie[0], parsed_lnie[1])
           loaded_flashcard.set_mistakes(int(parsed_lnie[2]))
           flashcards.append(loaded_flashcard)

    return flashcards


def save_logs(logs_list, file_name):
    return None