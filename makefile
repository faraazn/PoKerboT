lint: handodds.py
	-pylint --msg-template='{path}:{line}: {msg_id} {msg}' -r n handodds.py
	-pep8 handodds.py

run:
	python3 handodds.py
