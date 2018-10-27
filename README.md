# languages-similarity-analysis
Analysis of similarity between different languages (Introduction to Data Analysis class second assignment)

The script vectorize_documents.py is used to convert documents into their vector representations (relative triplet frequency). It allows the user to choose various parameters for the vectorizations. Edit the DOCS_PATH variable to choose a different path for docuemnts.

The dictionary resulting from the vectorization process is stored in triplets_dicts.npy.

The script k_medoids_clustering_analysis.py is used to perform the k-medoids clustering analysis. Various parameters of the analysis can be set by the user.

The script hierarchical_clustering_analysis is used to perform hierarchical clustering analysis of the documents.

The script language_inference allows user to get suggestions for languages of a document.