import random
from enum import Enum
from typing import List, Optional

import requests


class AccessType(Enum):
    round_robin = "round_robin"
    choose_one = "choose_one"


class DistributedServiceComm:
    def __init__(self, service_address_list: List[str], access_type: AccessType = AccessType.round_robin):
        self.service_address_list = service_address_list
        self.access_type = access_type
        self.address_counter = 0

        self.reset_counter()

    def reset_counter(self):
        self.address_counter = random.randint(0, len(self.service_address_list))

    def send_post(self, json_data: Optional[dict] = None, entrypoint="",
                  address_index: Optional[int] = None) -> Optional[requests.Response]:
        if len(self.service_address_list) == 0:
            return None

        if address_index:
            return requests.post(self.service_address_list[address_index] + entrypoint, json=json_data)

        if self.access_type.round_robin:
            self.address_counter += 1
            self.address_counter %= len(self.service_address_list)
        response = requests.post(self.service_address_list[self.address_counter] + entrypoint, json=json_data)
        return response

    def send_post_data(self, data: Optional[str] = None, entrypoint="", address_index: Optional[int] = None) -> \
            Optional[requests.Response]:
        if len(self.service_address_list) == 0:
            return None

        if address_index:
            return requests.post(self.service_address_list[address_index] + entrypoint, data=data)

        if self.access_type.round_robin:
            self.address_counter += 1
            self.address_counter %= len(self.service_address_list)
        response = requests.post(self.service_address_list[self.address_counter] + entrypoint, data=data)
        return response
