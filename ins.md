# Create an isolated test environment
py -3.14 -m venv .testvenv

# Install the actual distribution
.\.testvenv\Scripts\python.exe -m pip install `
    .\dist\etherlyzer-0.3.0-py3-none-any.whl


.\.testvenv\Scripts\etherlyzer.exe --help
