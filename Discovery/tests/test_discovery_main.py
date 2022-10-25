from unittest import TestCase

from Discovery.discovery_main import register, main, delete
from Discovery.domain.models import RegistrationService, Service


class TestDiscoveryServiceCode(TestCase):
    def test_register_code(self, registration_services=None):
        if registration_services is None:
            return

        test_services = []

        for registration_service in registration_services:
            test_services.append(Service(fullAddress=f"http://{registration_service.Host}:{registration_service.Port}/",
                                         serviceName=registration_service.ServiceName))

        for registration_service in registration_services:
            register(None, registration_service)

        services = main()

        for service in test_services:
            assert service in services

    def test_delete_code(self, registration_services=None):
        if registration_services is None:
            return

        test_services = []

        for registration_service in registration_services:
            test_services.append(Service(fullAddress=f"http://{registration_service.Host}:{registration_service.Port}/",
                                         serviceName=registration_service.ServiceName))

        for registration_service in registration_services:
            delete(None, registration_service)

        services = main()

        for service in test_services:
            assert service not in services

    def test_register_and_delete_code(self, registration_services=None):
        if not registration_services:
            registration_services = [RegistrationService(Port="6969", Host="localhost", ServiceName="Testservice0")]

        self.test_register_code(registration_services)
        self.test_delete_code(registration_services)

    def test_multiple_register_and_delete_code(self, amount=10):
        test_register_port_start = 6969
        test_services = []

        for x in range(amount):
            test_services.append(RegistrationService(Port=f"{test_register_port_start + x}", Host=f"host{x}",
                                                     ServiceName=f"Testservice{x}"))

        self.test_register_and_delete_code(test_services)
