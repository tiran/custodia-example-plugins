from __future__ import absolute_import

from custodia import log
from custodia.plugin import HTTPAuthorizer, PluginOption


class ExampleAuthz(HTTPAuthorizer):
    startswith = PluginOption(str, '/secret/example', None)

    def __init__(self, config, section):
        super(ExampleAuthz, self).__init__(config, section)
        self.startswith = self.startswith.split('/')

    def handle(self, request):
        path = request['path_chain']
        if self.startswith == path[:len(self.startswith)]:
            self.audit_svc_access(log.AUDIT_SVC_AUTHZ_PASS,
                                  request['client_id'], path)
            return True

        self.logger.debug("Path '%s' does not start with '%s'",
                          path, self.startswith)
        return None
