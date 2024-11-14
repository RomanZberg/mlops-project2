FROM python:3.11-slim AS development
ENV PATH="${PATH}:/root/.local/bin"

RUN apt-get update &&\
apt-get -y install pipx &&\
pipx ensurepath &&\
pipx install poetry

# copying only the dependency files seperatly and installing dependencys, enables caching of this step if dependency tracking files did not change
COPY poetry.lock /pytorch-project/poetry.lock
COPY pyproject.toml /pytorch-project/pyproject.toml
RUN cd /pytorch-project &&\
poetry install

CMD cd /pytorch-project && poetry shell

FROM development AS train-model

ENV addArgs=''
ENV args='--model.weight_decay 0.08440353272813539 --model.learning_rate 0.00004315961071253895 --data.train_batch_size 24 --trainer.max_epochs 3 --seed_everything 42'
CMD cd /pytorch-project && poetry run python3 main.py fit $args $addArgs
