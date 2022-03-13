# bkstem

### Compiles and hot-reloads for development
```
docker-compose up
```

### remove cache
```
docker builder prune
```

### Run your tests web
```
docker exec -it bkstem_web bash
npm run test
```

### Lints and fixes files web
```
docker exec -it bkstem_web bash
npm run lint
```

### Run your tests api
```
docker exec -it bkstem_api bash
pytest -v
```

### Lints and fixes files api
```
docker exec -it bkstem_api bash
black .
flake8 .
```

### Run tasks
```
docker exec -it bkstem_api bash
poetry install
poetry run task

Import variety:
poetry run task import jfd --table 'variety' --file 'variety.csv'
```# bkstem
# bkstrem
