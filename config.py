import os

import sentry_sdk
import yaml

config = yaml.safe_load(open(os.path.dirname(__file__) + '/config.yml'))
sentry_sdk.init(config['sentry']['dsn'], traces_sample_rate=config['sentry']['rate'])
