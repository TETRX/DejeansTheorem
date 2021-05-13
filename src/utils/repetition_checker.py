import math


class RepetitionChecker():
    def check(self, word,k, already_checked=0):
        '''
        check if word is (k/k-1)^+ free
        performs naive iteration through all substrings and checks if they are succeeded by their substring of sufficient length

        params:
        - word - the word to check
        - k - cardinality of the alphabet
        - already_checked - length of the prefix guaranteed to be (k/k-1)^+ free
        '''
        for i in range(len(word)-1):
            for j in range(max(i+1,((k-1)*already_checked+i)//k),len(word)):
                '''
                j>=((k-1)already_checked+i)/k
                '''
                forbidden_length=math.ceil((j+1)/(k-1))
                if j+forbidden_length>len(word): # the word is to short to fit a forbidden repetition
                    break
                if word[i:i+forbidden_length]==word[j:j+forbidden_length]:
                    return (False,j+forbidden_length)
        return (True,0)

if __name__=="__main__":
    repetition_checker=RepetitionChecker()
    print(repetition_checker.check("abca",3))
    print(repetition_checker.check("abcab",3))
    print(repetition_checker.check("abcab",3,already_checked=3))