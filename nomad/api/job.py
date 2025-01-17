"""Nomad job: https://developer.hashicorp.com/nomad/api-docs/jobs"""
import nomad.api.exceptions

from nomad.api.base import Requester


class Job(Requester):

    """
    The job endpoint is used for CRUD on a single job.
    By default, the agent's local region is used.

    https://www.nomadproject.io/docs/http/job.html
    """
    ENDPOINT = "job"

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
            self.get_job(item)
            return True
        except nomad.api.exceptions.URLNotFoundNomadException:
            return False

    def __getitem__(self, item):
        try:
            job = self.get_job(item)
            if job["ID"] == item:
                return job
            if job["Name"] == item:
                return job

            raise KeyError
        except nomad.api.exceptions.URLNotFoundNomadException as exc:
            raise KeyError from exc

    def get_job(self, _id, namespace=None):
        """ Query a single job for its specification and status.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
              - namespace :(str) optional, specifies the target namespace. Specifying * would return all jobs.
                        This is specified as a querystring parameter.
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        params = {}

        if namespace:
            params["namespace"] = namespace

        return self.request(_id, method="get", params=params).json()

    def get_versions(self, _id):
        """ This endpoint reads information about all versions of a job.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - id
            returns: list of dicts
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "versions", method="get").json()

    def get_allocations(self, _id):
        """ Query the allocations belonging to a single job.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
            returns: list
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "allocations", method="get").json()

    def get_evaluations(self, _id):
        """ Query the evaluations belonging to a single job.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "evaluations", method="get").json()

    def get_deployments(self, _id):
        """ This endpoint lists a single job's deployments

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "deployments", method="get").json()

    def get_deployment(self, _id):
        """ This endpoint returns a single job's most recent deployment.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
            returns: list of dicts
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "deployment", method="get").json()

    def get_summary(self, _id):
        """ Query the summary of a job.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "summary", method="get").json()

    def register_job(self, _id, job):
        """ Registers a new job or updates an existing job

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, json=job, method="post").json()

    def evaluate_job(self, _id):
        """ Creates a new evaluation for the given job.
            This can be used to force run the scheduling logic if necessary.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "evaluate", method="post").json()

    def plan_job(self, _id, job, diff=False, policy_override=False):
        """ Invoke a dry-run of the scheduler for the job.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
              - job, dict
              - diff, boolean
              - policy_override, boolean
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        json_dict = {}
        json_dict.update(job)
        json_dict.setdefault('Diff', diff)
        json_dict.setdefault('PolicyOverride', policy_override)
        return self.request(_id, "plan", json=json_dict, method="post").json()

    def periodic_job(self, _id):
        """ Forces a new instance of the periodic job. A new instance will be
            created even if it violates the job's prohibit_overlap settings.
            As such, this should be only used to immediately
            run a periodic job.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(_id, "periodic", "force", method="post").json()

    def dispatch_job(self, _id, payload=None, meta=None):
        """ Dispatches a new instance of a parameterized job.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
              - payload
              - meta
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        dispatch_json = {"Meta": meta, "Payload": payload}
        return self.request(_id, "dispatch", json=dispatch_json, method="post").json()

    def revert_job(self, _id, version, enforce_prior_version=None):
        """ This endpoint reverts the job to an older version.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
              - version, Specifies the job version to revert to.
            optional_arguments:
              - enforce_prior_version, Optional value specifying the current job's version.
                                       This is checked and acts as a check-and-set value before reverting to the
                                       specified job.
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        revert_json = {"JobID": _id,
                       "JobVersion": version,
                       "EnforcePriorVersion": enforce_prior_version}
        return self.request(_id, "revert", json=revert_json, method="post").json()

    def stable_job(self, _id, version, stable):
        """ This endpoint sets the job's stability.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
              - version, Specifies the job version to revert to.
              - stable, Specifies whether the job should be marked as stable or not.
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
        revert_json = {"JobID": _id,
                       "JobVersion": version,
                       "Stable": stable}
        return self.request(_id, "stable", json=revert_json, method="post").json()

    def deregister_job(self, _id, purge=None):
        """ Deregisters a job, and stops all allocations part of it.

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - _id
              - purge (bool), optionally specifies whether the job should be
                stopped and purged immediately (`purge=True`) or deferred to the
                Nomad garbage collector (`purge=False`).

            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
              - nomad.api.exceptions.InvalidParameters
        """
        params = None
        if purge is not None:
            if not isinstance(purge, bool):
                raise nomad.api.exceptions.InvalidParameters("purge is invalid "
                        f"(expected type {type(bool())} but got {type(purge)})")
            params = {"purge": purge}
        return self.request(_id, params=params, method="delete").json()
