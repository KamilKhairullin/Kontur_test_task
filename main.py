import nltk
import models.truecaser as tc
import tests.tester as tester
import string

#path with unknown casing data
test_path = 'tests/test_1.txt'
#where to save predictions
pred_path = 'tests/test_2.txt'

model = tc.Truecaser()
#load model
#model.load_model('model.obj')

#fit model with train data.
tokens = model.fit(test_path)
model.train()

#(!!!) to save model, at first create empty model.obj
#model.save_model('model.obj')

#clear predict file 
file = open(pred_path, 'w')
file.close()


buffer = 5000 # saves data to file each N lines
counter = 0 #count processed lines
block = 0 #saved block number
answer = ""

for sentence in open(test_path, encoding='utf-8'):
    #get rid of 'new line' symbol
    sentence = sentence.strip('\n')
    #split sentence into tokens divided by space
    tokens = sentence.split(" ")
    #make them lowercase
    tokens_lower = [token.lower() for token in tokens]
    #predict sentence
    x = model.predict(tokens_lower)

    #join prediction with spaces
    x = " ".join(x)
    #add new line symbol to the end of sentence
    answer = answer + x + '\n'
    counter = counter  + 1
    if counter == buffer:
        counter = 0
        block += 1
        print('start writing to file.. Block [' + str(block) + "] of size " + str(buffer) + " lines")
        predict_file = open(pred_path, "a", encoding='utf-8')
        predict_file.write(answer)
        predict_file.close()
        print('ended writing to file .. ')
        answer = ""
   
predict_file = open(pred_path, "a", encoding='utf-8')
predict_file.write(answer)
predict_file.close()
print('Ended.')

eval = tester.Tester(test_path, pred_path)
eval.evaluate_F1()
eval.evaulate_consistency()

