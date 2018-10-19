import numpy as np
from pathlib import Path
from lib_naloga2 import language_inferer

########################
# Author: Jernej Vivod #
########################

# This script provides the human to computer interface for language inference functionality.

# Load reference documents dictionary and dictionary for decoding OHCHR language codes.
references_dicts = np.load('triplets_dicts.npy').item()
decode_OHCHR = np.load('OHCHR_decode.npy').item()


if __name__ == "__main__":
	# Prompt user for document name. Keep prompting until entered document name is valid.
	while True:
		document_name = input('Enter name of document to analyze: ')
		document_full_path = Path("./data/language_analysis_data/" + document_name)

		# Check if document exists.
		if document_full_path.is_file():
			# Create new instance of LanguageAnalyzer class and run analysis.
			la = language_inferer.LanguageAnalyzer(references_dicts, decode_OHCHR)
			la.run(3, document_name)
			break;
		else:
			print('\ndocument \'{0}\' not found. Make sure the document is located in ./data/language_analysis_data folder.\n'.format(document_name))
else:
	def infer_language(document_full_path):
		document_full_path = Path(document_full_path)
		# Create new instance of LanguageAnalyzer class and run analysis.
		la = language_inferer.LanguageAnalyzer(references_dicts, decode_OHCHR)
		la.run(3, document_name)