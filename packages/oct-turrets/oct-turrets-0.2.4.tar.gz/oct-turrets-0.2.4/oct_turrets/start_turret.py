import os
import logging
import tarfile
import argparse
from oct_turrets.turret import Turret
from oct_turrets.exceptions import InvalidConfiguration
from oct_turrets.utils import validate_conf, extract_tarfile, clean_tar_tmp, load_file

log = logging.getLogger(__name__)


def start():

    parser = argparse.ArgumentParser(description='Give parameters for start a turret instance')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--config-file', type=str, default='', help='path for config_file')
    group.add_argument('--tar', type=str, default='', help='Path for the tarball')
    args = parser.parse_args()

    if args.config_file == '' and args.tar == '':
        parser.error('You need a config_file.json to start a turret')

    from_tar = False
    if args.tar != '':
        from_tar = True
        if not tarfile.is_tarfile(args.tar):
            log.error("Invalid tar file provided")
            return None
        with tarfile.open(args.tar) as tar:
            config_file = extract_tarfile(tar, 'config.json')
            try:
                config = validate_conf(config_file)
            except InvalidConfiguration:
                clean_tar_tmp()
                log.error("you need a valid config.json or a valid tar archive")
                return None
            module_file = extract_tarfile(tar, config['script'])
    elif args.config_file != '' and os.path.isfile(args.config_file):
        config_file = args.config_file
        config = validate_conf(config_file)
        cfg_path = os.path.dirname(config_file)
        module_file = os.path.join(cfg_path, config['script'])
    else:
        log.error("you need a valid config.json or a valid tar archive")
        return None

    module = load_file(module_file)

    if from_tar:
        clean_tar_tmp(config)

    turret = Turret(config, module)
    turret.start()
