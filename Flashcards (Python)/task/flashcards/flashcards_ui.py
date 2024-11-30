from user_flashcard import Flashcard
import logging
main_commands = "add", "remove", "import", "export", "ask", "exit", "log", "hardest card", "reset stats"
list_logger = logging.getLogger("log_list")

def print_message(message, add_new_line=False):
    if add_new_line:
        print(message + "\n")
    else:
        print(message)
    list_logger.info(message)

def print_commands():
    commands = ", ".join(main_commands)
    print_message(f"Input the action ({commands}):")

def print_successful_card_creation_msg(flashcard: Flashcard):
    print_message(f"The pair (\"{flashcard.term}\":\"{flashcard.definition}\") has been added.", True)

def read_from_user():
    user_input = input()
    list_logger.info(user_input)
    return user_input

def print_successful_card_removal_msg():
    print_message("The card has been removed.", True)

def print_card_removal_error_msg(card_term):
    message = f"Can't remove \"{card_term}\": there is no such card."
    print_message(message, True)



