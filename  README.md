## Executing
### install
- create virtual env
  - linux
  ```
  cd /path/to/project
   python -m venv venv
   ```
  - windows
  ```
  cd c:\path\to\project
  c:\>python -m venv venv 
   ```
  
- activate virtual env
-  - linux
  ```
   source venv/bin/activate
   ```
  - windows
  ```
# In cmd.exe
venv\Scripts\activate.bat
# In PowerShell
venv\Scripts\Activate.ps1
  ```
- install dependencies 

  ```pip install -r requirements.txt```


### Running
#### Running mode
You can set the application to either test or production mode by editing `settings.py
```
PRODUCTION_MODE = True
```

#### run the application
from the main  directory run
```
uvicorn main:app --reload
```

### Testing
`pytest` is used for testing:
```
pytest tests  -s
```
You can pass additional arguments to `pytest` for more detailed output, HTML reports, etc.

## Simplifications and improvements
- Currently, an in-memory database is used. Consider switching to SQLite or another RDBMS for persistence.
- Convert functions in utils.py into decorators where appropriate.
- Address Pydantic warnings by adjusting some settings.
- Review and possibly adjust HTTP methods (POST vs. GET) for some endpoints.
- Add more Pydantic validations for stricter data integrity