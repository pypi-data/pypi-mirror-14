#!/usr/bin/env python
import json


def derive_type_list(k, v):
    if not v:
        return 'UNKNOWN_EMPTY_LIST', None
    v = v[0]
    if v is None:
        return 'Option<UNKNOWN_NULL>', None
    elif isinstance(v, basestring):
        return 'String', None
    elif isinstance(v, bool):
        return 'bool', None
    elif isinstance(v, int):
        return 'i32', None
    elif isinstance(v, float):
        return 'f32', None
    elif isinstance(v, dict):
        return derive_type_dict(k, v)


def derive_type_dict(k, v):
    name = k.title()
    return name, build_struct(name, v)


def build_struct(name, data):
    s = ''
    s += 'pub struct %s {\n' % name
    structs = {}
    for k, v in data.items():
        if v is None:
            s += '    pub %s: Option<UNKNOWN_NULL>,\n' % k
        elif isinstance(v, basestring):
            s += '    pub %s: String,\n' % k
        elif isinstance(v, bool):
            s += '    pub %s: bool,\n' % k
        elif isinstance(v, int):
            s += '    pub %s: i32,\n' % k
        elif isinstance(v, float):
            s += '    pub %s: f32,\n' % k
        elif isinstance(v, list):
            type_name, struct = derive_type_list(k, v)
            structs[type_name] = struct
            s += '    pub %s: Vec<%s>,\n' % (k, type_name)
        elif isinstance(v, dict):
            type_name, struct = derive_type_dict(k, v)
            structs[type_name] = struct
            s += '    pub %s: %s,\n' % (k, type_name)
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
    args = parser.parse_args()
    with open(args.path) as f:
        data = json.load(f)
    struct_str = build_struct(args.struct_name, data)
    print(struct_str)


if __name__ == '__main__':
    main()
