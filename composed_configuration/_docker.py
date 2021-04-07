from pathlib import Path


def _is_docker() -> bool:
    """Determine whether the current environment is within a Docker container."""
    # https://tuhrig.de/how-to-know-you-are-inside-a-docker-container/
    cgroup_file = Path('/proc/self/cgroup')
    if cgroup_file.exists():
        with cgroup_file.open() as cgroup_stream:
            # This file should be small enough to fully read into memory
            return 'docker' in cgroup_stream.read()
    else:
        # Maybe running on macOS
        return False


class _AlwaysContains(object):
    """An object which always returns True for `x in _AlwaysContains()` operations."""

    def __contains__(self, item) -> bool:
        # https://stackoverflow.com/a/49818040
        return True
