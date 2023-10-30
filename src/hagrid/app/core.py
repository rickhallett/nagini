# -*- coding: utf-8 -*-
# from .helpers import get_answer
from enum import Enum
from urllib import request
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

prompts = {
    Category.REDUCTIVE: {
        "choice": "Please select your form of reduction",
    },
    Category.TRANSFORMATIONAL: {
        "choice": "Please select your form of transformation"
    },
    Category.GENERATIVE: {
        "choice": "Please select your form of generation"
    }
}


class UserInterface():
    """Command Line Interface where the user interacts with the application."""

    def __init__(self) -> None:
        self.categories = list(Category)
        self.operations = operations.copy()

    def collect_prompt(self) -> tuple[str, Category, Reductive | Transformational | Generative]:
        """Collects initial topic and prompt category from the user."""
        # topic = click.prompt("\033[94mPlease enter the initial topic\033[0m")
        topic = "Soon, you will become magnificent"
        click.echo(f"Topic: {topic}")

        click.echo("\n\033[94mPlease select a prompt category:\033[0m")

        self.list_options(self.categories)

        category_choice = self.get_option(self.categories)
        # category_choice = 1

        operation_type = self.categories[category_choice - 1]
        subcategories = self.operations[operation_type]

        click.echo(
            f" - Prompt category: {operation_type.value}\n")

        click.echo(f"\033[94m{prompts[operation_type]['choice']}\033[0m")

        self.list_options(subcategories, operation_type)

        subcategory_choice = list(subcategories)[
            self.get_option(subcategories) - 1]

        click.echo(
            f" - Prompt subcategory: {subcategory_choice.value}")
        click.echo(
            f" - Desc: {self.operations[operation_type][subcategory_choice]}\n")

        return topic, operation_type, subcategory_choice

    def list_options(self, options: list[any], operation_type=None) -> None:
        for i, opt in enumerate(options):
            click.echo(
                f"\033[93m{i + 1}: {str(opt.name).replace('_',' ').lower().capitalize()}\033[0m{' - ' + self.operations[operation_type][opt] if operation_type else ''}")
        click.echo()

    def make_readable(self, category) -> str:
        return str(category.name).replace('_', '').lower().capitalize()

    def get_option(self, options: list[any]) -> int:
        """Ensures user selection is in range of options param"""
        option_choice = click.prompt("Your choice", type=int)
        while option_choice not in range(1, len(options) + 1):
            click.echo(
                f"Invalid choice. Please choose between {', '.join(map(str, list(range(1, len(options)))))}")
            option_choice = click.prompt("Your choice", type=int)
        return option_choice


class LLMInterface():
    """Sends and receives data to/from the LLM."""

    def request():
        req = request.urlopen('https://jsonplaceholder.typicode.com/todos/1')
        print(req)

    pass


class DataStorage():
    """Stores all prompts and responses for future use."""
    pass


class Manager():
    """Acts as mediator between other modules"""

    def __init__(self, db, llm, ui):
        self.db = db
        self.llm = llm
        self.ui = ui

    def start(self):
        topic, operation_type, subcategory_choice = ui.collect_prompt()
        print(topic, operation_type, subcategory_choice)


@click.command()
def init_prompt():
    ui.collect_prompt()


if __name__ == '__main__':
    db = DataStorage()
    llm = LLMInterface()
    ui = UserInterface()
    app = Manager(db, llm, ui)
    app.start()

"""

The Mediator pattern defines an object that encapsulates how a set of objects interact. It promotes loose 
coupling by keeping objects from referring to each other explicitly, and it allows their interaction to vary 
independently.

Advantages of the Mediator (Manager) pattern:

1. Reduced Coupling: The pattern limits direct communication between the objects (UserInterface, DataStorage, 
LLMInterface) which reduces the dependencies between them, leading to lower coupling.

2. Increased Flexibility: Changes to the system can be made more easily because interactions between objects 
are centralized in one location.

3. Simplifies Maintenance and Understanding: It's easier to understand and maintain the interaction logic 
that is concentrated in one place rather than spread across individual classes.

Disadvantages of the Mediator (Manager) pattern:

1. Can Become Overly Complex: If the mediator becomes too complex, it can become a monolith or god object, 
which is an object that knows too much or does too much. This can make the mediator itself hard to maintain.

2. Indirect Communication: The pattern can decrease the performance of the system as all communication is 
done indirectly, through the mediator.

Alternative patterns:

1. Facade Pattern: This pattern provides a simplified interface to a larger body of code. It can make a 
software library easier to use and understand, since the facade has convenient methods for common tasks.

2. Observer Pattern: This pattern is used when there is one-to-many relationship between objects such as 
if one object is modified, its dependent objects are to be notified automatically.

3. Command Pattern: This pattern allows you to encapsulate actions in objects. The key idea is to provide 
means to decouple client from receiver.

Choosing the right pattern depends on the specific needs and complexity of your software.

"""
