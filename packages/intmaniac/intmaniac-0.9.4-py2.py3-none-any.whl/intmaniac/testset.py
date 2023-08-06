#!/usr/bin/env python

from intmaniac.testrun import Testrun
from intmaniac.tools import deep_merge
from intmaniac import output

import logging as log


class Testset(object):

    def __repr__(self):
        return "<Testset '%s'>" % self.name

    def __init__(self, name, global_config={}):
        self.name = name
        self.log = log.getLogger("ts-%s" % self.name)
        self.log.debug("Instantiated")
        self.tests = []
        self.global_config = global_config if global_config else {}
        self.failed_tests = []
        self.succeeded_tests = []
        self.success = True

    def set_global_config(self, global_config=None):
        if global_config:
            self.global_config = global_config

    def add_from_config(self, name, config):
        test_name = "%s-%s" % (self.name, name)
        test_conf = deep_merge(self.global_config, config)
        self.tests.append(Testrun(test_name, test_conf))

    def succeeded(self):
        return self.success

    def run(self):
        for test in self.tests:
            self.log.debug("starting test <%s>" % test.name)
            test.run()
            if test.succeeded():
                self.succeeded_tests.append(test)
            else:
                self.failed_tests.append(test)
                self.success = False
        self.log.warning("testset successful" if self.success else "testset FAILED")
        return self.success

    def dump(self):
        output.output.test_suite_open(self.name)
        for test in self.tests:
            test.dump()
        output.output.test_suite_done()

if __name__ == "__main__":
    print("Don't do this :)")
