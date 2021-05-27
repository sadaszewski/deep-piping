from .insn import Instruction


class ClfForward(Instruction):
    def __init__(self, batch_element_names, map_names, output_element_names, **kwargs):
        super().__init__(**kwargs)
        self.batch_element_names = batch_element_names
        self.map_names = map_names
        self.output_element_names = output_element_names

    def __call__(self, context):
        batch = context['batch']
        feed = { k: batch[i] for i, k in enumerate(self.batch_element_names) }
        context.update(feed)
        feed = { k: context[v] for k, v in self.map_names.items() }
        output = context['ml_model'](**feed)
        for i, el in enumerate(output):
            context[self.output_element_names[i]] = el

        y_pred = context['logits'].argmax(1)
        context['y_pred'] = y_pred


class Return(Instruction):
    def __init__(self, names, **kwargs):
        super().__init__(**kwargs)
        self.names = names

    def __call__(self, context):
        context['result'].update({ k: context[k] for k in self.names })


class ReturnItems(Instruction):
    def __init__(self, dict_name, item_names, **kwargs):
        super().__init__(**kwargs)
        self.dict_name = dict_name
        self.item_names = item_names

    def __call__(self, context):
        d = context[self.dict_name]
        context['result'].update({ k: d[k] for k in self.item_names })


class RecomposeOutputs(Instruction):
    def __init__(self, names, **kwargs):
        super().__init__(kwargs)
        self.names = names

    def __call__(self, context):
        outputs = context['outputs']
        for n in self.names:
            context[n] = torch.cat([ out[n] for out in outputs ])


class Log(Instruction):
    def __init__(self, map_names, use_phase_prefix=True, **kwargs):
        super().__init__(**kwargs)
        self.map_names = map_names
        self.use_phase_prefix = use_phase_prefix

    def __call__(self, context):
        prefix = (context['phase'] + '_') if self.use_phase_prefix else ''
        context['logger'].log_metrics({ (prefix + k): context[v] \
            for k, v in self.map_names.items() })


class GetFromContext(Instruction):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __call__(self, context):
        return context[self.name]


class LogitsToPred(Instruction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, context):
        context['y_pred'] = context['logits'].argmax(dim=1)


class ToCPU(Instruction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, context):
        context_cpu = { k: v.cpu() if isinstance(v, torch.Tensor) else v
            for k, v in context.items() }
        context.update(context_cpu)
