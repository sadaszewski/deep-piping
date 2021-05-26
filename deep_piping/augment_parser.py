def augment_parser(parser, config):
    for k, v in config.get('arguments', dict()).items():
        v = dict(v)
        if 'type' in v and isinstance(v['type'], str):
            v['type'] = eval(v['type'])
        parser.add_argument('--' + k.replace('_', '-'), **v)
    return parser
