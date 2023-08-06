from collections import OrderedDict
import dpath.util as dpath
import tablib
import sys
import click
import uuid

def is_uuid(str):
    try:
        uuid.UUID(str)
        return True
    except ValueError:
        return False

def lookup_resource_id(list, id_rep):
    if hasattr(list, '__call__'):
        list = list().get('data')
    lookup = {}
    _is_uuid = is_uuid(id_rep)
    short_id_matches = []
    name_matches = []
    for entry in list:
        entry_id = entry.get('id')
        if _is_uuid:
            if entry_id == id_rep:
                return entry_id
        else:
            short_id = shorten_id(entry_id)
            if short_id == id_rep:
                short_id_matches.append(entry_id)
            else:
                try:
                    entry_name = dpath.get(entry, "attributes/name")
                    if entry_name == id_rep:
                        name_matches.append(entry_id)
                except KeyError:
                    pass
    if len(short_id_matches) == 0 and len(name_matches) == 0:
        raise KeyError('Id ' + id_rep.encode('ascii')  + ' does not exist')
    elif len(short_id_matches) == 1 and len(name_matches) == 0:
        return short_id_matches[0]
    elif len(short_id_matches) == 0 and len(name_matches) == 1:
        return name_matches[0]
    else:
        raise KeyError('Ambiguous id: ' + id_rep.encode('ascii'))

def shorten_id(str):
    return str.split('-')[0]

def shorten_json_id(json):
    return shorten_id(json.get('id'))

def tabulate(result, map):
    mapping = OrderedDict(map)
    if not mapping or not result: return result

    def _lookup(o, path):
        try:
            if hasattr(path, '__call__'):
                return path(o)
            else:
                return dpath.get(o, path)
        except KeyError, e:
            return ""

    def map_object(o, mapping):
        return [_lookup(o, path) for k, path in mapping.items()]

    mapped_result = [map_object(o, mapping) for o in result]
    data = tablib.Dataset(*mapped_result, headers=mapping.keys())
    return data

def output(result):
    if sys.stdout.isatty():
        click.echo(result)
    elif result.export:
        click.echo(result.export('csv'))
    else:
        click.echo(result)
