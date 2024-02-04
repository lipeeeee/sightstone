d:
		python3 driver.py
build:
		del dist
		del build
		pyinstaller build.spec
