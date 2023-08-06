#!/usr/bin/env python
#
# This file is part of Script of Scripts (SoS), a workflow system
# for the execution of commands and scripts in different languages.
# Please visit https://github.com/bpeng2000/SOS for more information.
#
# Copyright (C) 2016 Bo Peng (bpeng@mdanderson.org)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# passing string as unicode to python 2 version of SoS
# to ensure compatibility
from __future__ import unicode_literals

import os
import unittest

from pysos import *
from pysos.utils import env

class TestActions(unittest.TestCase):
    def setUp(self):
        env.run_mode = 'run'

    def testSoSAction(self):
        '''Test sos_action decorator'''
        script = SoS_Script(r"""
from pysos import SoS_Action

@SoS_Action(run_mode='dryrun')
def func_dryrun():
    return 1

@SoS_Action(run_mode='run')
def func_run():
    return 1

@SoS_Action(run_mode=['run', 'dryrun'])
def func_both():
    return 1

[0:alias='result']
a=func_dryrun()
b=func_run()
c=func_both()
""")
        wf = script.workflow()
        env.run_mode = 'dryrun'
        wf.run()
        self.assertEqual(env.sos_dict['result'].a, 1)
        self.assertEqual(env.sos_dict['result'].b, 0)
        self.assertEqual(env.sos_dict['result'].c, 1)
        #
        env.run_mode = 'run'
        wf.run()
        self.assertEqual(env.sos_dict['result'].a, 0)
        self.assertEqual(env.sos_dict['result'].b, 1)
        self.assertEqual(env.sos_dict['result'].c, 1)

    def testCheckCommand(self):
        '''Test action check_command'''
        script = SoS_Script(r"""
[0]
check_command('cat')
""")
        wf = script.workflow()
        # should be ok
        wf.run()
        #
        script = SoS_Script(r"""
[0]
check_command('catmouse')
""")
        env.run_mode = 'dryrun'
        wf = script.workflow()
        # should fail in dryrun mode
        self.assertRaises(RuntimeError, wf.run)
        #
        env.run_mode = 'run'
        wf = script.workflow()
        # should fail also in run mode
        self.assertRaises(RuntimeError, wf.run)
        #
        # should also check command with option
        script = SoS_Script(r"""
[0]
check_command('ls -l')
""")
        wf = script.workflow()
        # this should pass
        wf.run()
        #
        script = SoS_Script(r"""
[0]
fail_if(check_command('cat -h') != 0, 'command return non-zero')
""")
        wf = script.workflow()
        # this should give a warning and return false
        self.assertRaises(RuntimeError, wf.run)
        #
        # check check_command is the command is stuck
        env.run_mode = 'dryrun'
        script = SoS_Script(r"""
[0]
check_command('sleep 4')
""")
        wf = script.workflow()
        # this should pass
        wf.run()
        #
        script = SoS_Script(r"""
[0]
fail_if(check_command('sleep 4') != 0, 'Command time out')
""")
        wf = script.workflow()
        # this should pass
        self.assertRaises(RuntimeError, wf.run)
        # test reading this file
        script = SoS_Script(r"""
[0]
check_command('cat test_actions.py', 'abcde' + 'fgh')
""")
        wf = script.workflow()
        # should raise an error
        self.assertRaises(RuntimeError, wf.run)
        #
        script = SoS_Script(r"""
check_command('cat test_actions.py', 'testSearchOutput')
""")
        wf = script.workflow()
        wf.run()

    def testFailIf(self):
        '''Test action fail if'''
        script = SoS_Script(r"""
[0]
input: 'a.txt'
fail_if(len(input) == 1)
""")
        env.run_mode = 'dryrun'
        wf = script.workflow()
        # should fail in dryrun mode
        self.assertRaises(RuntimeError, wf.run)
        script = SoS_Script(r"""
[0]
input: 'a.txt', 'b.txt'
fail_if(len(input) == 1)
""")
        env.run_mode = 'dryrun'
        wf = script.workflow()
        # should be ok
        wf.run()

    def testWarnIf(self):
        '''Test action fail if'''
        script = SoS_Script(r"""
[0]
input: 'a.txt'
warn_if(len(input) == 1, 'Expect to see a warning message')
""")
        env.run_mode = 'dryrun'
        wf = script.workflow()
        # should see a warning message.
        wf.run()
        #self.assertRaises(RuntimeError, wf.run)
        script = SoS_Script(r"""
[0]
input: 'a.txt', 'b.txt'
warn_if(len(input) == 1)
""")
        env.run_mode = 'dryrun'
        wf = script.workflow()
        # should be silent
        wf.run()

    def testRun(self):
        '''Test action run'''
        script = SoS_Script(r'''
[0]
run:
echo 'Echo'
''')
        wf = script.workflow()
        wf.run()
        script = SoS_Script(r'''
[0]
run:
echo 'Echo
''')
        wf = script.workflow()
        self.assertRaises(RuntimeError, wf.run)

    def testBash(self):
        '''Test action run'''
        script = SoS_Script(r'''
[0]
bash:
echo 'Echo'
''')
        wf = script.workflow()
        wf.run()
        script = SoS_Script(r'''
[0]
bash:
echo 'Echo
''')
        wf = script.workflow()
        self.assertRaises(RuntimeError, wf.run)
        # docker
        script = SoS_Script(r'''
[0]
bash:  docker_image='ubuntu'
echo 'Echo'
''')
        wf = script.workflow()
        wf.run()


    def testSh(self):
        '''Test action run'''
        script = SoS_Script(r'''
[0]
sh:
echo 'Echo'
''')
        wf = script.workflow()
        wf.run()
        script = SoS_Script(r'''
[0]
sh:
echo 'Echo
''')
        wf = script.workflow()
        self.assertRaises(RuntimeError, wf.run)
        # test docker
        script = SoS_Script(r'''
[0]
sh: docker_image='ubuntu'
echo 'Echo
''')
        wf = script.workflow()
        # FIXME: syntax error is not reflected outside of the docker
        self.assertRaises(RuntimeError, wf.run)

    def testCsh(self):
        '''Test action csh'''
        script = SoS_Script(r'''
[0]
csh:
    foreach file (*)
        if (-d $file) then
            echo "Skipping $file (is a directory)"
        else
            echo "Echo $file"
            echo $file
        endif
    end
''')
        wf = script.workflow()
        wf.run()
        # no test for docker because standard distributions do not have csh

    def testTcsh(self):
        '''Test action tcsh'''
        script = SoS_Script(r'''
[0]
csh:
    foreach file (*)
        if (-d $file) then
            echo "Skipping $file (is a directory)"
        else
            echo "Echo $file"
            echo $file
        endif
    end
''')
        wf = script.workflow()
        wf.run()
        # no test for docker because standard distributions do not have tcsh

    def testZsh(self):
        '''Test action zsh'''
        script = SoS_Script(r'''
[0]
zsh:
echo "Hello World!", $SHELL
''')
        wf = script.workflow()
        wf.run()
        # cannot test in docker because no first-tier repository
        # provides zsh.

    def testPython(self):
        '''Test python command. This might fail if python3 is the
        default interpreter'''
        script = SoS_Script(r'''
[0]
python:
a = {'1': 2}
print(a)
''')
        wf = script.workflow()
        wf.run()
        # test docker
        script = SoS_Script(r'''
[0]
python:  docker_image='python'
a = {'1': 2}
print(a)
''')
        wf = script.workflow()
        wf.run()

    def testPython3(self):
        script = SoS_Script(r'''
[0]
python3:
a = {'1', '2'}
print(a)
''')
        wf = script.workflow()
        wf.run()
        # test docker
        script = SoS_Script(r'''
[0] 
python3: docker_image='python'
#!/usr/bin/env python3
a = {'1', '2'}
print(a)
''')
        wf = script.workflow()
        wf.run()

    def testPerl(self):
        '''Test action ruby'''
        script = SoS_Script(r'''
[0]
perl:
use strict;
use warnings;

print "hi NAME\n";
''')
        wf = script.workflow()
        wf.run()
        # test docker
        script = SoS_Script(r'''
[0]
perl: docker_image='ubuntu'
use strict;
use warnings;

print "hi NAME\n";
''')
        wf = script.workflow()
        wf.run()


    def testRuby(self):
        '''Test action ruby'''
        script = SoS_Script(r'''
[0]
ruby:
line1 = "Cats are smarter than dogs";
line2 = "Dogs also like meat";

if ( line1 =~ /Cats(.*)/ )
  puts "Line1 contains Cats"
end
if ( line2 =~ /Cats(.*)/ )
  puts "Line2 contains  Dogs"
end
''')
        wf = script.workflow()
        wf.run()
        # test docker
        script = SoS_Script(r'''
[0]
ruby: docker_image='ruby'
line1 = "Cats are smarter than dogs";
line2 = "Dogs also like meat";

if ( line1 =~ /Cats(.*)/ )
  puts "Line1 contains Cats"
end
if ( line2 =~ /Cats(.*)/ )
  puts "Line2 contains  Dogs"
end
''')
        wf = script.workflow()
        wf.run()

    def testNode(self):
        '''Test action ruby'''
        script = SoS_Script(r'''
[0]
node:
var args = process.argv.slice(2);
console.log('Hello ' + args.join(' ') + '!');
''')
        wf = script.workflow()
        wf.run()
        # test docker
        script = SoS_Script(r'''
[0]
node: docker_image='node'

var args = process.argv.slice(2);
console.log('Hello ' + args.join(' ') + '!');
''')
        wf = script.workflow()
        wf.run()


    def testJavaScript(self):
        '''Test action JavaScript'''
        script = SoS_Script(r'''
[0]
JavaScript:
var args = process.argv.slice(2);
console.log('Hello ' + args.join(' ') + '!');
''')
        wf = script.workflow()
        wf.run()
        # test docker
        script = SoS_Script(r'''
[0]
JavaScript: docker_image='node'

var args = process.argv.slice(2);
console.log('Hello ' + args.join(' ') + '!');
''')
        wf = script.workflow()
        wf.run()

    def testR(self):
        '''Test action JavaScript'''
        script = SoS_Script(r'''
[0]
R:
nums = rnorm(25, mean=100, sd=15)
mean(nums)
''')
        wf = script.workflow()
        wf.run()
        # test docker
        script = SoS_Script(r'''
[0]
R: docker_image='r-base'
nums = rnorm(25, mean=100, sd=15)
mean(nums)
''')
        wf = script.workflow()
        wf.run()

    def testCheckRLibrary(self):
        '''Test action check_R_library'''
        script = SoS_Script(r'''
[0]
check_R_library('edgeR')
''')
        wf = script.workflow()
        wf.run()
        script = SoS_Script(r'''
[0]
check_R_library('stephens999/ashr')
''')
        wf = script.workflow()
        wf.run()
        script = SoS_Script(r'''
[0]
check_R_library('edgeRRRR')
''')
        wf = script.workflow()
        self.assertRaises(RuntimeError, wf.run)

    def testDockerBuild(self):
        '''Test action docker build'''
        script = SoS_Script(r'''
[0]
docker_build:  tag='test/docker_build'
#
# Super simple example of a Dockerfile
#
FROM ubuntu:latest
MAINTAINER Andrew Odewahn "odewahn@oreilly.com"

RUN apt-get update
RUN apt-get install -y python python-pip wget
RUN pip install Flask

WORKDIR /home
''')
        wf = script.workflow()
        wf.run()


    def testDockerImage(self):
        '''Test docker_image option'''
        script = SoS_Script(r'''
[0]
fastq_files = glob.glob('data/*.fastq')
input_volume = os.path.dirname(fastq_files[0])
output_volume = os.getcwd()

run: docker_image='compbio/ngseasy-fastqc:1.0-r001', 
    docker_volumes=['${input_volume}:/input_data', '${output_volume}:/output_data']

    ls -l /input_data
    /usr/local/bin/fastqc /input_data/*.fastq --outdir /output_data
''')
        wf = script.workflow()
        wf.run()

    def testDockerImageFromFile(self):
        '''Test docker_image load from a file.'''
        # image from a saved file
        script = SoS_Script(r'''
[0]
run:   docker_image='hello-world'

[1]
run:
    docker save hello-world > hello.tar
    docker rmi -f hello-world

[2]
run: docker_image='hello-world', docker_file = 'hello.tar'
''')
        wf = script.workflow()
        wf.run()



if __name__ == '__main__':
    unittest.main()
