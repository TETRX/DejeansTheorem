from itertools import product



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
        # self.fake_seq=product(["D","E","F","G","H"],product("ABCCDEFGH", repeat=seq_length//4-1)) # 5*8^(k-2)
        self.first_letter=iter(["D","E","F","G","H"])
        self.curr_first_letter=self.first_letter.__next__() #Always "D", but it sets self.first_letter() in the correct position

        self.rest_of_letters=product("ABCCDEFGH", repeat=seq_length//4-1)
        # TODO: I think the inner product is not accessed lazily causing the program to use ludicrous amounts of RAM. Fix!
         
    
    def __iter__(self):
        return self

    FORBIDDEN_TWOS={"BA","BB","BC","DA", "DB", "DC", "GA", "GB", "GC" }
    def check_conditions(self,word):
        for i in range(self.seq_length//4-2):
            if word[i:i+2] in AllMophismValues.FORBIDDEN_TWOS:
                return False
        return True

    def get_fake_next(self):
        try:
            letters=self.rest_of_letters.__next__()
        except StopIteration:
            self.curr_first_letter=self.first_letter.__next__()
            print(self.curr_first_letter)
            self.rest_of_letters=product("ABCCDEFGH", repeat=self.seq_length//4-1)
            letters=self.rest_of_letters.__next__()
        return ''.join((self.curr_first_letter,)+letters)

    def get_real(self, word):
        return ''.join([AllMophismValues.FAKE_ALPHABET_TO_REAL[letter] for letter in word])

    def __next__(self):
        fake_next=self.get_fake_next()
        while not self.check_conditions(fake_next):
            fake_next=self.get_fake_next()
        
        real_next=self.get_real(fake_next)
        return real_next
