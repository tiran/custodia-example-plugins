from __future__ import absolute_import

from custodia import log
from custodia.plugin import HTTPAuthenticator, PluginOption, REQUIRED


class ExampleAuth(HTTPAuthenticator):
    header = PluginOption(str, 'REMOTE_USER', "header name")
    value = PluginOption(str, REQUIRED, "required value")

    def handle(self, request):
        if self.header not in request['headers']:
            self.logger.debug('SHA: No "headers" in request')
            return None
        value = request['headers'][self.header]
        if self.value is not None:
            # pylint: disable=unsupported-membership-test
            if value != self.value:
                self.audit_svc_access(log.AUDIT_SVC_AUTH_FAIL,
                                      request['client_id'], value)
                return False

        self.audit_svc_access(log.AUDIT_SVC_AUTH_PASS,
                              request['client_id'], value)
        request['remote_user'] = value
        return True
