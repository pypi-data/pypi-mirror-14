"""
Xen virtual machines.

http://www.xenproject.org/
"""

import os
from pathlib import Path
import shlex
import subprocess

from . import Container, ContainerConfig


class Xen(Container):
    """
    Represents and manages a Xen domain.

    This only supports the xl toolstack and qcow2 diskimages.
    """

    def __init__(self, cfg):
        super().__init__(cfg)
        self.manage = False
        self.running_image = None

    @classmethod
    def config(cls, machine_id, cfgdata, cfgpath):
        cfg = ContainerConfig(machine_id, cfgdata, cfgpath)

        xlcfg = Path(cfgdata["xl_cfg_file"])
        if xlcfg.is_absolute():
            xlcfg = cfgpath / xlcfg

        cfg.xlcfg = xlcfg
        cfg.base_image = Path(cfgdata["base_image"])
        cfg.overlay_image = Path(cfgdata["overlay_image"])

        if not cfg.base_image.is_file():
            raise FileNotFoundError("base image: " + str(cfg.base_image))

        return cfg

    def prepare(self, manage=False):
        self.manage = manage

        if not self.manage:
            # create a temporary runimage

            idx = 0
            while True:
                tmpimage = Path(str(self.cfg.overlay_image) + "_%02d" % idx)
                if not tmpimage.is_file():
                    break
                idx += 1

            self.running_image = tmpimage

            command = [
                "qemu-img", "create",
                "-o", "backing_file=" + str(self.cfg.base_image),
                "-f", "qcow2",
                str(self.running_image),
            ]
            if subprocess.call(command) != 0:
                raise RuntimeError("could not create overlay image")

        else:
            # to manage, use the base image to run
            pass

    def launch(self):
        # replace the disk with the working copy
        command = [
            "xl", "create", self.cfg.xlcfg,
            "disk=[format=qcow2, vdev=xvda, access=rw, target=%s]" % (
                str(self.running_image)),
        ]

        # TODO: somehow pass self.ssh_port
        #       maybe the host requires changing!

        if subprocess.call(command) != 0:
            raise VMError("failed to create xen domain")

    def is_running(self):
        # xl vm-list
        raise NotImplementedError()

        return running

    def terminate(self):
        # wait_a_bit(xl shutdown -w $domainid)
        # xl destroy $domainid
        raise NotImplementedError()

    def cleanup(self):
        if not (self.manage or self.running_image is None):
            try:
                os.unlink(str(self.running_image))
            except FileNotFoundError:
                pass
