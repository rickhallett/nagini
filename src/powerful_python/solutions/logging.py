'''

This is the file your logger will log to:
>>> LOGFILE
'logging-basic.txt'

To make this lab pass, in the code section, you need to do the
following:

1) Invoke logging.basicConfig() with the correct arguments.
   (Hint: set level, format and filename.)
3) Define the pet_log() function.


Let's first test the log level threshold. 
>>> logging.debug('debug message')
>>> logging.info('info message')
>>> logging.warning('warning message')
>>> logging.error('error message')
>>> logging.critical('critical message')

The log file ought to have records only of INFO or greater.  We'll use
the print_log() function (defined for you below) to check the log file
contents:

>>> print_log()
INFO - info message
WARNING - warning message
ERROR - error message
CRITICAL - critical message


Now define the function pet_log():

>>> pet_log({ "day": "Tuesday", "species": "dog", "destination": "Central Park"})
>>> pet_log({ "day": "Saturday", "species": "cat", "destination": "the lake" })

And check that it adds some new records:

>>> print_log()
INFO - info message
WARNING - warning message
ERROR - error message
CRITICAL - critical message
CRITICAL - On Tuesday, I'm taking my dog to Central Park.
CRITICAL - On Saturday, I'm taking my cat to the lake.

'''

LOGFILE = 'logging-basic.txt'

def print_log():
    "Prints out what's written to the log file so far."
    print(open(LOGFILE).read(), end="")

# This "with" line resets the log file to be empty,
# each time you run the test:
with open(LOGFILE, 'w'): pass
    
# Write your code here:

import logging

logging.basicConfig(
    level=logging.INFO,
    filename=LOGFILE,
    format='%(levelname)s - %(message)s',
    )

def pet_log(info):
    logging.critical("On %(day)s, I'm taking my %(species)s to %(destination)s.", info)

# Do not edit any code below this line!

if __name__ == '__main__':
    import doctest
    count, _ = doctest.testmod()
    if count == 0:
        print('*** ALL TESTS PASS ***\nGive someone a HIGH FIVE!')

# Part of Powerful Python. Copyright MigrateUp LLC. All rights reserved.
