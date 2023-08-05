import os as _os
import dotenv as _dotenv

_dirName = _os.getcwd()

for _ in range(5): 
    _dotenv_path = _os.path.join(_dirName, '.env')
    if (_os.path.isfile(_dotenv_path)): 
        break
    _dirName = _os.path.join(_dirName, '..')

def load_env():
    _dotenv.load_dotenv(_dotenv_path)

