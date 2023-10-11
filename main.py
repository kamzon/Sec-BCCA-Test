import numpy as np
from BCCA import BiCorrelationClusteringAlgorithm
from data_processing import load_yeast_tavazoie
from SecBic_BCCA import SecuredBiCorrelationClusteringAlgorithm
from data_processing import synthetic
import time

# load yeast data used in the original Cheng and Church's paper
data = load_yeast_tavazoie().values

# missing value imputation suggested by Cheng and Church
missing = np.where(data < 0.0)
data[missing] = np.random.randint(low=0, high=800, size=len(missing[0]))


# Set the size of the dataset
num_genes = 10  # Number of genes
num_conditions = 10 # Number of conditions


# Generate the synthetic yeast-like dataset
dataset = np.random.randint(1, 800, size=(num_genes, num_conditions))


# Generate the synthetic dataset based on six bicluster models including constant, scale, shift, shift_scale and plaid

Syn_dataset, exp  = synthetic.make_const_data(100, 75, 3)
Syn_dataset, exp  = synthetic.make_plaid_data(100, 75, 3)
Syn_dataset, exp  = synthetic.make_scale_data(100, 75, 3)
Syn_dataset, exp  = synthetic.make_shift_data(100, 75, 3)
Syn_dataset, exp  = synthetic.make_shift_scale_data(100, 75, 3)

# Print the dataset shape
print("Dataset shape:", Syn_dataset.shape)
print(dataset)

with open('resSecBicBCCA_test_dataset6.txt', 'a') as saveFile:
    for nbr_cols in range(3, 10):
        t0 = time.perf_counter()
        print("normal BCCA, min_clos: ", nbr_cols)
        bcca = BiCorrelationClusteringAlgorithm(correlation_threshold=0.9, min_cols=nbr_cols)
        normal_biclusters = bcca.run(dataset)
        t1 = time.perf_counter()
        print("Time Performance in Calculating Normal BCCA: ", round(t1 - t0, 5), "Seconds \n\n")

        print("Secure BCCA, min_cols: ", nbr_cols)
        sec_bcca = SecuredBiCorrelationClusteringAlgorithm(correlation_threshold=0.9, min_cols=nbr_cols, data=dataset)
        sec_biclusters = sec_bcca.run()
        t2 = time.perf_counter()
        print("Time Performance in Calculating Homomorphically: ", round(t2 - t1, 5), "Seconds \n\n")

        saveFile.write("Normal BCCA with min_cols: " + str(nbr_cols))
        saveFile.write("\n\n")
        saveFile.write("Time Performance in Calculating Normal BCCA: " + str(round(t1 - t0, 5)))
        saveFile.write("\n\n")
        saveFile.write(normal_biclusters.__str__())
        saveFile.write("\n\n Secure BCCA with min_cols: " + str(nbr_cols))
        saveFile.write("\nTime Performance in Calculating Homomorphically: " + str(round(t2 - t1, 5)))
        saveFile.write("\n\n")
        saveFile.write(sec_biclusters.__str__())
        saveFile.write("\n")

