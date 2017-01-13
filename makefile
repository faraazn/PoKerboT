lint: preflop.py
	-pylint --msg-template='{path}:{line}: {msg_id} {msg}' -r n preflop.py
	-pep8 preflop.py

run:
	python3 preflop.py
