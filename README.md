# MLOPS Project 2 Containerization 
## System requirements
For being able to use the contents of this repository, the following requirements must be fulfilled.
- [Docker]( https://www.docker.com/) and [docker compose](https://docs.docker.com/compose/install/) is installed on your system
- Operating system: macOS (intel) or linux (only tested on macOS and linux, most likely also works for windows, although some commands appearing in the readme might have to be adjusted )
- 26 GB free memory space (for build docker images)

**Note:** When the command ```docker-compose``` is not available on your system, try ```docker compose```, as this is the newer version but the commands in this readme should work the same. 


## Steps after cloning the repository
```bash
cd <project-root>
```
**Note:** replace <project-root> with the path to the project root
```bash
docker-compose build
```


### Setting Weights & Biases api key (required if you use docker-compose to run images)
When you execute the training image with ```docker run```, you will be prompted for your wandb api key at some point. When using ```docker-compose run``` to run the training image, it will use the api key specified in the ```.env``` file in your project root. Execute the following steps:
```bash
cp .env_template .env
```

Open the file ```.env``` and set the value for the variable **WANDB_API_KEY**. You can get that key by visiting [https://wandb.ai/authorize](https://wandb.ai/authorize).

**Attention !!!!:** Never, **never** put your wandb api key into the file ```.env_template```, as it will result in pushing your wandb api key to this GitHub repository, if you were to commit and push something.


## docker-compose run vs. docker run
After the images were build, there are two ways to run them. The differences and why you might want to use either of them is described below.
In the following sections, both ways of running the available commands, when sensible, will be described.
### docker-compose run 
When using this method, your current project folder will be mounted into the docker container on runtime, this has the benefit that you will not have to rebuild the docker image each time, you change something in the sourcecode of the model.
### docker run 
When using this method, the executed source code corresponds to the version, when the last time docker-compose build was executed. 


## How to run training?

### Run training run with the best current found hyperparameter settings
#### docker-compose run
```bash
docker-compose run --rm train-model
```

#### docker run
```bash
docker run -it mlops-project-2-train-model
```

If you don't want to be prompted for your wandb api key, you can pass your wandb api key like the following:
```bash
docker run -it -e WANDB_API_KEY=<api-key> mlops-project-2-train-model
```
**Note:** replace ```<api-key>``` with the key you get, by visiting [https://wandb.ai/authorize](https://wandb.ai/authorize)


### Run training run with the best current found hyperparameter settings with added arguments
#### docker-compose run
```bash
docker-compose run --rm -e addArgs='--wandb-run-name-prefix my-run-prefix' train-model
```

#### docker run
```bash
docker run -ite addArgs='--wandb-run-name-prefix my-run-prefix' mlops-project-2-train-model
```

**Some example arguments, which are typically used that way:**
- ```--wandb-project```: Name of the wandb project, to which the training is logged to 
- ```--wandb-entity```: Name of the wandb entity, to which the training is logged to
- ```--wandb-run-name-prefix```: Prefix added to a wandb run name

If you don't want to be prompted for your wandb api key, you can pass your wandb api key like the following:
```bash
docker run -ite addArgs='--wandb-run-name-prefix my-run-prefix' -e WANDB_API_KEY=<api-key> mlops-project-2-train-model
```
**Note:** replace ```<api-key>``` with the key you get, by visiting [https://wandb.ai/authorize](https://wandb.ai/authorize)


### List possible configurable hyperparameters 
#### docker-compose run
```bash
docker-compose run --rm -e args='-h' train-model
```

#### docker run
```bash
docker run -ite args='-h' mlops-project-2-train-model
```

### Run training run with custom defined hyperparameters
#### docker-compose run
```bash
docker-compose run --rm -e args='--model.weight_decay 0.04 --model.learning_rate 0.001 --data.train_batch_size 32 --seed_everything 42' train-model
```

#### docker run
```bash
docker run -ite args='--model.weight_decay 0.04 --model.learning_rate 0.001 --data.train_batch_size 32 --seed_everything 42' mlops-project-2-train-model
```

**Attention:** Don't forget to pass the ```--seed_everything 42``` option, tho ensure to always use the same random seed.

**Note:** You can pass any configuration option listed, when executing the command described in the section "List possible configurable hyperparameters"  

## How can I enter the development environment?
```bash
docker-compose run --rm dev-environment
```

**Note:** If you have installed new dependency's with ```poetry install <package-name>``` and exit the container afterwards, you have either to rebuild the image using ```docker-compose build``` or run the above command and run ```poetry install```