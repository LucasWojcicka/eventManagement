# eventManagement

## How to initialise project

```
cd <<into project>>

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

## How to start project and initialise database

```
reflex db init
reflex db makemigrations
reflex db migrate
chmod +x ./eventManagement/seed.sh
./eventManagement/seed.sh
reflex run
```

NOTE: There is a known issue when `reflex run` incorrectly suggests to `makemigrations` again and again. 
The application is running and db is up to date. Issues will be addressed soon.

