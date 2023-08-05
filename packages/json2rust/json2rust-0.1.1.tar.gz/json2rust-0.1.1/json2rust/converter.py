#!/usr/bin/env python
import json


def derive_type_list(k, v, **kwargs):
    if not v:
        return 'UNKNOWN_EMPTY_LIST', None
    v = v[0]
    if v is None:
        return 'UNKNOWN_NULL', None
    elif isinstance(v, basestring):
        return 'String', None
    elif isinstance(v, bool):
        return 'bool', None
    elif isinstance(v, int):
        return 'i32', None
    elif isinstance(v, float):
        return 'f32', None
    elif isinstance(v, dict):
        return derive_type_dict(k, v, **kwargs)


def derive_type_dict(k, v, **kwargs):
    name = k.title()
    return name, build_struct(name, v, **kwargs)


def build_struct(name, data, option=False):
    s = ''
    s += 'pub struct %s {\n' % name
    structs = {}
    for k, v in data.items():
        if v is None:
            typ = 'UNKNOWN_NULL'
        elif isinstance(v, basestring):
            typ = 'String'
        elif isinstance(v, bool):
            typ = 'bool'
        elif isinstance(v, int):
            typ = 'i32'
        elif isinstance(v, float):
            typ = 'f32'
        elif isinstance(v, list):
            typ, struct = derive_type_list(k, v, option=option)
            typ = 'Vec<%s>' % typ
            structs[typ] = struct
        elif isinstance(v, dict):
            typ, struct = derive_type_dict(k, v, option=option)
            structs[typ] = struct
        if option:
            typ = 'Option<%s>' % typ
        s += '    pub %s: %s,\n' % (k, typ)
    s += '}\n'
    for v in structs.values():
        if v is None:
            continue
        s += v
    return s


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('struct_name')
    parser.add_argument('path')
    parser.add_argument('--option', '-o', action='store_true',
                        help='wrap fields in Option')
    args = parser.parse_args()
    with open(args.path) as f:
        data = json.load(f)
    struct_str = build_struct(args.struct_name, data, option=args.option)
    print(struct_str)


if __name__ == '__main__':
    main()
