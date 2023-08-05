"""A minimal command-line utility for booting SpiNNaker machines.

Installed as "rig-boot" by setuptools.
"""

import sys
import argparse

import rig

from rig.machine_control import boot, MachineController

from rig.machine_control.machine_controller import SpiNNakerBootError

from rig.geometry import standard_system_dimensions

BOOT_OPTION_POSTFIX = "_boot_options"
"""Postfix for boot option dicts in boot."""


def main(args=None):
    parser = argparse.ArgumentParser(description="Boot a SpiNNaker board")
    parser.add_argument("--version", "-V", action="version",
                        version="%(prog)s {}".format(rig.__version__))

    parser.add_argument("hostname", type=str,
                        help="hostname or IP of SpiNNaker system")

    parser.add_argument("width", type=int, default=None, nargs="?",
                        metavar="num_boards|width",
                        help="number of (SpiNN-5) boards or width "
                             "of SpiNNaker system")
    parser.add_argument("height", type=int, default=None, nargs="?",
                        help="height of SpiNNaker system")
    parser.add_argument("--hardware-version", type=int, default=None,
                        help="board hardware version number")
    parser.add_argument("--led-config", type=int, default=None,
                        help="LED configuration word")

    parser.add_argument("--binary", type=str, default=None,
                        help="binary to boot the system with")

    # Automatically build a list of available machine parameters by inspecting
    # boot module.
    type_group = parser.add_mutually_exclusive_group()
    for dict_name in dir(boot):
        if dict_name.endswith(BOOT_OPTION_POSTFIX):
            type_name = dict_name[:-len(BOOT_OPTION_POSTFIX)]
            option_name = "--{}".format(type_name)
            option_dict = getattr(boot, dict_name)
            option_help = "use predefined boot options for a {} board".format(
                type_name)
            type_group.add_argument(option_name, action="store_const",
                                    const=option_dict, default={},
                                    dest="machine_type",
                                    help=option_help)

    args = parser.parse_args(args)

    # Check that either a width and height have been supplied or a predefined
    # set of machine parameters was chosen.
    if (args.width is None and args.height is None and
            args.machine_type == {}):
        parser.error("either a number of boards or a width and height must "
                     "be specified or a predefined boot option selected")
    elif args.width is not None and args.height is None:
        # A number of boards was given, infer the width and height
        if args.width % 3 == 0:
            args.width, args.height = standard_system_dimensions(args.width)
        else:
            parser.error("the number of boards must be a multiple of three")

    # Accumulate the set of options from the commandline
    options = {
        "hardware_version": 0,
        "led_config": 0x00000001,
        "boot_data": (open(args.binary, "rb").read()
                      if args.binary is not None else None),
    }
    options.update(args.machine_type)
    options.update({
        opt_name: getattr(args, opt_name)
        for opt_name in "width height hardware_version led_config".split()
        if getattr(args, opt_name) is not None
    })

    # Attempt to boot the machine
    mc = MachineController(args.hostname)
    try:
        if mc.boot(**options):
            return 0
        else:
            # The machine was already booted.
            sys.stderr.write(
                "{}: error: machine already booted.\n".format(parser.prog))
            return 1
    except SpiNNakerBootError as e:
        # The machine could not be booted for some reason; show an appropriate
        # message
        sys.stderr.write("{}: error: {}\n".format(parser.prog, str(e)))
        return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
