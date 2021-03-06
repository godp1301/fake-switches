# Copyright 2015 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from fake_switches.command_processing.shell_session import \
    ShellSession
from fake_switches.brocade.command_processor.piping import \
    PipingProcessor
from fake_switches.brocade.brocade_core import BrocadeSwitchCore
from fake_switches.dell.command_processor.default import \
    DellDefaultCommandProcessor
from fake_switches.terminal import LoggingTerminalController


class DellSwitchCore(BrocadeSwitchCore):
    def launch(self, protocol, terminal_controller):
        self.last_connection_id += 1
        self.logger = logging.getLogger("fake_switches.dell.%s.%s.%s" % (self.switch_configuration.name, self.last_connection_id, protocol))

        command_processor = DellDefaultCommandProcessor(
            switch_configuration=self.switch_configuration,
            terminal_controller=LoggingTerminalController(self.logger, terminal_controller),
            piping_processor=PipingProcessor(self.logger),
            logger=self.logger)

        return DellShellSession(command_processor)


class DellShellSession(ShellSession):
    def handle_unknown_command(self, line):
        self.command_processor.terminal_controller.write("          ^\n")
        self.command_processor.terminal_controller.write("% Invalid input detected at '^' marker.\n")
        self.command_processor.terminal_controller.write("\n")
