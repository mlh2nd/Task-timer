# TaskTimer.py
#
# Copyright 2018 Michael Hess II
#
# TaskTimer allows the user to set an expected amount of time to complete a
# given task, and then to time that task. Completed tasks are written to a file
# for recordkeeping.
#
# TaskTimer was inspired by the following quote:
#     Decide how long a time is required for a given task, and then bend every
#     effort toward accomplishing the work in the given time. The exercise of
#     the willpower will make the hands move deftly. (1MCP 6)
#       --Ellen White, Mind, Character, and Personality, Vol. 1, p. 6
 
from datetime import date       
from time import time, sleep          
from os import system           

################################################################################
# File designations
################################################################################

# File to record tasks during actual use
hist_file = "C:\\users\\mlh2n\\documents\\productivity\\taskhistory.csv"
# File to record test input
test_file = "C:\\users\\mlh2n\\documents\\programming\\python\\taskhistory.csv"
# Use hist_file as the one to record to unless user specifies otherwise.
record = hist_file

################################################################################
# Function definitions
################################################################################

def display(filename):
    """ Function to display previously recorded tasks """
    print('\n')
    with open(filename) as task_file:
        for line in task_file:
            print(line)

def stopwatch(name="stopwatch", color="07"):
    """Simple stopwatch function to time tasks"""
    total_elapsed = 0
    while True:
        starter_text = "\nPress Enter to start " + name + ". "
        starter = input(starter_text)
        system("color " + color)
        system("title " + name)
        start = time()
        print("Stopwatch running...")
        stopper_text = "Press Enter to stop " + name + ". "
        stopper = input(stopper_text)
        stop = time()
        elapsed = stop - start
        total_elapsed += elapsed
        print("Time elapsed:", total_elapsed, "seconds")
        if stopper == "pause":
            print("Stopwatched paused...")
            continue
        else:
            return total_elapsed

def help():
    """ Function to explain how to use the program """
    print("\nType the name of your next task (e.g. \"grading Algebra 1 HW\")",
          "\nto get started. Or type one of the following commands:\n",
          "\n\texit\t\texit TaskTimer",
          "\n\thistory\t\tdisplay previously recorded tasks",
          "\n\ttesting\t\tuse a test file for task history",
          "\n\tnormal\t\tuse the normal file for task history",
          "\n\thelp\t\tdisplay this help menu",
          "\n\topen\t\topen task history file",
          "\n\tclear\t\tclear the screen")

def manual():
    """ Manually add a task to the record """
    print("\nManually add a completed task.")
    task_name = input("What was the task? ")
    if task_name == "cancel":
        return 1
    task_date = input("What date was the task completed? ")
    task_exp = input("How many minutes did you allot? ")
    task_act = input("How many minutes did you take? ")
    file_string = task_date + ',' + task_name + ',' + task_exp + ',' + task_act
    print("Is this correct?\n", file_string)
    proceed = input()
    if proceed == ('yes'):
        with open(record, 'a') as task_file:
            task_file.write(file_string)
    else:
        manual()

def color(arg):
    """ Set the screen colors """
    call = "color " + arg
    system(call)


################################################################################
# Color schemes
################################################################################

norm_col = '1b'     # color scheme for normal mode
test_col = '0a'     # color scheme for testing mode
task_col = '5f'     # color scheme while timing a task
ontime_col = 'af'   # color displayed if task completed on time
overtime_col = 'cf' # color displayed if task takes too long


################################################################################
# Main program
################################################################################

col = norm_col      # Set initial color scheme to normal. Variable col may be
                    # reassigned as test_col

# Welcome screen
color(col)
system("title TaskTimer")
print("""Welcome to TaskTimer!\n
Decide how long a time is required for a given task, and then bend every
effort toward accomplishing the work in the given time. The exercise of
the willpower will make the hands move deftly.
--Ellen White, Mind, Character, and Personality, Vol. 1, p. 6\n\n
Let's start timing your tasks!""")

# Program
while True:
    color(col)  # col will be either the normal color or the testing color
    # Get task name
    current_task = input("\n\nWhat's your next task? ")
    # Special commands: "exit" to quit the program, "history" to display
    # recorded tasks, "testing" to save to a test file instead of the main
    # history, "normal" to save to the normal location, "help" to display a
    # help menu.
    if current_task == "exit":
        break
    elif current_task == "history":
        display(record)
        continue
    elif current_task == "open":
        print("\nOpening task history file...")
        print("Close file to continue.")
        system(record)
        continue
    elif current_task == "testing":
        record = test_file
        col = test_col
        color(col)
        print("\nTaskTimer is now in testing mode. Task data will be saved",
              "\nto a test file instead of the main record.")
        continue
    elif current_task == "normal":
        record = hist_file
        col = norm_col
        color(col)
        print("\nTaskTimer is now in normal mode. Task data will be saved",
              "\nto the main record.")
        continue
    elif current_task == "help":
        help()
        continue
    elif current_task == "clear":
        system('cls')
        continue
    elif current_task == "manual":
        manual()
        continue
    
    # Get allotted time
    expected_mins = input("How many minutes do you think you'll need? ")
    # Allow user to cancel the task if desired
    if expected_mins == "cancel":
        print("Task cancelled.")
    else:   
        expected_time = float(expected_mins) * 60
        # Run stopwatch function to time the task
        actual_time = stopwatch(current_task, task_col)
        # Compute and compare times
        actual_mins = actual_time / 60                  
        int_mins = int(actual_time // 60)
        secs = int(actual_time % 60)
        print("\nYou spent", int_mins, "minute(s) and",
              secs, "second(s) on", current_task + ".")
        if actual_time > expected_time:
            color(overtime_col)
            print("Hmm. That took longer than expected.")
            sleep(1)
        else:
            color(ontime_col)
            print("Great! You completed", current_task,
                  "within the allotted time.")
            sleep(1)
        system("title TaskTimer")

        # Write data to file
        file_string = str(date.today().strftime("%y-%m-%d") + ', ' +
                          current_task + ', ' + str(expected_mins) + ', ' +
                          str(actual_mins) + '\n')
        with open(record, 'a') as task_file:
            task_file.write(file_string)

# Exit message
print("\n\nThanks for using TaskTimer! Bye for now.\n")
sleep(2)


