class Morphism():
    def __init__(self, letters_val: dict):
        self.letters_val=letters_val

    def calculate(self, word):
        return ''.join([self.letters_val[letter] for letter in word])

    def __mul__(self, other):
        letters_val={}
        for letter in self.letters_val:
            letters_val[letter]=self.calculate(other.calculate(letter))
        return Morphism(letters_val)

    def identity(self):
        letters_val={}
        for letter in self.letters_val:
            letters_val[letter]=letter
        return Morphism(letters_val)

    def __pow__(self, exp):
        ret_val=self.identity()
        scaler=Morphism(self.letters_val)
        while exp>0:
            if exp%2==1:
                ret_val*=scaler
            scaler*=scaler
            exp>>=1
        return ret_val

if __name__=='__main__':
    morphism=Morphism(
        {
            "0": "01",
            "1": "10"
        })
    print(morphism.calculate("0110"))
    print((morphism*morphism).calculate("0110"))
    print((morphism**4).calculate("0110"))