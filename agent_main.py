import numpy as np
import cv2
import random


class Agent:
    # The default constructor for the agent
    def __init__(self):
        pass

    def read_image(self, problem):
        if problem.problemType == "2x2":
            # Print the Problem Set Name and Problem for Debugging
            print(problem.name)
            answer_arr = []

            imageA = cv2.imread(problem.figures['A'].visualFilename)
            imageB = cv2.imread(problem.figures['B'].visualFilename)
            imageC = cv2.imread(problem.figures['C'].visualFilename)
            image1 = cv2.imread(problem.figures['1'].visualFilename)
            image2 = cv2.imread(problem.figures['2'].visualFilename)
            image3 = cv2.imread(problem.figures['3'].visualFilename)
            image4 = cv2.imread(problem.figures['4'].visualFilename)
            image5 = cv2.imread(problem.figures['5'].visualFilename)
            image6 = cv2.imread(problem.figures['6'].visualFilename)

            imagesInputs = [imageA, imageB, imageC]
            imagesAnswers = {"1": image1, "2": image2, "3": image3, "4": image4, "5": image5, "6": image6}
            potentialAnswers = {"1": image1, "2": image2, "3": image3, "4": image4, "5": image5, "6": image6}


def main():
    print("Test")


if __name__ == "__main__":
    main()