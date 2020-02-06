from qgis.PyQt.QtCore import QSettings

from asistente_ladm_col.utils.singleton import Singleton


class TransitionSystemConfig(metaclass=Singleton):
    ST_DEFAULT_DOMAIN = "http://apist.proadmintierra.info"  # "http://192.168.98.61:8090"
    ST_LOGIN_SERVICE_PAYLOAD = "username={}&password={}&grant_type=password"
    encoded = b'c3Qtd2ViLWRldmVsb3AtZHZLREtnUXI6MTIzNDU='  # b'c3Qtd2ViLXNkVmExTlh3OmhLYmNlTjg5'
    ST_LOGIN_AUTHORIZATION_CLIENT = "Basic {}".format(encoded.decode('utf-8'))
    ST_EXPECTED_RESPONSE = "unauthorized"

    def get_domain(self):
        return QSettings().value('Asistente-LADM_COL/sources/service_transition_system', self.ST_DEFAULT_DOMAIN)

    @property
    def ST_LOGIN_SERVICE_URL(self):
        return "{}/api/security/oauth/token".format(self.get_domain())

    @property
    def ST_GET_TASKS_SERVICE_URL(self):
        return "{}/api/workspaces/v1/tasks/pending".format(self.get_domain())


