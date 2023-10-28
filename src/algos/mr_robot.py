"""
Robot Challenge

Blue and Orange are friendly robots. An evil computer mastermind has locked them up in
separate hallways to test them, and then possibly give them cake. The robots cannot
communicate with each other.

Each hallway contains 100 buttons labeled with the positive integers {1, 2, ..., 100}. Button k
is always k metres from the start of the hallway, and the robots both begin at button 1. Over
the period of one second, a robot can walk one meter in either direction, or it can press the
button at its position once, or it can stay at its position and not press the button. To complete
the test, the robots need to push a certain sequence of buttons in a certain order. Both
robots know the full sequence in advance.

How would you program a method to determine the minimum time to run the
sequence?

For example, let's consider the following button sequence: 'O 2, B 1, B 2, O 4'

Here, O 2 means button 2 in Orange's hallway, B 1 means button 1 in Blue's hallway, and so on. 
The robots can push this particular sequence of buttons in 6 seconds, e.g:

Time    Orange          Blue
1       moves to 2      stays at 1
2       presses 2       stays at 1
3       moves to 3      presses 1
4       moves to 4      move to 2
5       stay at 4       presses 2
5       presses 4       stays at 2

Note: the robots cannot push a button at the same time.

for each cmd
  compare cmd position to current position and move that many steps + button press
  update position and total time taken

provided you take into account the time to press buttons, you dont need to worry about button conflicts

it is the *time taken* that is more important here than what a robot is doing in a given amount of time

as we always know the time taken for the previous command, we can work out if the currently examined command
is *behind* the other one, and so can move without incrementing total time taken
"""


def is_equal(actual: int, expected: int, msg: str) -> [str, int]:
    if actual != expected:
        return [f"FAIL {msg}", actual]
    else:
        return [f"PASS {msg}", actual]


def get_action(cmd: str):
    return cmd.strip().split(' ')


def parse(sequence: str):
    return map(get_action, sequence.split(','))


def time(sequence: list[str]) -> int:
    min_time = 0
    blue_pos = 0
    orange_pos = 0
    blue_time = 0
    orange_time = 0
    for [action, position] in parse(sequence):
        if (action == "O"):
            time_needed = abs(blue_pos - position) + 1
            blue_time = min([blue_time + time_needed, min_time + 1])
            blue_pos = position
        else:
            time_needed = abs(orange_pos - position) + 1
            orange_time = min([orange_time + time_needed, min_time + 1])
            orange_pos = position
        min_time = max(orange_time, blue_time)
    return min_time


print(is_equal(time('O 2, B 1, B 2, O 4'), 6, "'O 2, B 1, B 2, O 4' => 6"))
print(is_equal(time('O 5, O 8, B 100'), 100, "'O 5, O 8, B 100' => 100"))
print(is_equal(time('B 2, B 1'), 4, "'O 5, O 8, B 100' => 6"))
