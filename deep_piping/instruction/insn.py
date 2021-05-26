class Instruction:
    def __init__(self, callback_mask=[ "step" ]):
        self.callback_mask = callback_mask

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
