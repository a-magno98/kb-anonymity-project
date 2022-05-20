import time

from pandas import DataFrame
from Modules.PEM.subject_program_heart import exec_pc_heart
from Modules.PEM.subject_program_infortuni import exec_pc_infortuni
from Utilities.utils import string_toValue,_log

#for each row convert strings to value (integer)
def convertValues(row):
    for i in range(0, len(row)):
        row[i] = string_toValue(row[i])
    return row

#convert path constraints to string 
def pc_toString(lst):
    return '|'.join([str(i) for i in lst])

def ProgramExecutionModule(R: DataFrame, k, name_dataset):
    PCBuckets = dict()
    _log("[LOG]: Begin the collection of path constraints ...")
    #parse the pandas DataFrame per row
    for i, t in R.iterrows():
        #convert string to values 
        row_copy = t.copy()
        t_aux = convertValues(row_copy)

        #execute subject_program with t_aux and collect the path condition pc
        if name_dataset == "heart":
            pc = exec_pc_heart(t_aux)
        elif name_dataset == "infortuni":
            pc = exec_pc_infortuni(t_aux)
        
        #convert path constraint to strings
        pc = pc_toString(pc)
        
        if pc not in PCBuckets.keys():
            PCBuckets.setdefault(pc, [])

        #build dict PCBuckets with pc(dict):t(pandas.series)
        PCBuckets[pc] += [t]
    
    _log("[LOG]: Done, path constraints collected")
    #delete all PCBuckets with number of elements minor of k
    del_pc = [pc for pc, B in PCBuckets.items() if len(B) < k]
    for elem in del_pc:
        del PCBuckets[elem]

    return PCBuckets
    

          

        
        