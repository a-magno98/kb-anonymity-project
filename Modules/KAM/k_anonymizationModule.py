import pandas as pd
import numpy as np
from Utilities.utils import string_toValue, value_toString, _log

def suppression_tuple(df, df_check, age_eta, sex_gen):
    #delete the row present in df_check from the dataset df
    df = df[(df[age_eta+'_group'] != df_check[age_eta+'_group'][0]) & (df[sex_gen] != df_check[sex_gen][0])]

def check_is_anonymized(df, k, age_eta, sex_gen):
    #calculate how many unique combination are for age and sex
    df_check = df.groupby([age_eta+'_group', sex_gen]).size().reset_index(name='Count')

    #filter the rows that have count less than k
    df_check = df_check[df_check['Count'] < k]
    df_check = df_check.reset_index()

    #if it is empty, anonymization is reached
    if df_check.empty:
        return True

    if(len(df_check) == 1):
        suppression_tuple(df, df_check, age_eta, sex_gen)
        return True
    
    return False

def get_generalization(level):
    bins = []
    labels = []
    if(level == 1):
        bins = [0,10,20,30,40,50,60,70,80,90,100]
        labels = ['0-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100']
    if(level == 2):
        bins = [0,20,40,60,80,100]
        labels = ['0-20','20-40','40-60','60-80','80-100']
    if(level == 3):
        bins = [0,50,100]
        labels = ['0-50','50-100']
    return bins, labels
        

#approach AG_TS, attribute generalization and tuple suppression
def anonymize(B, qi, pc, k, op):
    #result
    anonymized = []
    #take the columns from dictionary
    columns = B[0].index
    #select quasi-identifiers from lists
    age_eta = qi[0]
    sex_gen = qi[1]

    #create new dataframe from B
    df = pd.DataFrame(columns=columns)
    for row in B:
        df = df.append([row])
    
    #convert strings age/eta in actual value -> integer
    df[age_eta] = [string_toValue(age) for age in df[age_eta]]
    #aux column for generalization
    df[age_eta+'_group'] = df[age_eta].copy()

    #k-anonymization
    level = 1
    while(level < 5):
        #if bucket anonymized exit, otherwise continue
        if check_is_anonymized(df, k, age_eta, sex_gen):
            _log("[LOG]: bucket k-anonymized!")
            if level == 1:
                del df[age_eta+'_group']
            else:
                df[age_eta] = df[age_eta+'_group']
                del df[age_eta+'_group']
            break
        elif (level == 4):
            #Not able to anonymized the bucket
            if len(df) < k:
                _log("[LOG]: bucket not anonymized, bucket of dataset less than k")
            del df[age_eta+'_group']
            break
        
        #get bins and labels 
        bins, labels = get_generalization(level)
        #generalization
        df[age_eta+'_group'] = pd.cut(df[age_eta], bins=bins, labels=labels)
        level+=1
    
    #convert values to string
    df[age_eta] = [value_toString(age) for age in df[age_eta]]

    for i, b in df.iterrows():
        #if it I-T, check b
        if op:
            if len(b)<=1:
                _log("Error:unsatisfiable case")
                continue
        #construct the result tuple b, pc, B
        anonymized.append((b, pc, B))
    return anonymized

def k_AnonymizationModule(PCBuckets, qi, k, alg):
    #holding intermediate k-anonymized dataset
    A = []
    #flag to check alg I-T 
    is_I_T = True if alg == 'I-T' else False

    _log("[LOG]: Begin of anonymization ...")
    #parse PCBuckets and construct the anonymized dataset
    for pc, B in PCBuckets.items():
        pc_anonym = anonymize(B, qi, pc, k, is_I_T)
        A.extend(pc_anonym)
    
    return A