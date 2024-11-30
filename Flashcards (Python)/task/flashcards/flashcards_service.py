import random

import flashcard_logger
import flashcards_ui
import file_io
from user_flashcard import Flashcard


class DefinitionAlreadyExistsException(Exception):

    def __init__(self, definition):
        self.definition = definition

    def __str__(self):
        return f"The definition \"{self.definition}\" already exists."


class TermAlreadyExistsException(Exception):

    def __init__(self, term):
        self.term = term

    def __str__(self):
        return f"The card \"{self.term}\" already exists."


flashcards = []


def create_flashcard():
    while True:
        flashcards_ui.print_message(f"The card:")
        while True:
            card_term = flashcards_ui.read_from_user()
            try:
                if check_term_exists(card_term):
                    raise TermAlreadyExistsException(card_term)
                else:
                    break
            except TermAlreadyExistsException as er:
                flashcards_ui.print_message(er.__str__() + " Try again:")
        flashcards_ui.print_message("The definition of the card:")
        while True:
            card_definition = flashcards_ui.read_from_user()
            try:
                if check_definition_exists(card_definition):
                    raise DefinitionAlreadyExistsException(card_definition)
                else:
                    break
            except DefinitionAlreadyExistsException as er:
                flashcards_ui.print_message(er.__str__() + " Try again:")
        new_flashcard = Flashcard(card_term, card_definition)
        flashcards_ui.print_successful_card_creation_msg(new_flashcard)
        add_flashcard(new_flashcard)
        break


def add_flashcard(flashcard):
    flashcards.append(flashcard)


def check_term_exists(term):
    term_set = set([flashcard.term for flashcard in flashcards])
    return term in term_set


def check_definition_exists(definition):
    definition_set = set([flashcard.definition for flashcard in flashcards])
    return definition in definition_set


def find_flashcard_by_definition(definition):
    for flashcard in flashcards:
        if flashcard.definition == definition:
            return flashcard


def find_flashcard_by_term(term):
    for flashcard in flashcards:
        if flashcard.term == term:
            return flashcard


def delete_flashcard():
    flashcards_ui.print_message("Which card?")
    card_term = flashcards_ui.read_from_user()
    if check_term_exists(card_term):
        flashcards.remove(find_flashcard_by_term(card_term))
        flashcards_ui.print_successful_card_removal_msg()
    else:
        flashcards_ui.print_card_removal_error_msg(card_term)


def get_random_flashcard(already_prompted_flashcards):
    # while True:
    #     random_flashcard = flashcards[random.randrange(0, len(flashcards))]
    #     if random_flashcard not in already_prompted_flashcards:
    #         return random_flashcard
    #     elif len(already_prompted_flashcards) == len(flashcards):
    #         return random_flashcard
    return random.choice(flashcards)


def update_flashcard_mistake_rate(flashcard: Flashcard):
    flashcard.update_mistakes()


def prompt_user():
    already_prompted_flashcards = []
    flashcards_ui.print_message("How many times to ask?")
    cards_to_prompt_nr = int(flashcards_ui.read_from_user())
    for _ in range(cards_to_prompt_nr):
        random_flashcard = get_random_flashcard(already_prompted_flashcards)
        already_prompted_flashcards.append(random_flashcard)
        flashcards_ui.print_message(f"Print the definition of \"{random_flashcard.term}\":")
        user_definition = flashcards_ui.read_from_user()
        if user_definition == random_flashcard.definition:
            flashcards_ui.print_message("Correct!")
        else:
            update_flashcard_mistake_rate(random_flashcard)
            searched_flashcard = find_flashcard_by_definition(user_definition)
            if searched_flashcard:

                flashcards_ui.print_message(
                    f"Wrong. The right answer is \"{random_flashcard.definition}\", but your definition is correct for \"{searched_flashcard.term}\".")
            else:
                flashcards_ui.print_message(f"Wrong. The right answer is \"{random_flashcard.definition}\".")
    # flashcards_ui.print_message("")
    print("")


def import_flashcards(file=""):
    if file:
        flashcards_from_file = file_io.read_flashcards(file)
        flashcards.clear()
        flashcards.extend(flashcards_from_file)
        flashcards_ui.print_message(f"{len(flashcards)} cards have been loaded.")
    else:
        flashcards_ui.print_message("File name:")
        file_name = flashcards_ui.read_from_user()
        if file_io.file_exists(file_name):
            imported_flashcard = file_io.read_flashcards(file_name)
            flashcards_ui.print_message(f"{len(imported_flashcard)} cards have been loaded.\n")
            merged_flashcards = imported_flashcard
            #merge imported and program flashcards, excluding duplicates
            merged_flashcards.extend(flashcard for flashcard in flashcards if flashcard not in merged_flashcards)
            print(*merged_flashcards)
            #override running program flashcards
            flashcards.clear()
            flashcards.extend(merged_flashcards)

        else:
            flashcards_ui.print_message("File not found.\n")


def export_flashcards():
    flashcards_ui.print_message("File name:")
    file_name = flashcards_ui.read_from_user()
    file_io.save_to_file(flashcards, file_name)
    flashcards_ui.print_message(f"{len(flashcards)} cards have been saved.\n")


def get_hardest_flashcards() -> list[Flashcard]:
    sorted_flashcards = sorted(flashcards, key=lambda flashcard: flashcard.mistakes, reverse=True)
    hardest_flashcard = sorted_flashcards[0]
    return [flashcard for flashcard in flashcards if flashcard.mistakes == hardest_flashcard.mistakes]


def find_hardest_flashcard():
    if len(flashcards) == 0:
        flashcards_ui.print_message("There are no cards with errors.", add_new_line=True)
    else:
        hardest_flashcards = get_hardest_flashcards()
        if len(hardest_flashcards) == 0 or hardest_flashcards[0].mistakes == 0:
            flashcards_ui.print_message("There are no cards with errors.", add_new_line=True)
        elif len(hardest_flashcards) == 1:
            flashcards_ui.print_message(f"The hardest card is \"{hardest_flashcards[0].term}\"."
                                        f" You have {hardest_flashcards[0].mistakes} errors answering it",
                                        add_new_line=True)
        else:
            mapped_flashcards = ["\"{0}\"".format(flashcard.term) for flashcard in hardest_flashcards]
            parsed_hardest_flashcards = " ,".join(mapped_flashcards)
            flashcards_ui.print_message(f"The hardest cards are {parsed_hardest_flashcards}."
                                        f" You have {hardest_flashcards[0].mistakes} errors answering them.",
                                        add_new_line=True)


def reset_mistakes_flashcards():
    for flashcard in flashcards:
        flashcard.mistakes = 0
    flashcards_ui.print_message("Card statistics have been reset.", add_new_line=True)


def log_flashcards():
    flashcards_ui.print_message("File name:")
    file_name = flashcards_ui.read_from_user()
    file_io.save_to_file(flashcard_logger.logs_list, file_name)
    flashcards_ui.print_message("The log has been saved.", add_new_line=True)


def parse_arguments(args):
    parsed_args = {}
    if len(args) > 0:
        for arg in args:
            if "import" in arg:
                file_name = arg[len("--import_from="):]
                parsed_args["import"] = file_name
            elif "export" in arg:
                file_name = arg[len("--export_to="):]
                parsed_args["export"] = file_name

    return parsed_args


def exit_program(save_on_exit, export_file_name):
    if save_on_exit:
        file_io.save_to_file(flashcards, export_file_name)
        flashcards_ui.print_message(f"{len(flashcards)} cards have been saved.")
    flashcards_ui.print_message("Bye bye!")
    return True
