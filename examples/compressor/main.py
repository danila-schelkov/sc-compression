import os

from sc_compression.signatures import Signatures
from sc_compression import compress

if not os.path.exists('in'):
	os.mkdir('in')
	
if not os.path.exists('out'):
	os.mkdir('out')


for filename in os.listdir('in'):
	with open('in/' + filename, 'rb') as f:
		filedata = f.read()
		f.close()
	with open('out/' + filename, 'wb') as f:
		f.write(
			compress(filedata, Signatures.SC, 1)
		)
		f.close()
