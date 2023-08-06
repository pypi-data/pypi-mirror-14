import os
import unittest

import ConfigSpace
import ConfigSpace.util
import ConfigSpace.io.pcs as pcs_parser


class ExampleSearchSpacesTest(unittest.TestCase):
    pass


def generate(configuration_space_path):
    def run_test(self):
        if 'autoweka' in configuration_space_path:
            return
        with open(configuration_space_path) as fh:
            cs = pcs_parser.read(fh)

        # Sample a little bit
        for i in range(10):
            print(i)
            cs.seed(i)
            configurations = cs.sample_configuration(size=10)
            for j, c in enumerate(configurations):
                print(j)
                c.is_valid_configuration()
                neighborhood = ConfigSpace.util.get_one_exchange_neighbourhood(
                    c, seed=i)
                for n in neighborhood:
                    n.is_valid_configuration()

    return run_test


this_file = os.path.abspath(__file__)
this_directory = os.path.dirname(this_file)
configuration_space_path = os.path.join(this_directory,
                                        "..", "test_searchspaces")
configuration_space_path = os.path.abspath(configuration_space_path)
pcs_files = os.listdir(configuration_space_path)

for pcs_file in pcs_files:
    if '.pcs' in pcs_file:
        full_path = os.path.join(configuration_space_path, pcs_file)
        setattr(ExampleSearchSpacesTest, 'test_%s' % pcs_file.replace('.', '_'),
                generate(full_path))
