# Note's API
# TODO WIP

# In order to run
## With remote debugging activated
```bash
docker-compose -f docker-compose.dev.yml build && docker-compose up
```
## Production mode
```bash
docker-compose build && docker-compose up
```

```bash
#ways to build and run
$ docker-compose build && docker-compose up -d
$ docker-compose up -d # detached
$ docker-compose up # attached
```

# Flask migrate/Alembic

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
```

# Pytest running locally
first run **poetry** **shell** from the project folder

```bash
# simple test
$ python -m pytest test/
```

```bash
# test with html report
$ python -m pytest  --html=reports/report.html --self-contained-html test/
```
# Run commands 

### create user
```bash
$ poetry shell
$ python -m flask user create
```

# Tips

    You can also use the **[flask db current]** command to check the current migration version of your database, and the **[flask db history]** command to view the history of all the migrations that were applied to your database.

    It's worth noting that, as a best practice, you should make sure that your migration scripts are tested and validated before deploying them to a production environment. Also, you should make sure to backup your production database before applying any migrations.
