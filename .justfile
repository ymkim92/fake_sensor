run-test:
    pytest -svv 
run-test-filter TEST:
    pytest -svv tests/*{{TEST}}*
lint:
    ./linting.sh
mypy:
    ./mypy.sh
install-requirement:
    pip install -r requirements.txt
all:
    ./linting.sh && pytest -svv && ./mypy.sh 