def _is_docker() -> bool:
    """Determine whether the current environment is within a Docker container."""
    # https://tuhrig.de/how-to-know-you-are-inside-a-docker-container/
    with open('/proc/self/cgroup') as cgroup_stream:
        # This file should be small enough to fully read into memory
        return 'docker' in cgroup_stream.read()


class _AlwaysContains(object):
    """An object which always returns True for `x in _AlwaysContains()` operations."""

    def __contains__(self, item) -> bool:
        # https://stackoverflow.com/a/49818040
        return True
