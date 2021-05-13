

class AllMophismValuesB():
    def __init__(self,seq_length, repetition_checker, pansiot_coder, k):
        self.seq_length=seq_length
        self.curr_val=["1"] #starts with "1"

        self.pansiot_coder=pansiot_coder
        self.encoded_prefix=pansiot_coder.default_prefix(k)

        self.repetition_checker=repetition_checker

        self.k=k

    def check(self, curr_val):
        # print(''.join(curr_val))
        if len(curr_val)>1:
            # print(self.curr_val[-2:])
            if curr_val[-2:]==["0","0"]:
                return False
        encoded_word=self.pansiot_coder.decode(curr_val[len(self.encoded_prefix)-self.k+1:], self.k, prefix=self.encoded_prefix)
        print(encoded_word)
        self.encoded_prefix=encoded_word
        return self.repetition_checker.check(encoded_word, self.k)

    def limit_prefix_length(self, limit):
        '''
        limit is the index on which the curr_val and previous curr_val definitely diverge
        '''
        if len(self.encoded_prefix)>=limit+self.k-2:
            self.encoded_prefix=self.encoded_prefix[:limit+self.k-2]
    
    def backtrack(self):
        while self.curr_val[-1]=="1":
            self.curr_val.pop()
            if self.curr_val==[]:
                raise StopIteration()
        self.curr_val[-1]="1"
        self.limit_prefix_length(len(self.curr_val)-2)

    def __next__(self):
        if len(self.curr_val)==self.seq_length:
            if self.curr_val[-1]=="0":
                self.curr_val[-1]="1"
                self.limit_prefix_length(len(self.curr_val)-2)
                if self.check(self.curr_val):
                    return ''.join(self.curr_val)
            self.backtrack()

        while len(self.curr_val)<self.seq_length:
            self.curr_val.append("0")
            if not self.check(self.curr_val):
                self.curr_val[-1]="1"
                self.limit_prefix_length(len(self.curr_val)-2)
                if not self.check(self.curr_val):
                    self.backtrack()
        return ''.join(self.curr_val)

    def __iter__(self):
        return self

if __name__=="__main__":
    from .repetition_checker import RepetitionChecker
    from .pansiot_coder import PansiotCoder
    repetition_checker = RepetitionChecker()
    pansiot_coder = PansiotCoder()
    am=AllMophismValuesB(12, repetition_checker, pansiot_coder,3)

    for val in am:
        print(val)