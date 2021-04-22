import nltk 

def getCasing(word):  
    """ Returns the casing of a word"""
    if len(word) == 0:
        return 'other'
    elif word.isdigit(): #Is a digit
        return 'numeric'
    elif word.islower(): #All lower case
        return 'allLower'
    elif word.isupper(): #All upper case
        return 'allUpper'
    elif word[0].isupper(): #is a title, initial char upper, then all lower
        return 'initialUpper'
    
    return 'other'

def checkSentenceSanity(sentence):
#    """ Checks the sanity of the sentence. If the sentence is for example all uppercase, it is recjected"""
#    caseDist = nltk.FreqDist()
#    
#    for token in sentence:
#        caseDist[getCasing(token)] += 1
#    
#    if caseDist.most_common(1)[0][0] != 'allLower':        
#        return True
    
    return True

def train(text, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist):
  # :: Create unigram lookup ::
  for sentence in text:
      if not checkSentenceSanity(sentence):
          continue
      
      for tokenIdx in range(1, len(sentence)):
          word = sentence[tokenIdx]
          uniDist[word] += 1
                      
          if word.lower() not in wordCasingLookup:
              wordCasingLookup[word.lower()] = set()
          
          wordCasingLookup[word.lower()].add(word)
          
  
  # :: Create backward + forward bigram lookup ::
  for sentence in text:
      if not checkSentenceSanity(sentence):
          continue
      
      for tokenIdx in range(2, len(sentence)): #Start at 2 to skip first word in sentence
          word = sentence[tokenIdx]
          wordLower = word.lower()
          
          if wordLower in wordCasingLookup and len(wordCasingLookup[wordLower]) >= 2: #Only if there are multiple options
              prevWord = sentence[tokenIdx-1]
              
              backwardBiDist[prevWord+"_"+word] +=1
              
              if tokenIdx < len(sentence)-1:
                  nextWord = sentence[tokenIdx+1].lower()
                  forwardBiDist[word+"_"+nextWord] += 1
                  
  # :: Create trigram lookup ::
  for sentence in text:
      if not checkSentenceSanity(sentence):
          continue
      
      for tokenIdx in range(2, len(sentence)-1): #Start at 2 to skip first word in sentence
          prevWord = sentence[tokenIdx-1]
          curWord = sentence[tokenIdx]
          curWordLower = curWord.lower()
          nextWordLower = sentence[tokenIdx+1].lower()
          
          if curWordLower in wordCasingLookup and len(wordCasingLookup[curWordLower]) >= 2: #Only if there are multiple options   
              trigramDist[prevWord+"_"+curWord+"_"+nextWordLower] += 1

  return (uniDist, backwardBiDist, forwardBiDist, trigramDist, wordCasingLookup)
