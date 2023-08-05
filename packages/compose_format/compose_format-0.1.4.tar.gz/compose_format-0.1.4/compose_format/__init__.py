#!/usr/bin/env python3
from collections import OrderedDict
import pyaml
from yaml import load


class ComposeFormat:
    TOPLEVEL_ORDER = ['version', 'services', 'volumes', 'networks']
    SERVICE_ORDER = [
        'image', 'command', 'links',
        'volumes_from', 'volumes', 'expose', 'ports',
        'extra_hosts', 'restart', 'ulimits', 'tty']
    BUILD_ORDER = ['context', 'dockerfile']

    ORDERS = {
        'version': TOPLEVEL_ORDER,
        'image': SERVICE_ORDER,
        'dockerfile': BUILD_ORDER
    }

    def __init__(self):
        pass

    def format(self, path, replace=False):
        with open(path, 'r') as file:
            data = file.read()
        original = data
        formatted = self.format_string(data, replace=replace)

        if replace:
            with open(path, 'w') as file:
                file.write(formatted)
        else:
            print(formatted)
        return original == formatted

    def format_string(self, data, replace=False):
        data = self.reorder(load(data))

        def is_legacy_version(data):
            if 'version' not in data:
                return True
            return str(data['version']) != '2' and str(data['version']) != '\'2\''

        vspacing = [1, 0] if is_legacy_version(data) else [0, 1, 0]

        formatted = pyaml.dump(data, vspacing=vspacing, indent=2, width=120, string_val_style='plain')
        return formatted.strip() + '\n'

    @staticmethod
    def reorder(data):
        if type(data) is dict or type(data) is OrderedDict:
            for key in ComposeFormat.ORDERS.keys():
                if key not in data.keys():
                    continue
                current_order = ComposeFormat.ORDERS[key]

                def order(item):
                    key, _ = item
                    assert key in current_order, 'key: {0} not known'.format(key)

                    if key in current_order:
                        return current_order.index(key)
                    return len(current_order)

                result = {key: ComposeFormat.reorder(value) for key, value in data.items()}
                result = OrderedDict(sorted(result.items(), key=order))

                return result
            return {key: ComposeFormat.reorder(value) for key, value in data.items()}
        if type(data) is list:
            return sorted([ComposeFormat.reorder(item) for item in data])
        if len(str(data)) >= 1 and str(data)[0].isdigit():
            return '\'{}\''.format(data)
        return data
