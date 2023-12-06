DOCKER_TAG=lcharles060/access-system:0.1
main: help

run:
	python3 run.py 234234

runprod:
	python3 run.py

gunicorn:
	gunicorn -w 4 -b 0.0.0.0:5000 "run:create_app(development=False)"

all_tests: 
	python3 -m unittest discover -s test

#t: integration_test.py system_usecases_test.py  unit_test.py
t: unit_test.py

integration_test.py:
	python3 -m unittest web_server/test/$@

system_usecases_test.py:
	python3 -m unittest web_server/test/$@

unit_test.py:
	python3 -m unittest web_server/test/$@

dedit:
	nano Dockerfile

dbuild:
	docker build . --tag $(DOCKER_TAG)

drun:
	docker run -p 5000:5000 -it $(DOCKER_TAG)

# do docker login on a repository to push
dpush:
	docker push $(DOCKER_TAG)

clean:
	rm -rf __pycache__ /tmp/foo.db database/database.sqlite 

help: 
	# steps to build and run:
	@echo "apt install python3-venv libsasl2-dev python-dev libldap2-dev libssl-dev"
	@echo "cd access-system/"
	@echo "python3 -m venv venv"
	@echo "source venv/bin/activate"
	# Install requirements with pip
	@echo "pip install --upgrade pip"
	@echo "pip install -r requirements.txt"
	# run
	@echo "make run"
	# to deactivate:
	@echo "venv/bin/activate"
	
	# try minimal bcrypt
