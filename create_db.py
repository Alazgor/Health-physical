import os
from pathlib import Path

# Path to dir instance
instance_dir = Path('C:/Users/aleks/CodeAcademy/health&physical/instance/')

# creating empty file db.sqlite, if they are not there
db_file = instance_dir / 'db.sqlite'
if not db_file.exists():
    try:
        db_file.touch()
        print(f"File '{db_file}' successfully created.")
    except Exception as e:
        print(f"didn't create file '{db_file}': {e}")
else:
    print(f"File '{db_file}' already existed.")
