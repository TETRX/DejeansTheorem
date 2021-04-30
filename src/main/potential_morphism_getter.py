from itertools import product
from ..utils.permutation_func import PermutationFunc

class AllMophismValues():
    '''
    Custom iterator that iterates through strings on alphabet {0,1} of length seq_length that have the bare minimum potential for being conivenient.
    What I mean by "bare minimum potential" is they satisfy the following 2 conditions:
    1. They start with "1"
    1. They don't contain "00" as a substring
    These are enough to guarantee h^omega(0) doesn't contain "00" as a substring.

    We could iterate through all strings and check if they satisfy the conditions, but we can implement a trick.
    Since the seq_length are of length divisible by 4 we can take all 9 possible configurations of length 4 and iterate through those.
    Because of that we eliminate a significant amount of bad sequences in O(1) time for all (as opposed to O(seq_length) for each)

    We do this by defining a "fake alphabet", on which we iterate and convert to words on {0,1}.
    '''

    FAKE_ALPHABET_TO_REAL={
        "A": "0101",
        "B": "0110",
        "C": "0111",
        "D": "1010",
        "E": "1011",
        "F": "1101",
        "G": "1110",
        "H": "1111"
    }
    def __init__(self,seq_length):
        '''
        params:
        - seq_length - length of h(0), needs to be divisible by 4
        '''
        self.seq_length=seq_length
        self.fake_seq=product(["D","E","F","G","H"],product("ABCCDEFGH", repeat=seq_length//4-1))

    def __iter__(self):
        return self

    FORBIDDEN_TWOS={"BA","BB","BC","DA", "DB", "DC", "GA", "GB", "GC" }
    def check_conditions(self,word):
        for i in range(self.seq_length//4-2):
            # print(word[i:i+2])
            if word[i:i+2] in AllMophismValues.FORBIDDEN_TWOS:
                # print(word, word[i:i+2])
                return False
        return True

    def get_fake_next(self):
        unprocessed_fake_next=self.fake_seq.__next__()
        return ''.join((unprocessed_fake_next[0],)+unprocessed_fake_next[1])

    def get_real(self, word):
        return ''.join([AllMophismValues.FAKE_ALPHABET_TO_REAL[letter] for letter in word])

    def __next__(self):
        fake_next=self.get_fake_next()
        while not self.check_conditions(fake_next):
            fake_next=self.get_fake_next()
        
        real_next=self.get_real(fake_next)
        return real_next


class PotentialMorphismGetter():

    def get(self, k):
        '''
        params:
        - k - alphabet cardinality
        returns:
        a dict of format:
        {
            "0":[
                list of potential h(0) values
            ]
            "1":[
                list of potential h(1) values
            ]
        }
        Potential h(x) values are decided based on cycle decomposition of sigma_k(h(x)). Indeed, h needs to fullfill the algebraic condition,
        which means cycle decomposition of sigma_k(h(x)) needs to be the same (in the sense of the length of cycles) as h(x).
        This means that sigma_k(h(0)) needs to have cycles of lengths k-1 and 1, and sigma_k(h(1)) needs to have a single cycle of length k
        '''
        unfiltered_morphism_values=AllMophismValues(4*k-4)
        perm_func=PermutationFunc(k)

        potential_vals={
            "0": [],
            "1": []
        }

        for morphism_val in unfiltered_morphism_values:
            perm=perm_func.value(morphism_val)
            if perm.cycle_structure=={1:1, k-1:1}:
                potential_vals["0"].append(morphism_val)
            elif perm.cycle_structure=={k:1}:
                potential_vals["1"].append(morphism_val)

        return potential_vals

if __name__=="__main__":
    pmg=PotentialMorphismGetter()
    print(pmg.get(4))
    