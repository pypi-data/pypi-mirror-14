import os
import time
import shutil
import warnings
from datetime import datetime

import spec  # type: ignore

import tryp
from tryp.logging import tryp_stdout_logging
from tryp.test.sure_ext import install_assertion_builder, AssBuilder
from tryp.test import path


def later(ass, timeout=1, intval=0.1):
    start = datetime.now()
    ok = False
    while not ok and (datetime.now() - start).total_seconds() < timeout:
        try:
            ass()
            ok = True
        except AssertionError:
            time.sleep(intval)
    return ass()


class Spec(spec.Spec):

    def __init__(self):
        self._warnings = True

    def setup(self):
        if path.__base_dir__:
            shutil.rmtree(str(path.temp_path()), ignore_errors=True)
        if self._warnings:
            warnings.resetwarnings()
        tryp.development = True
        tryp_stdout_logging()
        install_assertion_builder(AssBuilder)

    def teardown(self, *a, **kw):
        warnings.simplefilter('ignore')

    def _wait_for(self, pred, timeout=5, intval=0.1):
        start = datetime.now()
        while (not pred() and
               (datetime.now() - start).total_seconds() < timeout):
            time.sleep(intval)
        pred().should.be.ok

    def _wait(self, seconds):
        time.sleep(seconds)


class IntegrationSpec(Spec):

    def setup(self):
        os.environ['TRYP_INTEGRATION'] = '1'
        tryp.integration_test = True
        super().setup()

__all__ = ('Spec', 'IntegrationSpec')
