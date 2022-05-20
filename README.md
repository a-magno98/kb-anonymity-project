# kb-anonymity project
I have developed the project of kb-anonymity, which has been realized by the paper "kb-anonymity: A model for anonymized behavior-preserving test and debugging data." The project has been built using the tool VisualStudioCode with language Python 3.8.10 and library z3py for concerning the solver. 

The project is organized in the following files and modules:

- **Dataset**: contains all the files of example on which perform the tests and configuration files containing the constraints;
- **Modules**: contains all the scripts of the four modules of the algorithm, plus the subject programs;
- **Stats**: contains a program for plotting the graphs comparing the execution times of different algorithms;
- **Utilities**: has auxiliaries functions;
- **main.py**: principal script for starting the program

In the file of data constraints the user specify the range constraints for each field of a tuple. The first row must contain all the fields present in the dataset as strings. Then each row must follow this syntax: 

if the constraints are related to a single field:
```
field:(([op_symbol value]+),?)+
```
otherwise, if the constraints involve two related fields:
```
#field1 op_symbol field2
```
The *comma* symbol separates the conditions to be put in OR, while the *whitespaces* are for conditions in AND.

## Parameters in input

For running the project, we have just to execute the script main.py using a series of parameters:
- `-i` | `--input`: path to csv file on which apply the kb-anonymity (required)
- `a` | `--algorithm`: configuration option, the value can just be P-F(same path, no field repeat), P-T(same path, no tuple repeat), I-T (same path and same input, no tuple repeat) (required)
- `k` | `--k_value`: value k of anonymization (required)
- `dc` | `--data_constraints`: path to the file containing all the constraints of domain of the attributes (required)
- `tf` | `--tuple_fields`: attributes used to do not have repetition of tuples, using only for alg P-T. If it is not setted, take in input the attribute age/eta (optional)
- `o` | `--output`: path to the file of output in csv(required)

## Example of commands
Using dataset of heart disease:
```sh
python main.py -i 'Dataset/heart.csv' -a "P-F" -k 2 -dc 'Dataset/data_constraints_heart.txt' -o 'Dataset/heart_release.csv'
```

Using dataset of inail of Liguria regarding accidents at work:
```sh
python main.py -i 'Dataset/infortuni_Liguria_2000.csv' -a "I-T" -k 3 -dc 'Dataset/data_constraints_infortuni.txt' -o 'Dataset/infortuni_Liguria_2000_release.csv'
```

