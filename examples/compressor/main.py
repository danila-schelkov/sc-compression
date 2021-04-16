import os

from sc_compression.compressor import Compressor
from sc_compression.signatures import Signatures

if not os.path.exists('in'):
	os.mkdir('in')
	
if not os.path.exists('out'):
	os.mkdir('out')


compressor = Compressor()
for filename in os.listdir('in'):
	with open('in/' + filename, 'rb') as f:
		filedata = f.read()
		f.close()
	with open('out/' + filename, 'wb') as f:
		f.write(
			compressor.compress(filedata, Signatures.SCLZ)
		)
		f.close()