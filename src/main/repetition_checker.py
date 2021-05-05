import math


class RepetitionChecker():
    def check(self, word,k):
        '''
        check if word is (k/k-1)^+ free
        performs naive iteration through all substrings and checks if they are succeeded by their substring of sufficient length
        '''
        for i in range(len(word)):
            for j in range(len(word)-i):
                if j==0:
                    continue
                forbidden_length=math.ceil((j+1)/(k-1))
                if i+j+forbidden_length>len(word): # the word is to short to fit a forbidden repetition
                    break
                if word[i:i+forbidden_length]==word[i+j:i+j+forbidden_length]:
                    return (False,i+j+forbidden_length)
        return (True,0)

if __name__=="__main__":
    repetition_checker=RepetitionChecker()
    print(repetition_checker.check("abca",3))
    print(repetition_checker.check("abcab",3))