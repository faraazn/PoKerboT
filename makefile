lint: discardodds.py
	-pylint --msg-template='{path}:{line}: {msg_id} {msg}' -r n discardodds.py
	-pep8 discardodds.py

run:
	python3 discardodds.py
