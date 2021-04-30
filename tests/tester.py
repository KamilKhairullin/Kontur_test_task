class Tester():

    def __init__(self, test_file, predicted_file):
        self.test_file = test_file
        self.predicted_file = predicted_file

    def evaluate_F1(self):
        TP = 0
        FP = 1e-10
        TN = 0
        FN = 1e-10
        
        read_A=open(self.test_file ,'r',  encoding='utf-8').read()
        read_B=open(self.predicted_file,'r',  encoding='utf-8').read()

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
        if F1 < 1e-10:
           F1 = 0
        print(F1)
        
    def evaulate_consistency(self):
        cnt_true = 0
        cnt_all = 0
        read_A=open(self.test_file ,'r',  encoding='utf-8').read()
        read_B=open(self.predicted_file,'r',  encoding='utf-8').read()

        for char_a, char_b in zip(read_A, read_B):
            cnt_all += 1
            if char_a.lower() == char_b.lower():
                cnt_true += 1
        print(cnt_true/cnt_all)


        


