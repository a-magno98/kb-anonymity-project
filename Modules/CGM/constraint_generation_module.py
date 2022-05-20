from .CSM.constraint_solver_module import ConstraintSolverModule
from Utilities.utils import string_toValue, _log
from ast import literal_eval as make_tuple

#same path, no field repeat
def algorithm2(B):
    S = []
    #scan the tuples in B
    for t in B:
        #extract constraint variable k and value v
        for k, v in t.items():
            #result is a conjunctive set of constraints
            S += [(k, '!=', string_toValue(v))] 

    return S

#same path, no tuple repeat
def algorithm3(B, field_pt, qi):
    S = []
    #if the field is not specified, I take the first
    if field_pt is None:
        field_pt = qi[0] #age or eta
    
    #scan tuples and build a conjunctive set of constraints
    for t in B:
        S += [(field_pt, '!=', string_toValue(t[field_pt]))]

    return S

def algorithm4(B, b1, qi):
    S = []
    attributes = []

    #check if b1 contains generic values
    for k, v in b1.items():
        if('-' in v):
            #if contains generic values, save the attribute in a list
            attributes.append(k)

    #if the list is empty, b1 contains no generic values
    # invoke algorithm 3 
    if len(attributes) == 0:
        return algorithm3(B, None, qi)
    
    #scan tuples in B
    for t in B:
        for k, v in t.items():
            #if constraint varible k in attributes 
            #then build the conjunctive set of constraints
            if k in attributes:
                S += [(k, "!=", string_toValue(v))]
    
    #scan fields in b1
    for k,v in b1.items():
        #if constraint varible k not in attributes 
        # then build the conjunctive set of constraints
        if k not in attributes:
            S += [(k, "==", string_toValue(v))]
    
    return S

# convert the key-string into path (list of path conditions) 
def str2path_condition(s):
    return [make_tuple(t) for t in s.split('|')]

def ConstraintGenerationModule(A, alg, config_file, tf, qi):

    #result dataset
    R1 = []
    _log("[LOG]: Begin constraint generation ...")
    #for each value b1, pc, B in A
    for b1, pc, B in A:
        #based on parameter alg apply algorithm
        if alg == 'P-F':
            S = algorithm2(B) #same path, no field repeat

        elif alg == 'P-T':
            S = algorithm3(B, tf, qi) #same path, no tuple repeat

        elif alg == 'I-T':
            S = algorithm4(B, b1, qi) #same path and same input, no tuple repeat

        else:
            _log("[ERROR]: Invalid algorithm")
            continue

        # Conjunction of S and pc
        S += str2path_condition(pc)

        #call the constraint solver module on S and get its result row
        row = ConstraintSolverModule(S, config_file) # solve the constraints
        
        #if it is not None, add to the result dataset
        if row:
            _log("[LOG]: row added to the result dataset")
            R1 += [row]
    _log("[LOG]: Done constraint generation")
    #return the release dataset
    return R1
        
