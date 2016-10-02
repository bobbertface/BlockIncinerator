BlockIncinerator
================

Destroy all the Blocks!

#####
# Dependencies to run BlockIncinerator.py
#####
* Python 3.3
* Pygame 1.9.2
* NumPy 1.7 RC 1

#####
# Building win32 executable with PyInstaller (Only verified on Win 7 64-bit)
#####
1. Get pip (http://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows)
2. From cmd prompt
	python.exe -m pip install PyInstaller
	cd <location of BlockIncinerator>/src
	python.exe -m PyInstaller BlockIncinerator.spec
3. If all goes well, it will create src/dist/BlockIncinerator.exe and you can launch it on other Windows machines without Python or the other listed dependencies installed.