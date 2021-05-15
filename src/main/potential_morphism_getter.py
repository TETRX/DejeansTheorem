# from ..utils.all_morphism_values import AllMophismValues
from ..utils.all_morphism_values_backtracking import AllMophismValuesB
from ..utils.permutation_func import PermutationFunc
from .morphism_checker import MorphismChecker
from ..utils.morphism import Morphism
from ..utils.pansiot_coder import PansiotCoder
from ..utils.repetition_checker import RepetitionChecker



class PotentialMorphismGetter():

    def __init__(self, morphism_checker, repetition_checker, pansiot_coder) -> None:
        self.morphism_checker = morphism_checker
        self.repetition_checker=repetition_checker
        self.pansiot_coder=pansiot_coder

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
        unfiltered_morphism_values=AllMophismValuesB(4*k-4,self.repetition_checker,self.pansiot_coder, k)
        perm_func=PermutationFunc(k)

        potential_vals={
            "0": [],
            "1": []
        }
        for morphism_val in unfiltered_morphism_values:
            perm=perm_func.value(morphism_val)
            if perm.cycle_structure=={1:1, k-1:1}:
                potential_vals["0"].append(morphism_val)
                for potential_one in potential_vals["1"]:
                    if potential_one[-1]!=morphism_val[-1]:
                        vals={
                            "0": morphism_val,
                            "1": potential_one
                        }
                        h=Morphism(vals)
                        if self.morphism_checker.check(h,k):
                            return vals
            elif perm.cycle_structure=={k:1}:
                potential_vals["1"].append(morphism_val)
                for potential_zero in potential_vals["0"]:
                    if potential_zero[-1]!=morphism_val[-1]:
                        vals={
                            "0": potential_zero,
                            "1": morphism_val
                        }
                        h=Morphism(vals)
                        if self.morphism_checker.check(h,k):
                            return vals
        return potential_vals

if __name__=="__main__":
    from datetime import datetime
    start=datetime.now()
    pansiot_coder=PansiotCoder()
    morphism_checker=MorphismChecker(pansiot_coder)
    repetition_checker=RepetitionChecker()
    pmg=PotentialMorphismGetter(morphism_checker,repetition_checker,pansiot_coder)
    import json
    print(json.dumps(pmg.get(16)))
    print(datetime.now()-start)
    