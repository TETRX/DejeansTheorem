

class PansiotCoder():
    def decode(self, coding, k, prefix=None):
        if prefix==None:
            # prefix=''.join([chr(ord('a') + i) for i in range(k-1)])
            prefix=[chr(ord('a') + i) for i in range(k-1)]
        alphabet=set(chr(ord('a') + i) for i in range(k))
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
                word.append(first_letter)
            if codeletter=="1":
                word.append(missing_letter)
                missing_letter=first_letter
            first_letter=word[i]
        
        # return word
        return ''.join(word)


    def encode(self, word, k): # for now probably not needed
        pass


if __name__=="__main__":
    coder=PansiotCoder()
    print(coder.decode("11010111011101011",3))
    print("abcacbcabcbacbcacba")