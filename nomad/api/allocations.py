"""Nomad allocation: https://developer.hashicorp.com/nomad/api-docs/allocations"""
from typing import Optional

from nomad.api.base import Requester


class Allocations(Requester):
    """
    The allocations endpoint is used to query the status of allocations.
    By default, the agent's local region is used; another region can be
    specified using the ?region= query parameter.

    https://www.nomadproject.io/docs/http/allocs.html
    """

    ENDPOINT = "allocations"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"{self.__dict__}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __getattr__(self, item):
        raise AttributeError

    def __len__(self):
        response = self.get_allocations()
        return len(response)

    def __iter__(self):
        response = self.get_allocations()
        return iter(response)

    def get_allocations(  # pylint: disable=too-many-arguments
        self,
        prefix: Optional[str] = None,
        filter_: Optional[str] = None,
        namespace: Optional[str] = None,
        resources: Optional[bool] = None,
        task_states: Optional[bool] = None,
    ):
        """Lists all the allocations.

        https://www.nomadproject.io/docs/http/allocs.html
         arguments:
           - prefix :(str) optional, specifies a string to filter allocations on based on an prefix.
                     This is specified as a querystring parameter.
           - filter_ :(str) optional
                     Name has a trailing underscore not to conflict with builtin function.
           - namespace :(str) optional, specifies the target namespace. Specifying * would return all jobs.
                     This is specified as a querystring parameter.
           - resources :(bool) optional
           - task_states :(bool) optional
         returns: list
         raises:
           - nomad.api.exceptions.BaseNomadException
           - nomad.api.exceptions.URLNotFoundNomadException
        """
        params = {
            "prefix": prefix,
            "filter": filter_,
            "namespace": namespace,
            "resources": resources,
            "task_states": task_states,
        }
        return self.request(method="get", params=params).json()
