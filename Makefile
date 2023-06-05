develop: setup-git
	pip install "file://`pwd`#egg=freckle_client[dev]"
	pip install -e .
	pip install -r requirements-dev.txt

setup-git:
	git config branch.autosetuprebase always
	cd .git/hooks && ln -sf ../../hooks/* ./

lint-python:
	@echo "Linting Python files"
	pre-commit run --all-files
	@echo ""
