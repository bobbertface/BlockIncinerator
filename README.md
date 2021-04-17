# BlockIncinerator

Destroy all the Blocks!

## Setup steps in macOS

```bash
brew install pyenv
pyenv install 3.9.4
pyenv init
pyenv global 3.9.4
brew install pipx
pipx ensurepath
pipx install pipenv
pipenv install
pipenv shell
cd src
python BlockIncinerator.py
```

## Building win32 executable with PyInstaller (Only verified on Win 7 64-bit)

1. Get [pip for windows](http://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows)
1. From cmd prompt:

    ```bash
    python.exe -m pip install PyInstaller
    cd src
    python.exe -m PyInstaller BlockIncinerator.spec
    ```

1. If all goes well, it will create src/dist/BlockIncinerator.exe and you can
   launch it on other Windows machines without Python or the other listed
   dependencies installed.
