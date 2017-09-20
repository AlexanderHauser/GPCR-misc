"""
Created in Jul 2016

@author: Alexander Hauser <alexshauser@gmail.com>

Compare signal sequences of different proteinclasses e.g.:

GPCRBinding: keyword:"Signal [KW-0732]" go:"G-protein coupled receptor binding [0001664]" AND reviewed:yes AND organism:"Homo sapiens (Human) [9606]"

receptorBinding: keyword:"Signal [KW-0732]" NOT go:"G-protein coupled receptor binding [0001664]" go:"receptor binding [0005102]" AND reviewed:yes AND organism:"Homo sapiens (Human) [9606]"
"""

import pandas as pd
from collections import OrderedDict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

GPCRBinding = pd.read_csv("/Users/vzw960/Downloads/GPCRBinding.txt", sep="\t")
receptorBinding = pd.read_csv("/Users/vzw960/Downloads/receptor_binding-noGPCR.txt", sep="\t") # No GPCR binding

GPCRBinding['SignalLength'] = GPCRBinding['Signal peptide'].str.split(' ').str[2]
GPCRBinding = GPCRBinding[GPCRBinding['SignalLength'] != '?']
GPCRBinding[['SignalLength']] = GPCRBinding[['SignalLength']].apply(pd.to_numeric)

receptorBinding['SignalLength'] = receptorBinding['Signal peptide'].str.split(' ').str[2]
receptorBinding[['SignalLength']] = receptorBinding[['SignalLength']].apply(pd.to_numeric)

for i in GPCRBinding.index:
    # do calc here
    sequence = GPCRBinding.ix[i]['Sequence']
    length = GPCRBinding.ix[i]['SignalLength']
    GPCRBinding.set_value(i,'SignalPepAA',sequence[0:length])

for i in receptorBinding.index:
    # do calc here
    sequence = receptorBinding.ix[i]['Sequence']
    length = receptorBinding.ix[i]['SignalLength']
    receptorBinding.set_value(i,'SignalPepAA',sequence[0:length])

def pandas_to_fasta(name, df):
    with open('/Users/vzw960/Downloads/'+name+".fasta", 'w') as filename:
        for i in df.index:
            sequence = df.ix[i]['SignalPepAA']
            filename.write(">"+df.ix[i]['Entry name']+"\n"+sequence+"\n")

def PCanalysis(data1, data2, set1, set2):
    
    from sklearn.decomposition import PCA
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn import preprocessing

    hydrophilicity = {"A": 0.07, "R": 2.88, "N": 3.22, "D": 3.64, "C": 0.71, "E": 3.08, "Q": 2.18, "G": 2.23, "H": 2.41, "I": -4.44, "L": -4.19, "K": 2.84, "M": -2.49, "F": -4.92, "P": -1.22, "S": 1.96, "T": 0.92, "W": -4.75, "Y": -1.39, "V": -2.69, "-": 0}
    steric_properties = {"A": -1.73, "R": 2.52, "N": 1.45, "D": 1.13, "C": -0.97, "E": 0.39, "Q": 0.53, "G": -5.36, "H": 1.74, "I": -1.68, "L": -1.03, "K": 1.41, "M": -0.27, "F": 1.30, "P": 0.88, "S": -1.63, "T": -2.09, "W": 3.65, "Y": 2.32, "V": -2.53, "-": 0}
    electronic_properties = {"A": 0.09, "R": -3.44, "N": 0.84, "D": 2.36, "C": 4.13, "E": -0.07, "Q": -1.14, "G": 0.30, "H": 1.11, "I": -1.03, "L": -0.98, "K": -3.14, "M": -0.41, "F": 0.45, "P": 2.23, "S": 0.57, "T": -1.40, "W": 0.85, "Y": 0.01, "V": -1.29, "-": 0}

    decriptors = [hydrophilicity, steric_properties, electronic_properties]

    for desc in decriptors:

        for AA in desc:
            data1 = data1.replace(AA, desc[AA])
            data2 = data2.replace(AA, desc[AA])

        Xdata1 = data1.values
        Xdata2 = data2.values

        target_names =  np.array(['Receptor-binding', 'GPCR-binding'])

        X = np.concatenate([Xdata1, Xdata2])
        y = np.concatenate([np.zeros(len(Xdata1)),np.ones(len(Xdata2))])

        # random assignment:
        # y = np.random.randint(low=0, high=3, size=(len(X),))

        # X = preprocessing.normalize(X, norm='l2')
        # Number of components to keep. if n_components is not set all components are kept:
        
        # So keep in mind to normalize your data sometimes.!!
        # http://www.bytefish.de/blog/pca_lda_with_gnu_octave/

        pca = PCA(n_components=len(data1.columns)) # n_components=len(Gi.columns)
        X_r = pca.fit(X).transform(X)

        # Percentage of variance explained for each components
        print('explained variance ratio: ', np.sum(pca.explained_variance_ratio_))

        sns.set_style("whitegrid")
        plt.figure()
        for c, i, target_name in zip("rkb", [0, 1], target_names):
            plt.scatter(X_r[y == i, 0], X_r[y == i, 1], c=c, label=target_name)
        plt.legend()
        plt.title('PCA of G protein alignments based on \n' + 'different z-scores')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.show()
    
    # Linear Discriminant Analysis (LDA) tries to identify attributes that account for the most variance between classes. In particular, LDA, in contrast to PCA, is a supervised method, using known class labels.

    lda = LinearDiscriminantAnalysis(n_components=len(data1.columns))
    X_r2 = lda.fit(X, y).transform(X)

    plt.figure()
    for c, i, target_name in zip("rkb", [0, 1], target_names):
        plt.scatter(X_r2[y == i, 0], X_r2[y == i, 1], c=c, label=target_name)
    plt.legend()
    plt.title('LDA of G protein alignments')
    plt.xlabel('PC1')
    plt.ylabel('PC2')

    plt.show()  

# pandas_to_fasta('receptorBinding', receptorBinding)
# pandas_to_fasta('GPCRBinding', GPCRBinding)

# make MSA with Jalview (Muscle default) 
# Load MSA.fasta into a dataframe
df = pd.read_csv("/Users/vzw960/Downloads/MSA.fasta", header=0, sep='\s+')
splitted = df['sequence'].apply(lambda x: pd.Series(list(x)))
splitted.columns = ['A'+str(x) for x in splitted.columns]
df = df.join(splitted)
df.drop(['sequence'], inplace=True, axis=1)
df.drop_duplicates(inplace=True)
df.index = df.index.str.split('/').str[0]


df1 = df[df.index.isin(list(receptorBinding['Entry name']))]
df2 = df[df.index.isin(list(GPCRBinding['Entry name']))]

PCanalysis(df1, df2, list(receptorBinding['Entry name']), list(GPCRBinding['Entry name']))

# =============
# ==== VIS ====
# =============
# plt.style.use('ggplot')
# fig = plt.figure(1, figsize=(9, 6))
# ax = fig.add_subplot(111)
# data_to_plot = [GPCRBinding['SignalLength'], receptorBinding['SignalLength']]
# ax.boxplot(data_to_plot)
# labels = ['GPCR-binding','Receptor-binding']
# ax.set_xticklabels(labels)
# ax.set_title("Signal Peptide length comparison")
# ax.set_ylim([10, 40])
# plt.show()