import numpy as np
import cv2
import random


class Agent:
    # The default constructor for the agent
    def __init__(self):
        # Final Answer Guesses
        self.answer_guesses = []
        pass

    # Helper function using cv2 template matching and tm_ccoeff_normed to determine if two images are within a tolerance
    # threshold of being the same image
    def sameImages(self, image1, image2):
        result = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)
        if result > .9:
            return True
        else:
            return False

    # Helper Function for deleting inital images that we don't think will be the answer
    def eliminateImages(self, input_dict, image_dict, potential_ans):
        for key in image_dict:
            if self.sameImages(input_dict['A'], image_dict[key]) or self.sameImages(input_dict['B'], image_dict[key]) or self.sameImages(input_dict['C'], image_dict[key]):
                # print("Eliminated: ", key)
                del potential_ans[key]

        return potential_ans


    # Helper Function for Calculating DPR
    # DPR calculation modified from:
    # https://www.davidjoyner.net/blog/wp-content/uploads/2015/05/JoynerBedwellGrahamLemmonMartinezGoel-ICCC2015-Distribution.pdf
    # We will return the number of Black Pixels, White Pixels, and the DPR under each key
    def calculateDPR(self, imagesDict):
        imageDictDPR = {}
        for key in imagesDict:
            numBlackPix = np.sum(imagesDict[key] == 0)
            numWhitePix = np.sum(imagesDict[key] == 255)
            dpr = numBlackPix / (numWhitePix + numBlackPix)
            if dpr == 0:
                dpr = .00000001
            imageDictDPR[key] = numBlackPix, numWhitePix, dpr
        return imageDictDPR

    # Helper Function for Calculating IPR
    # IPR calculation modified from:
    # https://www.davidjoyner.net/blog/wp-content/uploads/2015/05/JoynerBedwellGrahamLemmonMartinezGoel-ICCC2015-Distribution.pdf
    def calcIPR(self, image1, image2):
        check = (image1 == 0)[image2 == 0]
        numSharedBlackPix = sum(check)
        numBlackPix1 = np.sum(image1 == 0)
        numBlackPix2 = np.sum(image2 == 0)
        if numBlackPix1 == 0 or numBlackPix2 == 0:
            ipr = 0
        else:
            ipr = (numSharedBlackPix / numBlackPix1) - (numSharedBlackPix / numBlackPix2)
        return ipr

    def read_image(self, problem):
        self.answer_guesses = []
        path = 'Basic Problems\\%s\\' % problem

        imageA = cv2.imread(path + "A.png")
        imageB = cv2.imread(path + "B.png")
        imageC = cv2.imread(path + "C.png")

        input_images_dict = {'A': imageA, 'B': imageB, 'C': imageC}

        image_answers_dict = {}
        key = 1
        while key < 7:
            image_answers_dict[key] = cv2.imread(path + '%s.png' % str(key))
            key += 1

        # For Debugging and viewing images easily ---
        # cv2.imshow("", imageA)
        # cv2.waitKey(0)
        # cv2.imshow("", image_answers_dict[1])
        # cv2.waitKey(0)

        answers = self.solve_problem(input_images=input_images_dict, image_answers=image_answers_dict)
        if len(answers) == 0:
            answers = [0]
        # print(answers)
        if len(answers) > 1:
            print(answers)
            answers = random.choice(answers)
            return answers
        else:
            return answers[0]

    # We will attempt to find our best guesses for the problem in this method
    def solve_problem(self, input_images, image_answers):
        # Copy of the answers, so we can keep a running dictionary of our current guesses to solve the problem
        potential_answers = image_answers.copy()

        # Let's check if the input images are the same. A&B A&C B&C
        abSame = self.sameImages(image1=input_images['A'], image2=input_images['B'])
        acSame = self.sameImages(image1=input_images['A'], image2=input_images['C'])
        bcSame = self.sameImages(image1=input_images['B'], image2=input_images['C'])

        # If none of the input images are the same, we assume the answer won't include an image from the input images ..
        # so, let's delete any matching images from the potential answer dictionary
        if not abSame and not acSame and not bcSame:
            potential_answers = self.eliminateImages(input_dict=input_images, image_dict=image_answers, potential_ans=potential_answers)

        # All Input Images are Same Image -> Find same image
        if abSame and acSame:
            for key in potential_answers:
                check = self.sameImages(image1=input_images['A'], image2=potential_answers[key])
                if check:
                    self.answer_guesses.append(int(key))

        # Input Images are only Same Across Horizontal
        if abSame and not acSame:
            for key in potential_answers:
                check = self.sameImages(image1=input_images['C'], image2=potential_answers[key])
                if check:
                    self.answer_guesses.append(int(key))

        # Input Images are only Same Across Vertical
        if acSame and not abSame:
            for key in potential_answers:
                check = self.sameImages(image1=input_images['B'], image2=potential_answers[key])
                if check:
                    self.answer_guesses.append(int(key))

        # Bitwise checks
        if len(self.answer_guesses) == 0:
            row1XOR = np.logical_xor(input_images['A'], input_images['B'])
            row1AND = np.logical_and(input_images['A'], input_images['B'])
            row1OR = np.logical_or(input_images['A'], input_images['B'])
            row1XOR = row1XOR.astype(np.uint8)
            row1XOR *= 255
            row1AND = row1AND.astype(np.uint8)
            row1AND *= 255
            row1OR = row1OR.astype(np.uint8)
            row1OR *= 255
            if self.sameImages(image1=row1AND, image2=input_images['B']):
                for key in potential_answers:
                    row2AND = np.logical_and(input_images['C'], potential_answers[key])
                    row2AND = row2AND.astype(np.uint8)
                    row2AND *= 255
                    # cv2.imshow("", row2AND)
                    # cv2.waitKey(0)
                    if self.sameImages(image1=row2AND, image2=input_images['C']):
                        self.answer_guesses.append(int(key))
            if self.sameImages(image1=row1XOR, image2=input_images['B']):
                for key in potential_answers:
                    row2XOR = np.logical_xor(input_images['C'], potential_answers[key])
                    row2XOR = row2XOR.astype(np.uint8)
                    row2XOR *= 255
                    # cv2.imshow("", row2AND)
                    # cv2.waitKey(0)
                    if self.sameImages(image1=row2XOR, image2=input_images['C']):
                        self.answer_guesses.append(int(key))
            if self.sameImages(image1=row1OR, image2=input_images['B']):
                for key in potential_answers:
                    row2OR = np.logical_or(input_images['C'], potential_answers[key])
                    row2OR = row2OR.astype(np.uint8)
                    row2OR *= 255
                    # cv2.imshow("", row2AND)
                    # cv2.waitKey(0)
                    if self.sameImages(image1=row2OR, image2=input_images['C']):
                        self.answer_guesses.append(int(key))


        # DPR and IPR are more resource intensive so if we already have an asnwer because the problem is basic,
        # Then let us skip this
        if len(self.answer_guesses) == 0:
            # Let's Calculate the Dark Pixel Ratio of the Input Image Dictionary
            input_images_DPR = self.calculateDPR(imagesDict=input_images)

            # Let's Calculate the Dark Pixel Ratio of the Potential Answers
            answer_images_DPR = self.calculateDPR(imagesDict=potential_answers)

            # IPR Checks
            abIPR = self.calcIPR(image1=input_images['A'], image2=input_images['B'])
            acIPR = self.calcIPR(image1=input_images['A'], image2=input_images['C'])

            # Let's Calculate the DPR Ratio for A&B and A&C
            abPerc = (input_images_DPR['B'][2] - input_images_DPR['A'][2]) / input_images_DPR['A'][2]
            acPerc = (input_images_DPR['C'][2] - input_images_DPR['A'][2]) / input_images_DPR['A'][2]
            for key in potential_answers:
                # If the DPR ratio of input image C and the current key is within +- .05 of the AB DPR then True
                ab_DPR_match = abPerc - .05 <= ((answer_images_DPR[key][2] - input_images_DPR['C'][2]) / input_images_DPR['C'][2]) <= abPerc + .05
                ab_IPR_match = abIPR - .001 <= self.calcIPR(image1=input_images['C'], image2=potential_answers[key]) <= abIPR + .001
                # If the DPR ratio of input image B and the current key is within +- .05 of the AC DPR then True
                ac_DPR_match = acPerc - .05 <= ((answer_images_DPR[key][2] - input_images_DPR['B'][2]) / input_images_DPR['B'][2]) <= acPerc + .05
                ac_IPR_match = acIPR - .001 <= self.calcIPR(image1=input_images['B'], image2=potential_answers[key]) <= acIPR + .001
                if ab_DPR_match and ab_IPR_match:
                    self.answer_guesses.append(int(key))
                elif ac_DPR_match and ac_IPR_match:
                    self.answer_guesses.append(int(key))

        return self.answer_guesses


def main():
    print("Test")


if __name__ == "__main__":
    main()
