from hitchserve import Service


class NpmService(Service):
    def __init__(self, node_package, **kwargs):
        self.node_package = node_package
        kwargs['no_libfaketime'] = True
        kwargs['env_vars'] = node_package.environment_vars
        super(NodeService, self).__init__(**kwargs)
