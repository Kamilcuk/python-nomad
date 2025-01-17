"""Nomad Node: https://developer.hashicorp.com/nomad/api-docs/nodes"""
import nomad.api.exceptions

from nomad.api.base import Requester


class Node(Requester):

    """
    The node endpoint is used to query the a specific client node.
    By default, the agent's local region is used.

    https://www.nomadproject.io/docs/http/node.html
    """
    ENDPOINT = "node"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"{self.__dict__}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __getattr__(self, item):
        msg = f"{item} does not exist"
        raise AttributeError(msg)

    def __contains__(self, item):

        try:
            self.get_node(item)
            return True
        except nomad.api.exceptions.URLNotFoundNomadException:
            return False

    def __getitem__(self, item):

        try:
            node = self.get_node(item)

            if node["ID"] == item:
                return node
            if node["Name"] == item:
                return node

            raise KeyError
        except nomad.api.exceptions.URLNotFoundNomadException as exc:
            raise KeyError from exc

    def get_node(self, _id):
        """ Query the status of a client node registered with Nomad.

           https://www.nomadproject.io/docs/http/node.html

            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, method="get").json()

    def get_allocations(self, _id):
        """ Query the allocations belonging to a single node.

           https://www.nomadproject.io/docs/http/node.html

            returns: list
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "allocations", method="get").json()

    def evaluate_node(self, _id):
        """ Creates a new evaluation for the given node.
            This can be used to force run the
            scheduling logic if necessary.

           https://www.nomadproject.io/docs/http/node.html

            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "evaluate", method="post").json()

    def drain_node(self, _id, enable=False):
        """ Toggle the drain mode of the node.
            When enabled, no further allocations will be
            assigned and existing allocations will be migrated.

           https://www.nomadproject.io/docs/http/node.html

            arguments:
              - _id (str uuid): node id
              - enable (bool): enable node drain or not to enable node drain
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """

        return self.request(_id, "drain", params={"enable": enable}, method="post").json()

    def drain_node_with_spec(self, _id, drain_spec, mark_eligible=None):
        """ This endpoint toggles the drain mode of the node. When draining is enabled,
            no further allocations will be assigned to this node, and existing allocations
            will be migrated to new nodes.

            If an empty dictionary is given as drain_spec this will disable/toggle the drain.

            https://www.nomadproject.io/docs/http/node.html

            arguments:
              - _id (str uuid): node id
              - drain_spec (dict): https://www.nomadproject.io/api/nodes.html#drainspec
              - mark_eligible (bool): https://www.nomadproject.io/api/nodes.html#markeligible
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        payload = {}

        if drain_spec and mark_eligible is not None:
            payload = {
                "NodeID": _id,
                "DrainSpec": drain_spec,
                "MarkEligible": mark_eligible
            }
        elif drain_spec and mark_eligible is None:
            payload = {
                "NodeID": _id,
                "DrainSpec": drain_spec
            }
        elif not drain_spec and mark_eligible is not None:
            payload = {
                "NodeID": _id,
                "DrainSpec": None,
                "MarkEligible": mark_eligible
            }
        elif not drain_spec and mark_eligible is None:
            payload = {
                "NodeID": _id,
                "DrainSpec": None,
            }

        return self.request(_id, "drain", json=payload, method="post").json()

    def eligible_node(self, _id, eligible=None, ineligible=None):
        """ Toggle the eligibility of the node.

           https://www.nomadproject.io/docs/http/node.html

            arguments:
              - _id (str uuid): node id
              - eligible (bool): Set to True to mark node eligible
              - ineligible (bool): Set to True to mark node ineligible
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        payload = {}

        if eligible is not None and ineligible is not None:
            raise nomad.api.exceptions.InvalidParameters
        if eligible is None and ineligible is None:
            raise nomad.api.exceptions.InvalidParameters

        if eligible is not None and eligible:
            payload = {"Eligibility": "eligible", "NodeID": _id}
        elif eligible is not None and not eligible:
            payload = {"Eligibility": "ineligible", "NodeID": _id}
        elif ineligible is not None:
            payload = {"Eligibility": "ineligible", "NodeID": _id}
        elif ineligible is not None and not ineligible:
            payload = {"Eligibility": "eligible", "NodeID": _id}

        return self.request(_id, "eligibility", json=payload, method="post").json()

    def purge_node(self, _id):
        """ This endpoint purges a node from the system. Nodes can still join the cluster if they are alive.
        arguments:
          - _id (str uuid): node id
        returns: dict
        raises:
          - nomad.api.exceptions.BaseNomadException
          - nomad.api.exceptions.URLNotFoundNomadException
        """

        return self.request(_id, "purge", method="post").json()
