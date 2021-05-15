# from ..utils.all_morphism_values import AllMophismValues
from sympy.combinatorics import permutations
from sympy.utilities.iterables import signed_permutations
from ..utils.all_morphism_values_backtracking import AllMophismValuesB
from ..utils.permutation_func import PermutationFunc
from .morphism_checker import MorphismChecker
from ..utils.morphism import Morphism
from ..utils.pansiot_coder import PansiotCoder
from ..utils.repetition_checker import RepetitionChecker

from sympy.combinatorics import Permutation


class PotentialMorphismGetter():

    def __init__(self, morphism_checker, repetition_checker, pansiot_coder) -> None:
        self.morphism_checker = morphism_checker
        self.repetition_checker=repetition_checker
        self.pansiot_coder=pansiot_coder

    def potential_taus_str(self,sigma_1,sigma_0):
        permutations=self.potential_taus(sigma_1,sigma_0)

        return [str(permutation) for permutation in permutations]

    def potential_taus(self,sigma_1,sigma_0):
        '''
        returns list of taus such that:
        tau*sigma_1*tau^-1=sigma_0
        '''
        k=sigma_1.size

        taus=[]

        # calculate one possible tau
        tau={
        }
        if sigma_1.cycle_structure=={k:1}:
            for i in range(k):
                tau[(sigma_0**i)(0)]=(sigma_1**i)(0)

        elif sigma_1.cycle_structure=={k-1:1, 1:1}:
            for cycle in sigma_1.full_cyclic_form:
                if len(cycle)==1:
                    fixed_point_1=cycle[0]

            for cycle in sigma_0.full_cyclic_form:
                if len(cycle)==1:
                    fixed_point_0=cycle[0]

            tau[fixed_point_0]=fixed_point_1        
            
            # find element not in big cycle
            first_of_rest_0=0 if not fixed_point_0==0 else 1
            first_of_rest_1=0 if not fixed_point_1==0 else 1
            
            # print(first_of_rest_0, first_of_rest_1)

            for i in range(k):
                tau[(sigma_0**i)(first_of_rest_0)]=(sigma_1**i)(first_of_rest_1)

        tau_list=[tau[i] for i in range(k)]
        tau_first=Permutation(tau_list)
        # print(tau_first*sigma_1*(tau_first**-1))
        # print(sigma_0)

        return {sigma_0**i*tau_first for i in range(k)}

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

        SIGMA_0=perm_func.value("0")
        SIGMA_1=perm_func.value("1")

        potential_vals={
            "0": dict(),
            "1": dict()
        }
        for morphism_val in unfiltered_morphism_values:
            perm=perm_func.value(morphism_val)
            if perm.cycle_structure=={1:1, k-1:1}:
                taus=self.potential_taus_str(perm,SIGMA_0)
                for tau in taus:
                    if tau in potential_vals["0"]:
                        potential_vals["0"][tau].append(morphism_val)
                    else:
                        potential_vals["0"][tau]=[morphism_val]

                for tau in taus:
                    if tau in potential_vals["1"]:
                        for potential_one in potential_vals["1"][tau]:
                            if potential_one[-1]!=morphism_val[-1]:
                                vals={
                                    "0": morphism_val,
                                    "1": potential_one
                                }
                                h=Morphism(vals)
                                if self.morphism_checker.check(h,k):
                                    return vals
            elif perm.cycle_structure=={k:1}:
                taus=self.potential_taus_str(perm,SIGMA_1)
                for tau in taus:
                    if tau in potential_vals["1"]:
                        potential_vals["1"][tau].append(morphism_val)
                    else:
                        potential_vals["1"][tau]=[morphism_val]

                for tau in taus:
                    if tau in potential_vals["0"]:
                        for potential_zero in potential_vals["0"][tau]:
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
    pansiot_coder=PansiotCoder()
    morphism_checker=MorphismChecker(pansiot_coder)
    repetition_checker=RepetitionChecker()
    pmg=PotentialMorphismGetter(morphism_checker,repetition_checker,pansiot_coder)
    
    from sympy.combinatorics import Permutation
    sigma_1=Permutation([3,0,1,2])
    # sigma_0=Permutation([2,3,1,0])
    sigma_0=Permutation([1,2,3,0])
    # sigma_1=Permutation([0,2,3,1])
    # sigma_0=Permutation([1,2,0,3])
    taus=pmg.potential_taus(sigma_1,sigma_0)

    print(sigma_0)

    for tau in taus:
        print(tau*sigma_1*(tau**-1))