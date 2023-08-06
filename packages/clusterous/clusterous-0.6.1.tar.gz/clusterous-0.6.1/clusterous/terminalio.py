# Copyright 2015 Nicta
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

import textwrap
import readline     # to support raw_input

def boldify(s):
    """
    Adds shell formatting characters to s to make it bold when printed
    """
    return '\033[1m' + str(s) + '\033[0m'

class WizardIO:
    @staticmethod
    def out(text, indent=0, error=False, init_str='', bold=False, new_line=True, question=False):
        out = WizardIO._fmt_text(text, indent, error, init_str, bold)
        
        print out, 
        if new_line:
            print

    @staticmethod
    def plain_out(text):
        print text

    @staticmethod
    def ask(prompt):
        text = '* ' + WizardIO._fmt_text(prompt, question=True) + ' '
        return raw_input(text).strip()

    @staticmethod
    def new_para():
        print

    @staticmethod    
    def _fmt_text(text, indent=0, error=False, init_str='', bold=False, question=False):
        initial_str, subsequent_str = '', ''
        if init_str:
            initial_str = init_str
        elif indent > 0:
            initial_str = ' '*4
            subsequent_str = initial_str

        out = textwrap.fill(text, width=70, initial_indent=initial_str, subsequent_indent=subsequent_str,
                            break_on_hyphens=False)

        if bold:
            out = WizardIO._apply_heading_fmt(out)
        
        if error:
            out = WizardIO._apply_error_fmt(out)

        if question:
            out = WizardIO._apply_question_fmt(out)

        return out

    @staticmethod
    def _apply_error_fmt(text):
        return '\033[91m' + text + '\033[0m'

    @staticmethod
    def _apply_question_fmt(text):
        return '\033[4m' + text + '\033[0m'

    @staticmethod
    def _apply_heading_fmt(text):
        return '\033[1m' + text + '\033[0m'