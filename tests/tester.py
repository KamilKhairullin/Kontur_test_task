class Tester():

    """Class for evaluating model's metrics:
       - F1-Score
       - Lower case char-by-char consistensy of two files 
    """

    def __init__(self, test_file, predicted_file):
        self.test_file = test_file
        self.predicted_file = predicted_file

    """ evaluate_F1() Evaluates F1-score of predicted file based on test file

    Returns: void

    Prints the result to console.
    """
    def evaluate_F1(self):
        TP = 0
        FP = 1e-10 #add small float number to avoid 'divide by zero' error
        TN = 0
        FN = 1e-10 #add small float number to avoid 'divide by zero' error
        
        #open and read test file
        read_A=open(self.test_file ,'r',  encoding='utf-8').read()
        #open and read train file
        read_B=open(self.predicted_file,'r',  encoding='utf-8').read()

        #TP FP TN FN evaluation
        for char_a, char_b in zip(read_A, read_B):
            if char_a.isupper() and char_b.isupper():
                TP += 1
            elif char_a.islower() and char_b.isupper():
                FP += 1
            elif char_a.islower() and char_b.islower():
                TN += 1
            elif char_a.isupper() and char_b.islower():
                FN += 1

        presicion = TP / (TP + FP) 
        recall = TP / (TP + FN) 
        F1 = (2 * presicion * recall) / (presicion + recall)

        #rounding to avoid an incorrect result due to the addition of float in FP and FN
        if F1 < 1e-10:
           F1 = 0
        print(F1)
        

    """ evaulate_consistency() Evaluates consistency between predicted and test files.
    Due to the fact that the measurement will take place char-by-char 
    we need to make sure that the letters, not counting the casing, are in the same places.

    Returns: void

    Prints the result to console. 
    Result is the sum of same letters divided by number of all letters.
    Prints "1" if consistent. Everything else is inconsistent.
    """
    def evaulate_consistency(self):
        cnt_same = 0
        cnt_all = 0
        read_A=open(self.test_file ,'r',  encoding='utf-8').read()
        read_B=open(self.predicted_file,'r',  encoding='utf-8').read()

        for char_a, char_b in zip(read_A, read_B):
            cnt_all += 1
            if char_a.lower() == char_b.lower():
                cnt_same += 1
        print(cnt_same/cnt_all)


        


