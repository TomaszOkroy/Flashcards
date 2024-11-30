import sys

import flashcards_ui
import flashcards_service

# Write your code here

def read_args():
   args = sys.argv[1:]
   return args

if __name__ == '__main__':
    exit_loop = False
    save_on_exit = False
    parsed_args = flashcards_service.parse_arguments(read_args())
    export_file_name = ""
    for order, file_name in parsed_args.items():
        if order == "import":
            flashcards_service.import_flashcards(file=file_name)
        elif order == "export":
            save_on_exit = True
            export_file_name = file_name


    while not exit_loop:
        flashcards_ui.print_commands()
        user_command = flashcards_ui.read_from_user()
        if user_command in flashcards_ui.main_commands:
            match user_command:
                case "add": flashcards_service.create_flashcard()
                case "remove": flashcards_service.delete_flashcard()
                case "ask": flashcards_service.prompt_user()
                case "import": flashcards_service.import_flashcards()
                case "export": flashcards_service.export_flashcards()
                case "exit" : exit_loop = flashcards_service.exit_program(save_on_exit, export_file_name)
                case "hardest card": flashcards_service.find_hardest_flashcard()
                case "reset stats": flashcards_service.reset_mistakes_flashcards()
                case "log": flashcards_service.log_flashcards()






