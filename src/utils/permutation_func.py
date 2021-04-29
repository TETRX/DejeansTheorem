from sympy.combinatorics import Permutation

class PermutationFunc:
    def __init__(self, k):
        self.k=k
        common_start= [i+1 for i in range(k-2)]
        zero_list=common_start+[0,k-1]
        # print(zero_list)
        one_list=common_start+[k-1,0]
        # print(one_list)
        self.zero=Permutation(zero_list)
        # print(self.zero)
        self.one=Permutation(one_list)
        # print(self.one)

    def value(self, word):
        value=Permutation([i for i in range(self.k)])
        for letter in word:
            if letter=="0":
                value*=self.zero
            elif letter=="1":
                value*=self.one
        return value

if __name__=="__main__":
    perm_func=PermutationFunc(4)
    print(perm_func.value("111"))