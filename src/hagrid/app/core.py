"""This is Hagrid. Hagrid likes to help Harry become a wizard, by developing
his questions. Regard:

# Data and Process Flow Diagram Description

### Simplified Components

1. **User Interface (UI)**: Where the user interacts with the application.
2. **LLM Interface (LLMI)**: Manages all interactions with the Large Language Model, including sending and receiving prompts and responses.
3. **Data Storage (DS)**: Stores optimized prompts, responses, and history.

### Simplified Data Flow

1. **UI -> LLMI**: User inputs topic and prompt category.
2. **LLMI -> LLM**: Sends initial prompt for refinement.
3. **LLM -> LLMI**: Returns optimized prompt.
4. **LLMI -> DS**: Stores optimized prompt.
5. **DS -> LLMI**: Retrieves stored optimized prompt.
6. **LLMI -> LLM**: Sends optimized prompt for answering.
7. **LLM -> LLMI**: Returns answer.
8. **LLMI -> UI**: Displays answer to the user and allows for further prompt engineering selection.
9. **UI -> DS**: Stores prompt history for future use.

### Simplified Process Flow

1. **Initialize Application**: Start all modules.
2. **Gather User Input**: Use UI to collect user's topic and prompt category.
3. **Initial LLM Interaction**: Use LLMI to send initial prompt to LLM for refinement.
4. **Store Optimized Prompt**: Use DS to store the optimized prompt returned by LLM.
5. **Display Answer**: Use UI to display the LLM's answer based on the optimized prompt.
6. **Iterative Refinement**: Use UI to allow the user to select another prompt engineering technique.
7. **Repeat Steps 3-6**: Until the user is satisfied.
8. **Store History**: Use DS to store all prompts and responses for future use.

"""

from enum import Enum
from urllib import request
import os
import sys
import argparse
import sqlite3
import json
import logging
import unittest
import pdb
import ipdb


def catch_errors(func):
    """Wrapper decorator to catch and print errors"""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BaseException as ex:
            # TODO: integrate with error system
            print("Caught error via decorator!", ex)
            logger.error(ex)
    return wrapper


class HagridErrorCode(Enum):
    SUPERMIND_INTERFERENCE = "No good sitting worrying about it. What's coming will come, and we'll meet it when it does"
    UNKNOWN_ERROR = "Yer a wizard, Harry"
    INPUT_ERROR = "Got me the gamekeeper job...trusts people, he does. Gives 'em second chances...tha's what set him apar' from other Heads, see."


class HagridError(BaseException):
    def __init__(self, msg, error_code=HagridErrorCode.UNKNOWN_ERROR):
        super().__init__(msg)
        self.error_code = error_code

    def log_err(self):
        print(f"\033[91mError!Error: {self.error_code}: {self}\033[0m")


class FileContextManager():
    def __init__(self, file_name):
        self._file_name = file_name
        self._file = None

    def __enter__(self):
        self._file = open(self._file_name)
        return self._file

    def __exit__(self, cls, value, tb):
        self._file.close()


class GPTRequestContextManager():
    def __init__(self, prompt=None, ui=None, is_config=False) -> None:
        self._prompt = prompt
        self._api_key = os.getenv("OPENAI_API_KEY")
        if self._api_key == None:
            raise HagridError(
                'No OPENAI_API_KEY env variable found', HagridErrorCode.INPUT_ERROR)
        self._org = os.getenv("OPENAI_API_ORG")
        if self._org == None:
            raise HagridError(
                'No OPENAI_API_ORG env variable found', HagridErrorCode.INPUT_ERROR)
        self._req_url = 'https://api.openai.com/v1/chat/completions'
        self._ui = ui
        self._is_config = is_config

    def __enter__(self):
        data = self.gen_request_data(self._prompt)
        headers = self.gen_headers()
        req = request.Request(self._req_url, data=data,
                              headers=headers, method='POST')

        if self._is_config:
            self._ui.notify(
                f"\033[94mSending request:\033[0m {self._prompt}\n")
        else:
            self._ui.notify(
                "\033[95mSending GPT configuration request:\033[0m\n")
            self._ui.notify(self._prompt)
            self._ui.notify()

        try:
            with request.urlopen(req) as response:
                if response.status == 200:
                    result = response.read().decode()
                else:
                    raise HagridError(
                        f"FUCK HTTP HARRY! Use ya wand!!", HagridErrorCode.UNKNOWN_ERROR)
        except BaseException as ex:
            raise HagridError(ex, HagridErrorCode.SUPERMIND_INTERFERENCE)
        finally:
            request.urlcleanup()

        return result

    def __exit__(self, cls, value, tb):
        pass

    def gen_request_data(self, prompt):
        data = {
            "model": "gpt-4-0314",
            "messages": [{"role": "user", "content": f"{prompt}"}],
            "temperature": 0.7
        }

        return json.dumps(data).encode()

    def gen_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}"
        }


class UserInterface():
    """Command Line Interface where the user interacts with the application."""

    def __init__(self, taxonomy) -> None:
        self.categories = list(taxonomy.keys())
        self.taxonomy = taxonomy

    def select_prompt(self, options, refined_taxonomy=None):
        taxonomy = refined_taxonomy or self.taxonomy
        print("\n\033[94mPlease select a prompt category:\033[0m")
        self.list_options(options)
        choice = self.get_option(options)
        selected_option = options[choice - 1]
        subcategories = taxonomy[selected_option]

        print(f" - Prompt category: {selected_option}\n")
        print(f"\033[94mPlease select the subcategory:\n\033[0m")
        self.list_options(subcategories, selected_option)
        subcategory_choice = list(subcategories)[
            self.get_option(subcategories) - 1]
        print(f" - Prompt subcategory: {subcategory_choice}")
        print(
            f" - Desc: {taxonomy[selected_option][subcategory_choice]}\n")

        return selected_option, subcategory_choice

    def collect_prompt(self):
        topic = self.get_topic()
        operation_type, subcategory_choice = self.select_prompt(
            self.categories)
        return topic, operation_type, subcategory_choice

    def get_choices(self, refined_taxonomy):
        ipdb.set_trace()
        refined_categories = list(refined_taxonomy)
        operation_type, subcategory_choice = self.select_prompt(
            refined_categories, refined_taxonomy=refined_taxonomy)
        return operation_type, subcategory_choice

    def get_topic(self):
        topic = input("\033[94mPlease enter the initial topic: \033[0m")
        print(f"Topic: {topic}")
        return topic

    def list_options(self, options: list[any], operation_type=None) -> None:
        for i, opt in enumerate(options):
            print(
                f"\033[93m{i + 1}: {str(opt.name).replace('_',' ').lower().capitalize()}\033[0m{' - ' + self.operations[operation_type][opt] if operation_type else ''}")
        print()

    def get_option(self, options: list[any]) -> int:
        """Ensures user selection is in range of options param"""
        choice = input("Your choice: ")
        option = None

        try:
            option = int(choice)
        except ValueError:
            print("Invalid choice. Please choose a valid integer")
            return self.get_option(options)

        if option not in range(1, len(options) + 1):
            print(
                f"Invalid choice. Please choose between {', '.join(map(str, list(range(1, len(options) + 1))))}")
            return self.get_option(options)

        return option

    def notify(self, msg="\n"):
        print(msg)


class FileParser():
    def __init__(self) -> None:
        with open('ex_res.txt') as file:
            self.example_res = ''.join(file.readlines())

        with open('og_prompt.txt') as file:
            self.og_prompt = ''.join(file.readlines())

        with open('reduce_list_prompt.txt') as file:
            self.reduce_list_prompt = ''.join(file.readlines())

        with open('taxonomy.txt') as file:
            lines = file.readlines()
            self.taxonomy = self.convert_taxonomy_text_to_dict(lines)
            self.taxonomy_text = ''.join(lines)

    def convert_taxonomy_text_to_dict(self, lines):
        operations = {}
        current_category = None

        for line in lines:
            line = line.strip()
            if line.endswith(':'):
                current_category = line[:-1]
                operations[current_category] = {}
            elif line.startswith('-'):
                subcategory, description = line[1:].split(':', 1)
                operations[current_category][subcategory.strip()
                                             ] = description.strip()

        return operations


class LLMInterface():
    """Sends and receives data to/from the LLM."""

    def __init__(self):
        self.is_taxonomy_loaded = False

    def load_taxonomy(self, ui, parser):
        try:
            with GPTRequestContextManager(ui=ui, prompt=parser.reduce_list_prompt) as result:
                print(result)
                if result == "understood":
                    self.is_taxonomy_loaded = True
                return result
        except HagridError as ex:
            raise HagridError(ex)

    def refine_taxonomy(self, topic, ui):
        try:
            with GPTRequestContextManager(prompt=topic, ui=ui) as result:
                print(result)
                return self.decode_200_res(result)
        except HagridError as ex:
            raise HagridError(ex)

    def initial_request(self, initial_prompt, ui: UserInterface):
        prompt = self.gen_prompt(initial_prompt)

        try:
            with GPTRequestContextManager(prompt, ui) as result:
                return self.decode_200_res(result)
        except HagridError as ex:
            raise HagridError(ex)

    def enhanced_request(self, enhanced_prompt, ui: UserInterface):
        try:
            with GPTRequestContextManager(prompt=enhanced_prompt, ui=ui) as result:
                return self.decode_200_res(result)
        except HagridError as ex:
            raise HagridError(ex)

    def gen_prompt(self, initial_prompt):
        topic, operation_type, subcategory_choice = initial_prompt

        return f"Topic: {topic}, category: {operation_type}, subcategory: {subcategory_choice}. Please take the topic and create an enhanced prompt based on the category and subcategory. Be as detailed as possible. In the response, do not include anything but the enhanced prompt."

    def decode_200_res(self, res):
        return json.JSONDecoder().decode(res)['choices'][0]['message']['content']


class DataStorage():
    """Stores all prompts and responses for future use."""

    def __init__(self):
        self._con = sqlite3.connect('hagrid.db')
        self._cur = self._con.cursor()

        if not self.table_exists('prompts'):
            self._cur.execute(
                'CREATE TABLE prompts(topic TEXT, operation_type TEXT, subcategory_choice TEXT, enhanced_prompt TEXT, enhanced_res TEXT)')

    def table_exists(self, table_name):
        self._cur.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = self._cur.fetchone()
        return bool(result)

    @catch_errors
    def store_prompt(self, data):
        self._cur.execute(
            "INSERT INTO prompts (topic, operation_type, subcategory_choice, enhanced_prompt, enhanced_res) VALUES (?, ?, ?, ?, ?)", data)
        self._con.commit()


class Mediator():
    """Acts as mediator between other modules"""

    def __init__(self, parser):
        self.db = DataStorage()
        self.llm = LLMInterface()
        self.ui = UserInterface(taxonomy=parser.taxonomy)

    def get_deps(self):
        return self.db, self.llm, self.ui

    def init_gpt(self, parser):
        try:
            return self.llm.load_taxonomy(self.ui, parser)
        except HagridError as ex:
            raise ex

    def get_initial_prompt(self):
        return self.ui.collect_prompt()

    def get_topic(self):
        return self.ui.get_topic()

    def get_choices(self, refined_taxonomy):
        return self.ui.get_choices(refined_taxonomy)

    def refine_taxonomy(self, topic):
        return self.llm.refine_taxonomy(topic, self.ui)

    def make_initial_request(self, initial_prompt):
        return self.llm.initial_request(initial_prompt, self.ui)

    def make_enhanced_request(self, enhanced_prompt):
        return self.llm.enhanced_request(enhanced_prompt, self.ui)

    def store_prompt(self, data):
        return self.db.store_prompt(data)


class Frobnosticator():
    """
    Usage: frob, twiddle, and tweak sometimes connote points along a continuum. ‘Frob’ connotes aimless 
    manipulation; twiddle connotes gross manipulation, often a coarse search for a proper setting; tweak 
    connotes fine-tuning. If someone is turning a knob on an oscilloscope, then if he's carefully adjusting 
    it, he is probably tweaking it; if he is just turning it but looking at the screen, he is probably 
    twiddling it; but if he's just doing it because turning a knob is fun, he's frobbing it. The variant 
    frobnosticate has been recently reported.
    """
    pass


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--no_logs", action="store_true")
    parser.add_argument("--run-tests", action="store_true")
    parser.add_argument("--one-shot", action="store_true")
    return parser.parse_args()


def config_logger(args):
    if args.no_logs == True:
        return logging.getLogger('ye_be_firin_blanks_boyo')
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set level of logger

    # Create handlers
    debug_handler = logging.FileHandler('debug.log')
    debug_handler.setLevel(logging.DEBUG)

    error_handler = logging.FileHandler('error.log')
    error_handler.setLevel(logging.ERROR)

    info_handler = logging.FileHandler('info.log')
    info_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    debug_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)

    return logger


def main(args, logger):
    logger.info(f"app initialised with args: {args}")

    if args.debug == True:
        ipdb.set_trace(context=5)

    parser = FileParser()

    app = Mediator(parser)
    db, llm, ui = app.get_deps()
    try:
        if args.skip == False:
            res = app.init_gpt(parser)
            if res:
                s = 'Prompt taxonomy system loaded into GPT'
                logger.info(s)
                print(f"\033[95m{s}\033[0m\n")

        if args.one_shot == True:
            topic, operation_type, subcategory_choice = app.get_initial_prompt()
        else:
            topic = app.get_topic()
            refined_taxonomy = app.refine_taxonomy(topic)
            new_taxonomy = parser.convert_taxonomy_text_to_dict(
                refined_taxonomy)
            operation_type, subcategory_choice = app.get_choices(new_taxonomy)

        enhanced_prompt = app.make_initial_request(
            (topic, operation_type, subcategory_choice))
        enhanced_res = app.make_enhanced_request(enhanced_prompt)
        app.store_prompt(
            (topic, operation_type, subcategory_choice, enhanced_prompt, enhanced_res))
        print('\033[94mResponse:\033[0m', enhanced_res)
    except HagridError as ex:
        print(f"\033[91mError! {ex}\033[0m")
        logger.exception(ex)
        pdb.post_mortem()


class TestUIInterface(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_hello_world(self):
        self.assertEqual(1, 1)

    @unittest.skip('demo skip')
    def test_nothing(self):
        self.fail('will not happen')


@unittest.skip('skipping test classes')
class TestDataStorage(unittest.TestCase):
    def test_nope(self):
        pass


def create_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestUIInterface('test_hello_world'))
    return suite


if __name__ == '__main__':
    args = get_args()
    logger = config_logger(args)

    if args.run_tests:
        runner = unittest.TextTestRunner(
            stream=sys.stdout, descriptions=True, verbosity=2)
        runner.run(create_test_suite())
        sys.exit()

    main(args, logger)
