from deep_piping import load_config, \
    augment_parser, \
    materialize_config
from argparse import ArgumentParser


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('--config', type=str)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    config = load_config(args.config)
    augment_parser(parser, config)
    args = parser.parse_args()
    container = materialize_config(config, args)
    model = container['model']
    trainer = container['trainer']
    trainer.fit(model)
    if hasattr(trainer, 'test'):
        trainer.test(model)


if __name__ == '__main__':
    main()
