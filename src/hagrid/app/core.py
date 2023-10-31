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
import time
import argparse
import sqlite3
import json
import logging
import unittest
import pdb
import ipdb


class Category(Enum):
    REDUCTIVE = "Reductive Operations"
    TRANSFORMATIONAL = "Transformational Operations"
    GENERATIVE = "Generative Operations"


class Reductive(Enum):
    SUMMARIZATION = "Summarization"
    DISTILLATION = "Distillation"
    EXTRACTION = "Extraction"
    CHARACTERIZING = "Characterizing"


class Transformational(Enum):
    REFORMATTING = "Reformatting"
    REFACTORING = "Refactoring"
    LANGUAGE_CHANGE = "Language Change"
    RESTRUCTURING = "Restructuring"
    MODIFICATION = "Modification"
    CLARIFICATION = "Clarification"


class Generative(Enum):
    CONTENT_GENERATION = "Content Generation"
    QUESTION_GENERATION = "Question Generation"
    CODE_GENERATION = "Code Generation"
    DIALOGUE_CREATION = "Dialogue Creation"
    SCENARIO_BUILDING = "Scenario Building"
    DATA_SIMULATION = "Data Simulation"
    CREATIVE_WRITING = "Creative Writing"
    INSTRUCTION_GENERATION = "Instruction Generation"
    PREDICTION = "Prediction"
    IDEA_BRAINSTORMING = "Idea Brainstorming"


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


operations = {
    Category.REDUCTIVE: {
        Reductive.SUMMARIZATION: "Condenses long content into shorter form.",
        Reductive.DISTILLATION: "Extracts core principles from complex information.",
        Reductive.EXTRACTION: "Pulls out specific data like names or numbers.",
        Reductive.CHARACTERIZING: "Identifies the nature or genre of the text."
    },
    Category.TRANSFORMATIONAL: {
        Transformational.REFORMATTING: "Changes the presentation style of content.",
        Transformational.REFACTORING: "Rewrites for better efficiency or clarity.",
        Transformational.LANGUAGE_CHANGE: "Translates between natural or coding languages.",
        Transformational.RESTRUCTURING: "Reorders content for logical flow.",
        Transformational.MODIFICATION: "Alters tone, formality, or style.",
        Transformational.CLARIFICATION: "Makes content clearer and more articulate."
    },
    Category.GENERATIVE: {
        Generative.CONTENT_GENERATION: "Creating new text based on a given topic or seed phrase.",
        Generative.QUESTION_GENERATION: "Creating questions based on a given text or context.",
        Generative.CODE_GENERATION: "Writing code snippets or full programs based on user requirements.",
        Generative.DIALOGUE_CREATION: "Generating conversational exchanges between characters or agents.",
        Generative.SCENARIO_BUILDING: "Creating hypothetical situations or case studies.",
        Generative.DATA_SIMULATION: "Generating synthetic data sets for testing or analysis.",
        Generative.CREATIVE_WRITING: "Generating poems, songs, or other forms of creative text.",
        Generative.INSTRUCTION_GENERATION: "Creating step-by-step guides or tutorials.",
        Generative.PREDICTION: "Making forecasts based on given data or trends",
        Generative.IDEA_BRAINSTORMING: "Generating a list of ideas or solutions for a given problem."
    }
}

operations_map = {
    Category.REDUCTIVE: list(map(lambda x: (x.value, operations[Category.REDUCTIVE][x]), Reductive)),
    Category.TRANSFORMATIONAL: list(map(lambda x: (x.value, operations[Category.TRANSFORMATIONAL][x]), Transformational)),
    Category.GENERATIVE: list(
        map(lambda x: (x.value, operations[Category.GENERATIVE][x]), Generative))
}


def gen_taxonomy():
    output = ""
    for category, operations in operations_map.items():
        output += (f"\nCategory: {category.value}\n")
        for operation in operations:
            output += (f" - {operation[0]}: {operation[1]}\n")
    return output


intro_prompt = f"You are a master logistician, linguist and teacher. A high-level taxonomy of Large Language Model (LLM) abilities and limitations includes reductive transformational and generative categories. Assuming each category is prefaced with 'Category:', and each subcategory is prefixed with ' - ', store the following:\n{gen_taxonomy()}\nThe prompt following this one will include a topic, category and subcategory so that you can elaborate on how to apply these to generate an enhanced prompt, based on the stored taxonomy. If the following prompt is a repeat of this prompt, ignore this prompt. If this is understood, please reply with 'understood'"


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
    def __init__(self, prompt=None, ui=None) -> None:
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

    def __enter__(self):
        data = self.gen_request_data(self._prompt)
        headers = self.gen_headers()
        req = request.Request(self._req_url, data=data,
                              headers=headers, method='POST')

        if self._prompt:
            self._ui.notify(
                f"\033[94mSending request:\033[0m {self._prompt}\n")
        else:
            self._ui.notify(
                "\033[95mSending GPT configuration request:\033[0m\n")
            self._ui.notify(intro_prompt)
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

    def gen_request_data(self, prompt=intro_prompt):
        data = {
            "model": "gpt-3.5-turbo",
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

    def __init__(self) -> None:
        self.categories = list(Category)
        self.operations = operations.copy()

    def collect_prompt(self) -> tuple[str, Category, Reductive | Transformational | Generative]:
        """Collects initial topic and prompt category from the user."""
        topic = input("\033[94mPlease enter the initial topic: \033[0m")
        print(f"Topic: {topic}")

        print("\n\033[94mPlease select a prompt category:\033[0m")

        self.list_options(self.categories)

        category_choice = self.get_option(self.categories)

        operation_type = self.categories[category_choice - 1]
        subcategories = self.operations[operation_type]

        print(
            f" - Prompt category: {operation_type.value}\n")

        print(
            f"\033[94mPlease select the subcategory:\n\033[0m")

        self.list_options(subcategories, operation_type)

        subcategory_choice = list(subcategories)[
            self.get_option(subcategories) - 1]

        print(
            f" - Prompt subcategory: {subcategory_choice.value}")
        print(
            f" - Desc: {self.operations[operation_type][subcategory_choice]}\n")

        return topic, operation_type.value, subcategory_choice.value

    def list_options(self, options: list[any], operation_type=None) -> None:
        for i, opt in enumerate(options):
            print(
                f"\033[93m{i + 1}: {str(opt.name).replace('_',' ').lower().capitalize()}\033[0m{' - ' + self.operations[operation_type][opt] if operation_type else ''}")
        print()

    def get_option(self, options: list[any]) -> int:
        """Ensures user selection is in range of options param"""
        option_choice = input("Your choice: ")
        choice_number = None  # TODO: this var name is awful.

        try:
            choice_number = int(option_choice)
        except ValueError:
            print("Invalid choice. Please choose a valid integer")
            return self.get_option(options)

        if choice_number not in range(1, len(options) + 1):
            print(
                f"Invalid choice. Please choose between {', '.join(map(str, list(range(1, len(options) + 1))))}")
            return self.get_option(options)

        return choice_number

    def notify(self, msg="\n"):
        print(msg)


class LLMInterface():
    """Sends and receives data to/from the LLM."""

    def __init__(self):
        self.is_taxonomy_loaded = False
        with FileContextManager('reduce_list_prompt.txt') as file:
            self.reduce_list_prompt = ''.join(file.readlines())

    def load_taxonomy(self, ui):
        try:
            with GPTRequestContextManager(ui=ui, prompt=self.reduce_list_prompt) as result:
                if result == "understood":
                    self.is_taxonomy_loaded = True
                return result
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


class Manager():
    """Acts as mediator between other modules"""

    def __init__(self):
        self.db = DataStorage()
        self.llm = LLMInterface()
        self.ui = UserInterface()

    def get_deps(self):
        return self.db, self.llm, self.ui

    def init_gpt(self):
        try:
            return self.llm.load_taxonomy(self.ui)
        except HagridError as ex:
            raise ex

    def get_initial_prompt(self):
        return self.ui.collect_prompt()

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
    logger.info("app initialised")

    if args.debug == True:
        ipdb.set_trace(context=5)

    app = Manager()
    db, llm, ui = app.get_deps()
    try:
        if args.skip == False:
            res = app.init_gpt()
            if res:
                s = 'Prompt taxonomy system loaded into GPT'
                logger.info(s)
                print(f"\033[95m{s}\033[0m\n")

        topic, operation_type, subcategory_choice = app.get_initial_prompt()
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
