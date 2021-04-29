
from ..utils.pansiot_coder import PansiotCoder
from ..utils.morphism import Morphism
import math

class MorphismChecker():
    def __init__(self, pansiot_coder):
        self.pansiot_coder=pansiot_coder

    def check(self, h, k):
        to_decode=(h**2).calculate("0110")
        word_to_check= self.pansiot_coder.decode(to_decode,k)
        # print(word_to_check)
        # 1. check kernel repetitions 
        # 2. check short repetitions

        # 1. iterate through all substrings e of length k-1, put them into a set, if we ever try to put an element into the set that was already there, we have a kernel repetition
        # We don't have to worry about these words overlapping since word_to_check is a Pansiot word, so the first letter e_1 of any repeating e which is a (k-1)-substring can occur in word_to_check only once every k-1 letters. 
        substrings_so_far=set()
        curr_word=word_to_check[:k-1]
        i=k
        while i<len(word_to_check):
            if curr_word in substrings_so_far:
                return False
            substrings_so_far.add(curr_word)
            curr_word=curr_word[1:]+word_to_check[i]
            i+=1

        # 2. Do a naive iteration through all subwords pe of size such that e of size less than k-1 would be sufficient for an exponent bigger than (k+1)/k
        # k-1>|e|>|p|/(k-1)
        # |p|<(k-1)(k-1)
        for p_length in range((k-1)**2):
            if p_length==0:
                continue
            # |e|>|p|/(k-1)
            e_length=math.ceil((p_length+1)/(k-1))
            for i in range(len(word_to_check)-p_length-e_length):
                if word_to_check[i:i+e_length]==word_to_check[i+p_length:i+p_length+e_length]:
                    print(word_to_check[i:i+p_length+e_length])
                    return False

        return True


if __name__=="__main__":
    pansiot_coder=PansiotCoder()
    checker=MorphismChecker(pansiot_coder)
    morphism=Morphism({
        "0":"1010101010101010101101101011011010101010101011010110110110101101",
        "1":"1010101010101010101101101101101010101010110110110110110110110110"
    })
    print(checker.check(morphism,17))