.PHONY: requirements

requirements:
	poetry lock && poetry export --without-hashes -f requirements.txt -o requirements.txt