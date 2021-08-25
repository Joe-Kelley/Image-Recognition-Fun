# Code Modified from: http://lucylabs.gatech.edu/kbai/fall-2021/project-overview/

import os
import sys
import csv
import pandas as pd

from agent_main import Agent


def getNextLine(r):
    return r.readline().rstrip()


# The project's main solve method. This will generate the agent's answers to all the current problems.
def solve():
    sets = []  # Store all problems

    r = open(os.path.join("Basic Problems", "ProblemList.txt"))  # ProblemList.txt lists the problems to solve.
    line = getNextLine(r)
    while not line == "":
        sets.append(line)
        line = getNextLine(r)

    # Initializing problem-solving agent
    agent = Agent()

    # Running agent against each problem
    with open("AgentAnswers.csv", "w") as results:

        results.write("Problem Name,Agent's Answer,Actual Answer\n")
        for set in sets:
            answer = agent.read_image(set)
            r = open(os.path.join("Basic Problems", set, "ProblemAnswer.txt"))
            line = getNextLine(r)
            while not line == "":
                correct_answer = line
                line = getNextLine(r)

            results.write("%s,%d,%s\n" % (set, answer, correct_answer))
    r.close()
    display_answers()


def check_answers(row):
    if row['Agent\'s Answer'] == row['Actual Answer']:
        return 'True'
    else:
        return 'False'


# def grade(row):
#     if row['Correct?']:
#         return 'True'
#     else:
#         return 'False'


def display_answers():
    df = pd.read_csv("AgentAnswers.csv")
    df['Correct?'] = df.apply(lambda row: check_answers(row), axis=1)
    print(df)
    print('Results:\n', df['Correct?'].value_counts())
    pass


# The main execution will have your agent generate answers for all the problems,
def main():
    solve()


if __name__ == "__main__":
    main()
