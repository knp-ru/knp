import os

from attacker import AttackRunner
import sys

DEFAULT_CONFIG_FILE = "./normal.config.yaml"

if __name__ == '__main__':
    # config_file = sys.argv[1] if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else DEFAULT_CONFIG_FILE
    config_file = "./attack.config.yaml"
    attack_runner = AttackRunner(config_file)
    attack_runner.run_attack()
