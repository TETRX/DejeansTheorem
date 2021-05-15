from ..utils.pansiot_coder import PansiotCoder
from ..main.morphism_checker import MorphismChecker
from ..utils.repetition_checker import RepetitionChecker
from ..main.potential_morphism_getter import PotentialMorphismGetter


if __name__=="__main__":
    from datetime import datetime
    start=datetime.now()
    pansiot_coder=PansiotCoder()
    morphism_checker=MorphismChecker(pansiot_coder)
    repetition_checker=RepetitionChecker()
    pmg=PotentialMorphismGetter(morphism_checker,repetition_checker,pansiot_coder)
    import json
    print(json.dumps(pmg.get(14)))
    print(datetime.now()-start)