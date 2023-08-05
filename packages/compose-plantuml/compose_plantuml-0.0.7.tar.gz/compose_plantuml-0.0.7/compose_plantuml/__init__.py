#!/usr/bin/env python3
from yaml import load


class ComposePlantuml:

    def __init__(self):
        pass

    def parse(self, data):
        return load(data)

    def link_graph(self, compose):
        result = 'skinparam componentStyle uml2\n'

        for component in sorted(self.components(compose)):
            result += '[{0}]\n'.format(component)
        for source, destination in sorted(self.links(compose)):
            result += '[{0}] --> [{1}]\n'.format(source, destination)
        for source, destination in sorted(self.dependencies(compose)):
            result += '[{0}] ..> [{1}] : depends on\n'.format(source, destination)
        return result.strip()

    def boundaries(self, compose):
        result = 'skinparam componentStyle uml2\n'

        result += 'cloud system {\n'
        for component in sorted(self.components(compose)):
            result += '  [{0}]\n'.format(component)
        result += '}\n'
        volume_registry = {}
        for volume in sorted(self.volumes(compose)):
            result += 'database {0}'.format(volume) + ' {\n'
            for usage in sorted(self.volume_usage(compose, volume)):
                registry_name = 'volume_{0}'.format(len(volume_registry.keys()) + 1)
                volume_registry['{0}.{1}'.format(volume, usage)] = registry_name
                result += '  [{0}] as {1}\n'.format(usage, registry_name)
            result += '}\n'

        for service, host, container in sorted(self.ports(compose)):
            port = host
            if container is not None:
                port = '{0} : {1}'.format(host, container)
            result += '[{0}] --> {1}\n'.format(service, port)

        for volume in sorted(self.volumes(compose)):
            for service, volume_path in sorted(self.service_using_path(compose, volume)):
                name = volume_path
                if '{0}.{1}'.format(volume, volume_path) in volume_registry:
                    name = volume_registry['{0}.{1}'.format(volume, volume_path)]
                result += '[{0}] --> {1}\n'.format(service, name)
        return result.strip()

    @staticmethod
    def components(compose):
        if 'version' not in compose:
            return [component for component in compose]
        return [component for component in compose.get('services', [])]

    @staticmethod
    def links(compose):
        result = []
        components = compose if 'version' not in compose else compose.get('services', {})

        for component_name, component in components.items():
            for link in component.get('links', []):
                link = link if ':' not in link else link.split(':')[0]
                result.append((component_name, link))
        return result

    @staticmethod
    def dependencies(compose):
        result = []
        components = compose if 'version' not in compose else compose.get('services', {})

        for component_name, component in components.items():
            for dependency in component.get('depends_on', []):
                result.append((component_name, dependency))
        return result

    @staticmethod
    def ports(compose):
        result = []
        components = compose if 'version' not in compose else compose.get('services', {})

        for component_name, component in components.items():
            for port in component.get('ports', []):
                port = str(port)
                host, container = (port, None)
                if ':' in port:
                    host, container = port.split(':')
                result.append((component_name, host, container))
        return result

    @staticmethod
    def volumes(compose):
        if 'version' not in compose:
            return []  # TODO: support for version 1
        volumes = compose.get('volumes', {})

        return list(volumes.keys())

    @staticmethod
    def volume_usage(compose, volume):
        result = []
        components = compose if 'version' not in compose else compose.get('services', {})

        for component_name, component in components.items():
            for volume_name in component.get('volumes', {}):
                if not volume_name.startswith('{0}:'.format(volume)):
                    continue
                result.append(volume_name.split(':')[1])
        return result

    @staticmethod
    def service_using_path(compose, volume):
        result = []
        components = compose if 'version' not in compose else compose.get('services', {})

        for component_name, component in components.items():
            for volume_name in component.get('volumes', {}):
                if not volume_name.startswith('{0}:'.format(volume)):
                    continue
                result.append((component_name, volume_name.split(':')[1]))
        return result
