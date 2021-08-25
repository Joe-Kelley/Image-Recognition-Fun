# Code Modified from: http://lucylabs.gatech.edu/kbai/fall-2021/project-overview/

import os
import sys
import csv

from agent_main import Agent


def getNextLine(r):
    return r.readline().rstrip()


# The project's main solve method. This will generate the agent's answers to all the current problems.
def solve():
    sets=[] # The variable 'sets' stores multiple problem sets.

    r = open(os.path.join("Basic Problems", "ProblemList.txt"))    # ProblemList.txt lists the sets to solve.
    line = getNextLine(r)
    while not line=="":
        sets.append(line)
        line=getNextLine(r)

    # Initializing problem-solving agent from Agent.java
    agent=Agent()   # Your agent will be initialized with its default constructor.
                    # You may modify the default constructor in Agent.java

    # Running agent against each problem set
    with open("AgentAnswers.csv", "w") as results:     # Results will be written to ProblemResults.csv.
                                                        # Note that each run of the program will overwrite the previous results.
                                                        # Do not write anything else to ProblemResults.txt during execution of the program.
        results.write("Problem Name,Agent's Answer\n")
        for set in sets:
            answer = agent.read_image(set)  # The problem will be passed to your agent as a RavensProblem object as a parameter to the Solve method
                                            # Your agent should return its answer at the conclusion of the execution of Solve.

            results.write("%s,%d\n" % (set, answer))
    r.close()

# The main execution will have your agent generate answers for all the problems,
# then generate the grades for them.
def main():
    solve()


if __name__ == "__main__":
    main()
