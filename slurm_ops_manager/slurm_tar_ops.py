#!/usr/bin/python3
"""install slurm via tarball."""
import os
import subprocess
from pathlib import Path

from slurm_ops_manager.install import TarInstall


class SlurmTarManager:
    """config values of slurm tar binary install."""

    _CHARM_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
    _TEMPLATE_DIR = _CHARM_DIR / 'templates'

    def __init__(self, component, res_path):
        """Determine values based on slurm component."""
        self._slurm_component = component
        self._resource = res_path
        if component == "slurmdbd":
            self._template_name = "slurmdbd.conf.tmpl"
            self._target = Path(
                    "/etc/slurm/slurmdbd.conf")
        else:
            self._template_name = "slurm.conf.tmpl"
            self._target = Path("/etc/slurm/slurm.conf")
        self._source = Path(self._TEMPLATE_DIR / self._template_name)
        self._slurm_installer = TarInstall(component, res_path)
        self._munge_key_path = Path("/etc/munge/munge.key")
        self.config_values = {
            "munge_socket": "/var/run/munge/munge.socket.2",
            "mail_prog": "/usr/bin/mail",
            "slurm_user": "slurm",
            "slurmctld_pid_file": "/srv/slurm/slurmctld.pid",
            "slurmd_pid_file": "/srv/slurm/slurmd.pid",
            "slurmctld_log_file": "/var/log/slurm/slurmctld.log",
            "slurmd_log_file": "/var/log/slurm/slurmd.log",
            "slurm_spool_dir": "/var/spool/slurm/d",
            "slurm_state_dir": "/var/spool/slurm/ctld",
            "slurm_plugin_dir": "/usr/local/lib/slurm",
            "slurm_plugstack_conf":
            "/etc/slurm/plugstack.d/plugstack.conf",
            "munge_socket": "/var/run/munge/munge.socket.2",
            "slurmdbd_pid_file": "/srv/slurm/slurmdbd.pid",
            "slurmdbd_log_file": "/var/log/slurm/slurmdbd.log",
        }

    @property
    def munge_key_path(self):
        """Return the munge key path."""
        return self._munge_key_path

    def get_version(self):
        """Get slurm version."""
        cp = subprocess.run(
            [self._slurm_component, "-V"],
            universal_newlines=True,
            stdout=subprocess.PIPE,
        )
        return cp.stdout[0:-1]

    @property
    def config(self):
        """Get slurm config."""
        return self.config_values

    def get_systemd_name(self):
        """Get systemd name."""
        return self._slurm_component

    def get_tmpl_name(self):
        """Get template name."""
        return self._template_name

    def get_template(self):
        """Get template location."""
        return self._source

    def get_target(self):
        """Get target path."""
        return self._target

    @property
    def munge_sysd(self):
        """Get munge."""
        return "munge"

    def get_munge_key_path(self):
        """Get munge key path."""
        return self._munge_key_path

    def install(self):
        """Install slurm."""
        self._slurm_installer.prepare_system_for_slurm()