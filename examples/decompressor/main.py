import os

from sc_compression.compression import Decompressor

if not os.path.exists('in'):
	os.mkdir('in')
	
if not os.path.exists('out'):
	os.mkdir('out')


decompressor = Decompressor()
for filename in os.listdir('in'):
	with open('in/' + filename, 'rb') as f:
		filedata = f.read()
		f.close()
	with open('out/' + filename, 'wb') as f:
		f.write(
			decompressor.decompress(filedata)
		)
		f.close()
