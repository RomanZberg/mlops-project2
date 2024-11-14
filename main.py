import wandb
import lightning as L
from pathlib import Path
from lightning.pytorch.callbacks import Callback
from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.cli import LightningCLI
from pytorch_lightning.loggers import WandbLogger
from src.datamodules import GLUEDataModule
from src.models import GLUETransformer

class SaveModelCheckpointsCallback(Callback):
    def on_train_end(self, trainer, pl_module):
        wandb.save('checkpoints/*ckpt*')

class MyLightningCLI(LightningCLI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def instantiate_trainer(self,**kwargs):
        hyper_param_string = '-'.join([
            f'{key}_{value}' if type(value) is not str else f'{key}_{value}' for key, value in \
            map(lambda x: (x[0].replace('_', '-'), x[1]),self.config_dump["model"].items())\
            if (value is not None) and (key not in ('task-name', 'model-name-or-path', 'eval-batch-size'))
        ])

        run_name_elements = []
        if self.config_dump["wandb_run_name_prefix"] is not None:
            run_name_elements.append(self.config_dump["wandb_run_name_prefix"])

        run_name_elements.append(hyper_param_string)

        wandb_args = {
            "project": self.config_dump["wandb_project"],
            "name": '/'.join(run_name_elements)
        }

        if self.config_dump["wandb_entity"] is not None:
            wandb_args["entity"] = self.config_dump["wandb_entity"]

        wandb_logger = WandbLogger(
            **wandb_args,
            config={
                "random_seed": self.config_dump["seed_everything"]
            }
        )

        trainer_config = {
            key: value for key, value in self.config_dump["trainer"].items() if key not in [
                'accelerator', 'devices', 'logger', 'callbacks'
            ]
        }

        checkpoint_callback_max_accuracy = ModelCheckpoint(monitor="accuracy", mode="max",
                                                           filename="best-accuracy-{epoch:02d}",
                                                           dirpath=Path(wandb_logger.experiment.dir) / "checkpoints")
        checkpoint_callback_epoch = ModelCheckpoint(monitor="epoch", mode="max", filename="last-{epoch:02d}",
                                                    dirpath=Path(wandb_logger.experiment.dir) / "checkpoints")

        save_model_checkpoints_callback = SaveModelCheckpointsCallback()

        return L.Trainer(
            accelerator="auto",
            devices=1,
            logger=wandb_logger,
            **trainer_config,
            callbacks=[
                save_model_checkpoints_callback,
                checkpoint_callback_max_accuracy,
                checkpoint_callback_epoch
            ]
        )

    def add_arguments_to_parser(self, parser):
        parser.link_arguments("data.num_labels", "model.num_labels", apply_on="instantiate")

        parser.link_arguments("data.train_batch_size", "model.train_batch_size")
        parser.link_arguments("data.eval_batch_size", "model.eval_batch_size")

        parser.link_arguments("model.model_name_or_path", "data.model_name_or_path")
        parser.link_arguments("model.task_name", "data.task_name")

        parser.add_argument("--wandb-project", type=str, default="mlops-project-2")
        parser.add_argument("--wandb-entity", type=str, default=None)
        parser.add_argument("--wandb-run-name-prefix", type=str, default=None)

def cli_main():
    cli = MyLightningCLI(GLUETransformer, GLUEDataModule, save_config_kwargs={"overwrite": True})

if __name__ == '__main__':
    cli_main()