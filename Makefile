
main: run

run:
	python3 run.py

runprod:
	sh run.sh

test:
	sh pytest


clean:
	rm -rf __pycache__

help: 
	# steps to build and run:
	@echo "apt install python3-venv libsasl2-dev python-dev libldap2-dev libssl-dev"
	@echo "cd access-system/"
	@echo "python3 -m venv venv"
	@echo "source venv/bin/activate"
	# Install requirements with pip
	@echo "pip install -r requirements.txt"
	# run
	@echo "make run"
	# to deactivate:
	@echo "venv/bin/activate"
	
	# try minimal bcrypt
