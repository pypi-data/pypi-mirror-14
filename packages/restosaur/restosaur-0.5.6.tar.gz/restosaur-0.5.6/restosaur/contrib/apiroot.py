from restosaur import API


class ResourceAlreadyRegistered(Exception):
    pass


class ApiRoot(object):
    def __init__(self):
        self.resources = {}

    def register(self, resource, name):
        if name in self.resources:
            raise ResourceAlreadyRegistered(name)
        self.resources[name]=resource

    def expose(self, name, resource):
        def wrap(resource):
            self.register(resource, name)
            return resource
        return wrap

    def as_view(self):
        def get_api_root(ctx):
            data = {}

            for name, resource in self.resources.items():
                data[name]=resource.uri(ctx)

            return ctx.Entity(data)
        return get_api_root


