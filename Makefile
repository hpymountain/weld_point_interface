.PHONY: clean virtualenv proto test fmt docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf coverage-report
	rm -rf html
	rm -rf tmp

virtualenv:
	virtualenv -q --prompt '> wp-interface <' .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo
	@echo "VirtualENV Setup Complete. Now run: source .venv/bin/activate"
	@echo

doc:
	rm -rf html
	pdoc3 --html wp-interface tests
	open http://localhost:9999
	pdoc3 --html --http localhost:9999 wp-interface tests

# check for log-level and enable print statement outputs on debug
ifdef debug
allow_print=-s
log_level=--log-cli-level=$(debug)0
else
allow_print=
log_level=
endif

# check for test with coverage reports
ifdef cov
cov_report=--cov=singer --cov-report=term --cov-report=html:coverage-report
else
cov_report=
endif

# limit the tests to run by files and tests filters
# make test files=test_logging.py tests=logging debug=1
test:
	rm -rf tmp/tests
	mkdir -p tmp/tests
	python -m pytest \
		-v \
		$(allow_print) \
		$(cov_report) \
		--basetemp=tmp/tests \
		$(log_level) \
		-k "$(tests)" \
		tests/$(files)

fmt:
	# align with https://google.github.io/styleguide/pyguide.html
	pyink --pyink-use-majority-quotes --line-length 115 --include "\.py$"" --exclude "\/__pycache__\/" wp-interface tests docs setup.py

sdist: clean
	rm -rf dist/*
	python setup.py sdist

wheel: clean
	rm -rf dist/*
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
