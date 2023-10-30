# -*- coding: utf-8 -*-
# from .helpers import get_answer
from enum import Enum
from urllib import request
import json
import os
import argparse
import click

"""
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
        self._org = os.getenv("OPENAI_API_ORG")
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
        topic = click.prompt("\033[94mPlease enter the initial topic\033[0m")
        # topic = "Soon, you will become magnificent"
        click.echo(f"Topic: {topic}")

        click.echo("\n\033[94mPlease select a prompt category:\033[0m")

        self.list_options(self.categories)

        category_choice = self.get_option(self.categories)
        # category_choice = 1

        operation_type = self.categories[category_choice - 1]
        subcategories = self.operations[operation_type]

        click.echo(
            f" - Prompt category: {operation_type.value}\n")

        click.echo(
            f"\033[94mPlease select the subcategory:\n\033[0m")

        self.list_options(subcategories, operation_type)

        subcategory_choice = list(subcategories)[
            self.get_option(subcategories) - 1]

        click.echo(
            f" - Prompt subcategory: {subcategory_choice.value}")
        click.echo(
            f" - Desc: {self.operations[operation_type][subcategory_choice]}\n")

        return (topic, operation_type.value, subcategory_choice.value)

    def list_options(self, options: list[any], operation_type=None) -> None:
        for i, opt in enumerate(options):
            click.echo(
                f"\033[93m{i + 1}: {str(opt.name).replace('_',' ').lower().capitalize()}\033[0m{' - ' + self.operations[operation_type][opt] if operation_type else ''}")
        click.echo()

    def get_option(self, options: list[any]) -> int:
        """Ensures user selection is in range of options param"""
        option_choice = click.prompt("Your choice", type=int)
        while option_choice not in range(1, len(options) + 1):
            click.echo(
                f"Invalid choice. Please choose between {', '.join(map(str, list(range(1, len(options)))))}")
            option_choice = click.prompt("Your choice", type=int)

        return option_choice

    def notify(self, msg="\n"):
        print(msg)


class LLMInterface():
    """Sends and receives data to/from the LLM."""

    def __init__(self):
        self.is_taxonomy_loaded = False

    def load_taxonomy(self, ui):
        try:
            with GPTRequestContextManager(ui=ui) as result:
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
    pass


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


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", action="store_true")
    args = parser.parse_args()

    app = Manager()
    db, llm, ui = app.get_deps()
    try:
        # app.start()
        if args.skip == False:
            res = app.init_gpt()
            if res:
                print("\033[95mPrompt taxonomy system loaded into GPT\033[0m\n")

        initial_prompt = app.get_initial_prompt()
        enhanced_prompt = app.make_initial_request(initial_prompt)
        enhanced_res = app.make_enhanced_request(enhanced_prompt)
        print('\033[94mResponse:\033[0m', enhanced_res)
        # llm.initial_request()
    except HagridError as ex:
        print(f"\033[91mError! {ex}\033[0m")
