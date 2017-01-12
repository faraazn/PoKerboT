lint: hands.py
	-pylint --msg-template='{path}:{line}: {msg_id} {msg}' -r n hands.py
	-pep8 hands.py

run:
	python3 hands.py
