run:
	@echo "Warning: You're running a development server which is not fit"
	@echo "for production."
	python3 manage.py runserver 0.0.0.0:8000

prepare:
	python3 manage.py migrate

testdata:
	python3 manage.py loaddata dummy_data.json

help:
	@echo "The following make targets are available:"
	@echo "run      - Run the application (in the foreground) on port 8000"
	@echo "prepare  - Make preparations for run"
	@echo "testdata - Add test data to the database. Useful for development"
	@echo "help     - Print this help text"
	@echo "Run make --help for help on the make utility itself."
