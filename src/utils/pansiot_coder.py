

class PansiotCoder():
    def decode(self, coding, k, prefix=None):
        if prefix==None:
            prefix=''.join([str(i) for i in range(k-1)])
        alphabet=set(str(i) for i in range(k))
        first_letter=prefix[0]
        rolling_letters=set(letter for letter in prefix)
        for letter in alphabet:
            if letter not in rolling_letters:
                missing_letter=letter
                break
        
        word=prefix
        i=0
        for codeletter in coding:
            i+=1
            if codeletter=="0":
                word+=first_letter
            if codeletter=="1":
                word+=missing_letter
                missing_letter=first_letter
            first_letter=word[i]
        
        return word


    def encode(self, word, k):
        pass


if __name__=="__main__":
    coder=PansiotCoder()
    print(coder.decode("11010111011101011",3))
    print("0120212012102120210")