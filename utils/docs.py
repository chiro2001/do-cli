def get_class_docs(class_, target_methods=None):
    def parse_doc(text: str):
        if text is None or len(text) == 0:
            return None
        lines = text.split('\n')
        if lines[0] == '':
            lines = lines[1:]
        if lines[-1] == '' or lines[-1].startswith('    '):
            lines = lines[:-1]
        res = ''
        for li in lines:
            while li.startswith(' '):
                li = li[1:]
            res = res + li + '\n'
        res = res[:-1]
        return res

    if target_methods is None:
        target_methods = [
            'get', 'post', 'put', 'delete', 'patch'
        ]
    dirs = dir(class_)
    result = {
        'disc': parse_doc(class_.__doc__),
        'methods': {}
    }
    # print('class', class_.__name__)
    for d in dirs:
        if d not in target_methods:
            continue
        target = eval(f"class_.{d}")
        # print(d, dir(target))
        if type(target) is not None and ('__doc__' in dir(target) or '__args_parser__' in dir(target)):
            doc = parse_doc(target.__doc__) if '__args_parser__' not in dir(target) else parse_doc(
                target.__inner__.__doc__)
            # print(d, doc)
            if d not in result['methods']:
                result['methods'][d] = {}
            if doc is not None:
                result['methods'][d]['disc'] = doc
            if '__args_parser__' in dir(target):
                args_parser = target.__args_parser__
                args = [{
                    'name': arg.name,
                    'type': arg.type.__name__,
                    'location': arg.location,
                    'help': arg.help,
                    'choices': arg.choices
                } for arg in args_parser.args]
                # print(d, args)
                result['methods'][d]['args'] = args
    return result
