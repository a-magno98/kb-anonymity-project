from msilib.schema import Error
import pandas as pd
import argparse
from datetime import datetime
import csv
from Utilities.utils import _log

import Modules.PEM.program_execution_module as pem
import Modules.KAM.k_anonymizationModule as kam
import Modules.CGM.constraint_generation_module as cgm

#read dataset from specified file
def read_dataset(file):
    rows = []
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            rows.append(row)
    return rows


def kb_anonymity(R, qi, k, alg, n_d, config_file, tf):
    """
    The algorithm of kb-anonymity, that apply the 3 steps to do it:
    1. Program execution module
    2. k-Anonymization module
    3. Constraint generation module

    :param R: Dataset in pandas
    :param quasi_identifiers: List of names of quasi-identifiers
    :param k: Level of anonymization
    :param alg: Configuration algorithm (PF,PT,IT) in constraint generation module
    :param n_d: Name dataset (heart or infortuni)
    :param tf: Tuple field for PT algorithm
    """ 

    #PCBuckets groups tuples based on path conditions
    PCBuckets = pem.ProgramExecutionModule(R, k, n_d)
    #k-Anonymization of buckets
    A = kam.k_AnonymizationModule(PCBuckets, qi, k, alg)

    #call constrain generation module with previous result A, the algorithm alg, the config file
    # which contain the constraints, tf(tuple field) for PT algorithm, qi (quasi identifiers)
    R1 = cgm.ConstraintGenerationModule(A, alg, config_file, tf, qi)

    #return the result as a pandas DataFrame
    return pd.DataFrame(R1)
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Implementation of K-B Anonimity algorithm")
    parser.add_argument( '--input_file','-i', help='path to the CSV dataset', required=True)
    parser.add_argument('--algorithm','-a', help='choose one between P-F, P-T, I-T', required=True) 
    parser.add_argument('--k_value','-k', help='degree of anonimity', type=int, required=True)
    parser.add_argument('--data_constraints','-dc', required=True,
                        type=str, help="Path to the data constraints that contains constraints of data for the solver.")
    parser.add_argument('--tuple_field','-tf', nargs='+', default=None,
                        type=str, help="Field used to have the no tuple repeat (only used with P-T option).")
    parser.add_argument('--output_file','-o', help='path to the output file with csv extention', required=True)
    
    args = parser.parse_args()

    try:
        if args.tuple_field != None and args.algorithm != 'P-T':
            _log("[ERROR]: Tuple field needed only with P-T algorithm")
            raise Error
        
        start = datetime.now()

        #initialize empty quasi identifiers for k-anonymity part
        quasi_identifiers = []
        
        #used for selecting the subject program 
        name_dataset = ""

        if ("heart" in args.input_file):
            #select the quasi identifiers for dataset heart
            quasi_identifiers = ["age", "sex"]
            name_dataset = "heart"

        elif ("infortuni" in args.input_file):
            #select the quasi identifiers for dataset inforutni Liguria
            quasi_identifiers = ["Eta", "Genere"]
            name_dataset = "infortuni"        
        
        #read dataset
        dataset = read_dataset(args.input_file)

        #name of the columns
        columns = dataset[0]

        #delete them from the dataset
        del dataset[0]

        #convert the dataset to a pandas dataframe
        df = pd.DataFrame(dataset, columns = columns)

        #remove duplicates which are useless
        df = df.drop_duplicates()

        #convert the dataframe to a dictionary
        R = df.to_dict('records')

        #call kb_anonymity algorithm
        R1 = kb_anonymity(df, quasi_identifiers, args.k_value, args.algorithm, name_dataset, args.data_constraints, args.tuple_field)
        
        #for debug
        R1.drop_duplicates()

        #save the output as csv file
        R1.to_csv(args.output_file, index = False)
        _log("[LOG]: Result dataset saved in csv file")

        end = (datetime.now() - start).total_seconds()
        print('{*} Overall Execution Time, done in %.2f seconds (%.3f minutes (%.2f hours))\t\t--\t' % (end, end / 60, end / 60 / 60))

    except FileNotFoundError as error:
        _log("[ERROR]: File '%s' has not been found." % error.filename,
                    endl=True, enabled=True)
    except IOError as error:
        _log("[ERROR]: There has been an error with reading file '%s'." % error.filename,
                    endl=True, enabled=True)