# api

## Project setup
```
poetry install
```

### Compiles and hot-reloads for development
```
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### Lints and fixes files
```
flake8 .
black .
```