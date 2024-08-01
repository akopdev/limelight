# Limelight
This is the first prototype of a search engine with the code name **limelight**. Most likely, you won't find anything useful here.

This project aims to create a proof of concept (POC) of the semantic search engine with Q&A capabilities that can be completely 
autonomous and run on low-end hardware, like Raspberry Pi. 

The code, as well as the documentation, are still in the early stages of development, and far from being anything close to production-ready.

## Installation

First, you will need to install [ollama](https://ollama.com), and manually start the service. 
Then, you can install the application virtual environment with it's dependencies by executing the following command:

```shell
make init install
```

## Testing

To run unit tests, execute the following command:

```shell
make test
```

To perform a manual testing, you need to import dataset first. To do so, execute the following command:

```shell
make dataset
```
It will download the dataset based on English wikipedia articles and import it into the persistent database.
Depending on the machine, it may take a while.
