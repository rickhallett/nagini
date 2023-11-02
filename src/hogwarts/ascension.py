"""
### Multidimensional Skills:
1. **Technical Mastery**: Proficiency in programming languages, understanding of algorithms and data structures.
2. **Architectural Insight**: Skills in system design, knowledge of design patterns, and architectural best practices.
3. **Problem-Solving Wizardry**: Ability to troubleshoot, debug, and find creative solutions to complex problems.
4. **Enchanted Communication**: Clarity in code documentation, effective communication skills, ability to articulate technical concepts.
5. **Potions (Tools & Technologies)**: Familiarity with various tools, frameworks, and emerging technologies.
6. **Divination (Future Readiness)**: Keeping up with industry trends, learning new technologies, and adapting to changes.
7. **Arcane Collaboration**: Teamwork skills, ability to work effectively in diverse teams, conflict resolution.
8. **Transfiguration**: Leadership qualities, ability to mentor and guide others, project management skills.
9. **Charms of Influence**: Networking skills, ability to influence and persuade, public speaking and presentation skills.
10. **Legilimency**: Emotional intelligence, ability to understand and respond to the needs of team members and stakeholders.
11. **Defense Against the Dark Arts (Security & Ethics)**: Knowledge of security best practices, ethical considerations in coding and technology.

### Advancement and Recognition:
- Coders can advance in each dimension independently, allowing them to focus on areas of interest or strength.
- Recognition can be given for achievements in specific dimensions, not just overall coding prowess.
"""

from queue import Queue
from enum import Enum, auto


class WizardRank(Enum):
    MUGGLE = auto()
    HOGWARTS_INITIATE = auto()
    JUNIOR_WIZARD = auto()
    MAGICIAN = auto()
    WIZARD = auto()
    AUROR = auto()
    MAGUS = auto()
    SWORD_OF_MERLIN = auto()
    RIGHT_HAND_OF_DUMBLEDORE = auto()
    DUMBLEDORE = auto()
    LEGEND_OF_THE_DEATHLY_HALLOWS = auto()
    ARCHMAGE = auto()
    ASCENDANT = auto()


class Dimension(Enum):
    """
    1. **Technical Mastery**: Proficiency in programming languages, understanding of algorithms and data structures.
    2. **Architectural Insight**: Skills in system design, knowledge of design patterns, and architectural best practices.
    3. **Problem-Solving Wizardry**: Ability to troubleshoot, debug, and find creative solutions to complex problems.
    4. **Enchanted Communication**: Clarity in code documentation, effective communication skills, ability to articulate technical concepts.
    5. **Potions (Tools & Technologies)**: Familiarity with various tools, frameworks, and emerging technologies.
    6. **Divination (Future Readiness)**: Keeping up with industry trends, learning new technologies, and adapting to changes.
    7. **Arcane Collaboration**: Teamwork skills, ability to work effectively in diverse teams, conflict resolution.
    8. **Transfiguration**: Leadership qualities, ability to mentor and guide others, project management skills.
    9. **Charms of Influence**: Networking skills, ability to influence and persuade, public speaking and presentation skills.
    10. **Legilimency**: Emotional intelligence, ability to understand and respond to the needs of team members and stakeholders.
    11. **Defense Against the Dark Arts (Security & Ethics)**: Knowledge of security best practices, ethical considerations in coding and technology.
    """
    TECHNICAL_MASTERY = auto()
    ARCHITECTURAL_INSIGHT = auto()
    PROBLEM_SOLVING_WIZARDRY = auto()
    ENCHANTED_COMMUNICATION = auto()
    POTIONS = auto()
    DIVINATION = auto()
    ARCANE_COLLABORATION = auto()
    TRANSFIGURATION = auto()
    CHARMS_OF_INFLUENCE = auto()
    LEGILIMENCY = auto()
    DEFENSE_AGAINST_THE_DARK_ARTS = auto()


class Hogwarts:
    def __init__(self):
        self.wizards = []
        self.registration_queue = Queue()

    def register_wizard(self, wizard):
        if isinstance(wizard, Wizard):
            self.registration_queue.put(wizard)

    def process_registrations(self):
        while not self.registration_queue.empty():
            new_wizard = self.registration_queue.get()
            self.wizards.append(new_wizard)
            print(f"{new_wizard.name} has been registered.")

    def get_wizard_by_name(self, name):
        for wizard in self.wizards:
            if wizard.name == name:
                return wizard
        return None

    def update_dimension(self, wizard_name, dimension, value):
        wizard = self.get_wizard_by_name(wizard_name)
        if wizard and isinstance(dimension, Dimension):
            wizard.update_dimension(dimension, value)

    def determine_ascension(self, wizard_name):
        wizard = self.get_wizard_by_name(wizard_name)
        if not wizard:
            return

        total_score = sum(wizard.dimensions.values())
        if total_score >= 120:
            wizard.set_rank(WizardRank.ASCENDANT)
        elif total_score >= 110:
            wizard.set_rank(WizardRank.ARCHMAGE)
        elif total_score >= 100:
            wizard.set_rank(WizardRank.LEGEND_OF_THE_DEATHLY_HALLOWS)
        elif total_score >= 90:
            wizard.set_rank(WizardRank.DUMBLEDORE)
        elif total_score >= 80:
            wizard.set_rank(WizardRank.RIGHT_HAND_OF_DUMBLEDORE)
        elif total_score >= 70:
            wizard.set_rank(WizardRank.SWORD_OF_MERLIN)
        elif total_score >= 60:
            wizard.set_rank(WizardRank.MAGUS)
        elif total_score >= 50:
            wizard.set_rank(WizardRank.AUROR)
        elif total_score >= 40:
            wizard.set_rank(WizardRank.WIZARD)
        elif total_score >= 30:
            wizard.set_rank(WizardRank.MAGICIAN)
        elif total_score >= 20:
            wizard.set_rank(WizardRank.JUNIOR_WIZARD)
        elif total_score >= 10:
            wizard.set_rank(WizardRank.HOGWARTS_INITIATE)
        else:
            wizard.set_rank(WizardRank.MUGGLE)

    def __str__(self):
        return f"\nHogwarts Wizards: {[wizard.pretty_print() for wizard in self.wizards]}"


class Wizard:
    def __init__(self, name):
        self.name = name
        self.rank = WizardRank.MUGGLE
        self.dimensions = {dimension: 0 for dimension in Dimension}

    def set_rank(self, rank):
        if isinstance(rank, WizardRank):
            self.rank = rank

    def update_dimension(self, dimension, value):
        if dimension in Dimension and isinstance(value, int):
            self.dimensions[dimension] = value

    def get_rank(self):
        return self.rank

    def get_dimension(self, dimension):
        return self.dimensions.get(dimension, None)

    def __str__(self):
        dimension_str = {dim.name: level for dim,
                         level in self.dimensions.items()}
        return f"Name: {self.name}, Rank: {self.rank.name}, Dimensions: {dimension_str}"

    def pretty_print(self):
        print(f"Name: {self.name}")
        print(f"Rank: {self.rank.name.replace('_', ' ').title()}")
        print(f"Power: {sum(self.dimensions.values())}")
        print("Dimensions:")
        for dim, level in self.dimensions.items():
            print(f"  - {dim.name.replace('_', ' ').title()}: Level {level}")
        print("-"*50)
        return self.name


hogwarts = Hogwarts()

harry = Wizard("Harry")
dumbledore = Wizard("Dumbledore")

hogwarts.register_wizard(harry)
hogwarts.register_wizard(dumbledore)
hogwarts.process_registrations()

hogwarts.update_dimension("Harry", Dimension.TECHNICAL_MASTERY, 4)
hogwarts.update_dimension("Harry", Dimension.ARCHITECTURAL_INSIGHT, 3)
hogwarts.update_dimension("Harry", Dimension.PROBLEM_SOLVING_WIZARDRY, 4)
hogwarts.update_dimension("Harry", Dimension.ENCHANTED_COMMUNICATION, 4)
hogwarts.update_dimension("Harry", Dimension.POTIONS, 4)
hogwarts.update_dimension("Harry", Dimension.DIVINATION, 5)
hogwarts.update_dimension("Harry", Dimension.ARCANE_COLLABORATION, 6)
hogwarts.update_dimension("Harry", Dimension.TRANSFIGURATION, 5)
hogwarts.update_dimension("Harry", Dimension.CHARMS_OF_INFLUENCE, 6)
hogwarts.update_dimension("Harry", Dimension.LEGILIMENCY, 7)
hogwarts.update_dimension("Harry", Dimension.DEFENSE_AGAINST_THE_DARK_ARTS, 1)

hogwarts.update_dimension("Dumbledore", Dimension.TECHNICAL_MASTERY, 9)
hogwarts.update_dimension("Dumbledore", Dimension.ARCHITECTURAL_INSIGHT, 8)
hogwarts.update_dimension("Dumbledore", Dimension.PROBLEM_SOLVING_WIZARDRY, 8)
hogwarts.update_dimension("Dumbledore", Dimension.ENCHANTED_COMMUNICATION, 9)
hogwarts.update_dimension("Dumbledore", Dimension.POTIONS, 8)
hogwarts.update_dimension("Dumbledore", Dimension.DIVINATION, 8)
hogwarts.update_dimension("Dumbledore", Dimension.ARCANE_COLLABORATION, 8)
hogwarts.update_dimension("Dumbledore", Dimension.TRANSFIGURATION, 8)
hogwarts.update_dimension("Dumbledore", Dimension.CHARMS_OF_INFLUENCE, 9)
hogwarts.update_dimension("Dumbledore", Dimension.LEGILIMENCY, 8)
hogwarts.update_dimension(
    "Dumbledore", Dimension.DEFENSE_AGAINST_THE_DARK_ARTS, 7)

hogwarts.determine_ascension("Harry")
hogwarts.determine_ascension("Dumbledore")


print(hogwarts)
