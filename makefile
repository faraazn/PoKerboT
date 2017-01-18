lint: discard.py
	-pylint --msg-template='{path}:{line}: {msg_id} {msg}' -r n discard.py
	-pep8 discard.py

run:
	python3 discard.py
