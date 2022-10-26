from unittest import TestCase

import requests

from Discovery.domain.models import RegistrationService, Service


class TestDiscoveryServiceApi(TestCase):
    def test_register_entrypoint(self, registration_services=None):
        if registration_services is None:
            return

        test_services = []

        for registration_service in registration_services:
            test_services.append(Service(fullAddress=f"http://{registration_service.Host}:{registration_service.Port}/",
                                         serviceName=registration_service.ServiceName))

        for registration_service in registration_services:
            response = requests.post(url="http://127.0.0.1:6969/register", json=registration_service.dict())
            assert response.status_code == 200

        response = requests.post(url="http://127.0.0.1:6969/")
        assert response.status_code == 200

        services_dict = response.json()
        services = []
        for service_dict in services_dict:
            # services.append(Service(**service_dict)) # For each key in the dictionary we assign a parameter of the same name that value
            services.append(Service(serviceName=service_dict["serviceName"],
                                    fullAddress=service_dict["fullAddress"]))

        for service in test_services:
            assert service in services

    def test_delete_entrypoint(self, registration_services=None):
        if registration_services is None:
            return

        test_services = []

        for registration_service in registration_services:
            test_services.append(Service(fullAddress=f"http://{registration_service.Host}:{registration_service.Port}/",
                                         serviceName=registration_service.ServiceName))

        for registration_service in registration_services:
            response = requests.post(url="http://127.0.0.1:6969/delete", json=registration_service.dict())
            assert response.status_code == 200

        response = requests.post(url="http://127.0.0.1:6969/")
        assert response.status_code == 200

        services_dict = response.json()
        services = []
        for service_dict in services_dict:
            services.append(Service(serviceName=service_dict["serviceName"],
                                    fullAddress=service_dict["fullAddress"]))

        for service in test_services:
            assert service not in services

    def test_register_and_delete_entrypoint(self, registration_services=None):
        if not registration_services:
            registration_services = [RegistrationService(Port="6969", Host="localhost", ServiceName="Testservice0")]

        self.test_register_entrypoint(registration_services)
        self.test_delete_entrypoint(registration_services)

    def test_multiple_register_and_delete_entrypoint(self, amount=10):
        test_register_port_start = 6969
        test_services = []

        for x in range(amount):
            test_services.append(RegistrationService(Port=f"{test_register_port_start + x}", Host=f"host{x}",
                                                     ServiceName=f"Testservice{x}"))

        self.test_register_and_delete_entrypoint(test_services)
