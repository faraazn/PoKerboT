lint: PoKerboT.py
	-pylint --msg-template='{path}:{line}: {msg_id} {msg}' -r n PoKerboT.py
	-pep8 PoKerboT.py

run:
	python3 PoKerboT.py
