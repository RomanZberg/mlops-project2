# MLOPS Project 2 Containerization 
## System requirements
For being able to use the contents of this repository, the following requirements must be fulfilled.
- [Docker]( https://www.docker.com/) and [docker compose](https://docs.docker.com/compose/install/) is installed on your system
- macOS (only tested on macOS, most likely also works for linux)



## Steps after cloning the repository
```bash
cd <project-root>
```
**Note:** replace <project-root> with the path to the project root
```bash
docker-compose build
```


### Setting Weights & Biases api key (optional)
When you execute the training command, you will be prompted for your wandb api key at some point. To allways use the same api key complete the following steps.
```bash
cp .env_template .env
```

Open the file .env and set the value for the variable **WANDB_API_KEY**. You can get that key by visiting [https://wandb.ai/authorize](https://wandb.ai/authorize).


## How to run training?

### Best current found hyperparameter settings
```bash
docker-compose run --rm train-model
```
### List possible configurable hyperparameters 

```bash
docker-compose run --rm -e args='-h' train-model
```

### Run training run with custom defined hyperparameters

```bash
docker-compose run --rm -e args='--model.weight_decay 0.04 --model.learning_rate 0.001 --data.train_batch_size 32 --seed-everything 42' train-model
```
**Attention:** Don't forget to pass the ```--seed-everything 42``` option, tho ensure to always use the same random seed.

**Note:** You can pass any configuration option listed, when executing the command described in the section "List possible configurable hyperparameters"  

## How can I enter the development environment?
```bash
docker-compose run --rm dev-environment
```

**Note:** If you have installed new dependency's with ```poetry install <package-name>``` and exit the container afterwards, you have either to rebuild the image using ```docker-compose build``` or run the above command and run ```poetry install```