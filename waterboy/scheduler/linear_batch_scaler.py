
import waterboy.api.base as base

from waterboy.api import BatchIdx


class LinearBatchScaler(base.Callback):
    """ Scales linearly LR from maximum value to 0 through every batch of training """
    def __init__(self, optimizer):
        self.optimizer = optimizer

        # TODO(jerry): handle restarting
        self.starting_lr = [p['lr'] for p in self.optimizer.param_groups]

    def on_batch_begin(self, batch_idx: BatchIdx):
        for starting_lr, param_group in zip(self.starting_lr, self.optimizer.param_groups):
            param_group['lr'] = starting_lr * (1.0 - batch_idx.extra['progress_meter'])


class LinearBatchScalerFactory(base.SchedulerFactory):
    """ Factory class for linear batch scaler scheduler """
    def instantiate(self, optimizer, last_epoch=-1) -> LinearBatchScaler:
        return LinearBatchScaler(optimizer)


def create():
    return LinearBatchScalerFactory()


