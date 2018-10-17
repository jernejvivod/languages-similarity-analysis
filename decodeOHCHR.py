import numpy as np

# dictionaty that maps OHCHR language codes to language names in English
res = {
	'afk' : 'Afrikaans',
	'cln' : 'Catalan-Valencian-Balear',
	'czc' : 'Czech',
	'dns' : 'Danish',
	'dut' : 'Dutch',
	'eng' : 'English',
	'frn' : 'French',
	'ger' : 'German',
	'gln' : 'Galician',
	'grk' : 'Greek',
	'ice' : 'Icelandic',
	'itn' : 'Italian',
	'jpn' : 'Japanese',
	'mkj' : 'Macedonian',
	'nrn' : 'Norwegian, Nynorsk',
	'por' : 'Portuguese',
	'pql' : 'Polish',
	'rum' : 'Romanian',
	'rus' : 'Russian',
	'slo' : 'Slovak',
	'slv' : 'Slovenian',
	'spn' : 'Spanish',
	'src1' : 'Bosnian (Latin)',
	'src3' : 'Serbian (Latin)',
	'swd' : 'Swedish',
	'trk' : 'Turkish',
	'ukr' : 'Ukrainian'
}

# Save dictionary to file.
np.save('OHCHR_decode.npy', res)