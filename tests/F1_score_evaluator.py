class F1Evaluator():

    def __init__(self, test_file, predicted_file):
        self.test_file = test_file
        self.predicted_file = predicted_file

    def evaluate(self):
        TP = 0
        FP = 1e-10
        TN = 0
        FN = 1e-10

        file = open('tests/log.txt', 'w')
        file.close()

        log = open('tests/log.txt', "a")
        read_A=open(self.test_file ,'r',  encoding='utf-8')#.read()
        read_B=open(self.predicted_file,'r',  encoding='utf-8')#.read()

        for line1, line2 in zip(read_A, read_B):
            for char_a, char_b in zip(line1, line2):
                #log.write(char_a)
                #log.write(" ") 
                #log.write(char_b)
                #log.write("\n")
                if char_a.isupper() and char_b.isupper():
                    TP += 1
                elif char_a.islower() and char_b.isupper():
                    FP += 1
                elif char_a.islower() and char_b.islower():
                    TN += 1
                elif char_a.isupper() and char_b.islower():
                    FN += 1
        log.close()
        print(TP, FP, TN, FN)
        presicion = TP / (TP + FP) 
        recall = TP / (TP + FN) 
        F1 = (2 * presicion * recall) / (presicion + recall)
        if F1 < 1e-10:
           F1 = 0
        print(F1)


        


