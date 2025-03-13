# manus-sandbox-code-decrypted
Decrypted Manus Sandbox Code

## What is done?

### Unpack Pyarmor v9

Follow instructions from [Pyarmor-Tooling](https://github.com/GDATAAdvancedAnalytics/Pyarmor-Tooling):

- Use IDA to find the key for Pyarmor 009055
- Decrypt the py code to marshal file

Additional steps:

- Rebuild marshal file
- Remove all dark piles inserted by Pyarmor

## Decompile pyc (not done yet)

- Use [Decompyle++](https://github.com/zrax/pycdc) to decompile pyc

### Decompile

## Running pre-compiled version

### Clone project

```sh
git clone https://github.com/vonjackustc/manus-sandbox-code-decrypted
cd manus-sandbox-code-decrypted
```

### Prepare virtual environment

```sh
python3.11 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Patch dotenv

```sh
sed -e 's/usecwd: bool = False/usecwd: bool = True/g' venv/lib/python3.11/site-packages/dotenv/main.py > venv/lib/python3.11/site-packages/dotenv/main.py
```

### Start server

```sh
cd sandbox-runtime-compiled
PYTHONPATH=. python start_server.pyc
```
