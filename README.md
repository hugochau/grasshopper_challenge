# Grasshopper coding challenge

Grasshopper Coding Challenge aims at giving the Senior Data Engineers candidates an idea about what kind of challenges would await while working at Grasshopper.

## Prerequisite

To be able to run this app, you must have [Docker](https://docs.docker.com/get-docker/) installed on your machine.

Set up the following environement variable:
- `$PGHOST`: postgresql host - the docker VM IP

Input data files are not included in the repository. Copy them into `data`.

NB: How to determine VM IP:
```bash
# solution 1
docker rum --rm --net host alpine ip address

# solution 2
docker-machine ip default
```


## Installation

Run the following commands under package root.

```bash
cd ./docker
docker-compose build
```

Please also move test data `l3_data_v3` to `./data`

## Structure

```bash
tree .

.
├── LICENSE
├── README.md
├── data
│   ├── blank
│   └── log
│       ├── blank
├── doc
│   └── requirements.pdf
├── docker
│   ├── docker-compose.yml
│   ├── postgres
│   │   ├── Dockerfile
│   │   └── init_db.sh
│   └── python
│       ├── Dockerfile
│       ├── requirements.txt
│       └── start.sh
└── src
    ├── config
    │   ├── constant.py
    │   └── schema.py
    ├── main.py
    ├── module
    │   ├── __init__.py
    │   ├── bbo.py
    │   ├── data.py
    │   ├── logger
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   ├── _formatter.py
    │   │   ├── adapter.py
    │   │   └── logger.py
    │   ├── postgres.py
    │   └── spark.py
    ├── test.py
    └── util
        └── util.py
```

## Usage

Run the following commands:

```bash
cd ./docker
# will create two microservices
# gh_python and gh_postgres
docker-compose up
```

For accessing gh_python in bash mode - useful for validating results:

```bash
docker-compose run --service-ports python bash

psql \
  -h $PGHOST \
  -d grasshopper \
  -U grasshopper \
  -p 5432

# sample queries
# count rows
select count(*) from l1_data

# list tables
\dt+
```

## Implementation

For the sake of simplicity and scalability, the code follows an object-oriented approach:
- classes are stored in the `src/module` folder
- utility functions in `src/util`
- constants and config files in `src/config`

`src/main.py` provides the main function.

From a high level perspective, the main function is implemented as follows:
  - define spark session
  - load data into spark DataFrame
  - replicate stream behavior
  - update bbo
  - push l1 data to csv/table

Logs are saved under `/tmp`. A logging decorator is defined in `util.log_item` and can be used throughout the code.


## Improvements

Further improvements to the code, listed below:

- Overall performance of the bbo module must be improved. It is a decent approach for an MVP but cannot be deployed to production as is.

- Streaming module is a POC. Due to time constraint, target folder only contains one CSV file. Besides, the input data comes in order. Suggested improvements with extra time:
  - support multiple files
  - add queueing system
  - deal with unordered

- Deal with corrupted records. Currently stored in separate column when loading CSV.

- Unit tests could be implemented in place of `test.py`.

- The logging module is not yet used at its full capacity. Suggested improvements:
  - Capture `pyspark` stdout output
  - Enrich log record with additional attributes
  - Add `logging.info` messages throughout the code, if need be.
  - Decorate other methods

## License
This product is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.

## Contact

Please reach out to chauvary.hugo@gmail.com

# Thank you!
