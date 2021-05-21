def augment_parser(parser, config):
    for k, v in config['arguments'].items():
        v = dict(v)
        if 'type' in v:
            v['type'] = eval(v['type'])
        parser.add_argument('--' + k.replace('_', '-'), **v)
    return parser
