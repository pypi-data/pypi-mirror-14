#!/usr/bin/python
__author__ = 'Jiri_Kulda'

import re
import shlex
import bkrdoc.analysis
import sys


class PhaseOutside:
    """Class for searching data outside of phases"""
    phase_name = ""
    statement_list = []
    variables = ""
    func_list = []

    def __init__(self):
        # self.parse_ref = parse_cmd
        self.phase_name = "Outside phase"
        self.statement_list = []
        self.variables = bkrdoc.analysis.TestVariables()
        self.func_list = []

    def setup_statement(self, line):
        self.statement_list.append(line)

    def search_data(self, variable_copy, function_copy):
        """
        This method searches variables in statements. Also when it finds function then this method
        created TestFunction object with function data.
        :param variable_copy: Copy of variables
        :param function_copy: Copy of functions
        """
        self.variables = variable_copy
        self.func_list = function_copy
        func = False
        for statement in self.statement_list:

            # These three conditions are here because of getting further
            # information from functions.
            if self.is_function(statement):
                func = True
                self.func_list.append(bkrdoc.analysis.TestFunction(statement[len("function")+1:]))

            elif func and not self.is_function_end(statement):
                self.func_list[-1].add_line(statement)

            elif func and self.is_function_end(statement):
                self.func_list[-1].add_line(statement)
                func = False

            else:
                # searching variables in statement line
                try:
                    read = shlex.shlex(statement)
                    member = read.get_token()
                    equal_to = read.get_token()

                    while equal_to:
                    # condition to handle assign to random value
                    # setting variable list
                        if equal_to == '=':
                        # These 7 lines are here for erasing comments and for reading whole line
                            pom_i = statement.find("=", len(member)) + 1
                            list_of_statement = shlex.split(statement[pom_i:], True, True)
                            value = ""
                            for value_member in list_of_statement:
                                if not value == "":
                                    value += " "
                                value += value_member

                            regular = re.compile("\"(/.*/)(.*)\"")
                            match = regular.match(value)
                            if match:
                                self.variables.add_variable(member, match.group(1) + match.group(2))
                                self.variables.add_keyword(match.group(2))
                            else:
                                self.variables.add_variable(member, value)

                        member = equal_to
                        equal_to = read.get_token()
                except ValueError as detail:
                    print("ERROR in line: " + str(statement))
                    print("With message: " + str(detail))

    def is_function(self, line):
        return line[0:len("function")] == "function"

    def is_function_end(self, line):
        """
        Test end of line of function in statement line
        :param line: statement line
        :return: true or false
        """
        if line[0:1] == "}":
            return True
        else:
            # This split for erasing comments on the end of line
            pom_list = shlex.split(line, True, True)
            if pom_list[-1][-1] == "}":
                return True
            else:
                return False


class PhaseContainer:
    """Class for storing information in test phase"""
    phase_name = ""
    statement_list = []
    doc_ref = ""
    variables = ""
    statement_classes = []
    documentation_units = []
    phase_documentation_information = []
    func_list = []
    generator_ref = ""

    def __init__(self, name):
        self.phase_name = name
        self.statement_list = []
        self.doc = []
        self.variables = bkrdoc.analysis.TestVariables()
        self.statement_classes = []
        self.documentation_units = []
        self.phase_documentation_information = []
        self.func_list = []
        self.generator_ref = ""

    def setup_statement(self, line):
        self.statement_list.append(line)

    def search_data(self, generator_ref, variable_copy, function_copy):
        """
        This method runs data searching in statement lines.
        :param generator_ref: parser object reference
        :param variable_copy: variable copy
        :param function_copy: function copy
        """
        self.func_list = function_copy
        self.variables = variable_copy
        self.generator_ref = generator_ref
        command_translator = bkrdoc.analysis.StatementDataSearcher()
        for statement in self.statement_list:
            try:
                replaced_statement_variables = self.variables.replace_variable_in_string(statement)
                self.get_cmd_line_params(replaced_statement_variables)
                self.get_environmental_variable(replaced_statement_variables)
                argparse_data, pom_variables = command_translator.parse_command(replaced_statement_variables)
                self.variables.copy_variables_from_variable_class(pom_variables)
                self.statement_classes.append(argparse_data)
            except ValueError:
                sys.stdout.write("********************************************")
                print("ERROR in line: " + str(statement))
                print(ValueError)
                print("********************************************")
            except SystemExit:
                sys.stdout.write("********************************************")
                print("ERROR in line: " + str(statement))
                print("Can be problem with variables substitutions")
                print("********************************************")

    def search_data_in_function(self, function):
        """
        Searching data in function object
        :param function: function object
        """
        command_translator = bkrdoc.analysis.StatementDataSearcher()
        function.data_list = []
        for statement in function.statement_list:
            try:
                function.add_data(command_translator.parse_command(statement))
            except ValueError:
                sys.stdout.write("********************************************")
                print("ERROR in line: " + str(statement))
                print(ValueError)
                print("********************************************")
            except SystemExit:
                sys.stdout.write("********************************************")
                print("ERROR in line: " + str(statement))
                print("Can be problem with variables substitutions")
                print("********************************************")

    def translate_data(self, parser_ref):
        """
        Translate data from argparse object to DocumentationInformation object
        :param parser_ref: parser reference
        """
        data_translator = bkrdoc.analysis.DocumentationTranslator(parser_ref)
        for data in self.statement_classes:
            if data.argname != "UNKNOWN":
                self.documentation_units.append(data_translator.translate_data(data))

    def generate_documentation(self):
        """
        Transforms DocumentationInformation into small classes using GetInformation
        """
        information_translator = bkrdoc.analysis.GetInformation()
        for information in self.documentation_units:
            if information:
                self.phase_documentation_information.append(information_translator.get_information_from_facts(information))

    def print_phase_documentation(self, cmd_options):
        """
        Prints nature language information
        :param cmd_options: possible command line options
        """
        self.print_phase_name_with_documentation_credibility()
        conditions = bkrdoc.analysis.ConditionsForCommands()

        for information in self.phase_documentation_information:
            if cmd_options.log_in or cmd_options.print_all:
                information.print_information()
            elif not conditions.is_rllog_command(information.get_command_name()):
                information.print_information()

    def print_phase_name_with_documentation_credibility(self):
        inf = self.phase_name + " [Unknown commands: " + str(self.get_unknown_commands()) \
                              + ", Total: " + str(self.get_total_commands()) \
                              + ", Documentation credibility: " + self.get_phase_credibility().get_credibility() + "]"
        print(inf)

    def get_information_list(self):
        return self.phase_documentation_information

    def set_information_list(self, inf_list):
        """
        Sets whole information list. This method is called after solving knapsack problem.
        :param inf_list: list of information from finished knapsack algorithm
        """
        self.phase_documentation_information = inf_list

    def get_phase_weigh(self):
        """
        this method returns number of lines on which information will be printed

        :return: -//-
        """
        phase_weigh = 0
        for inf in self.phase_documentation_information:
            phase_weigh += inf.get_information_weigh()
        return phase_weigh

    def get_cmd_line_params(self, line):
        """
        This method searches for command line variables in code represented as $1 $2 ...
        :param line: statement line of code
        """
        regular = re.compile("(.*)(\$(\d+))(.*)")
        match = regular.match(line)
        if match:
            self.generator_ref.set_test_launch(match.group(3))

    def get_environmental_variable(self, line):
        """
        Searches environmental variables in code line
        :param line: code line
        """
        minimum_variable_size = 4
        lexer = shlex.shlex(line)
        word = lexer.get_token()
        while word:
            if word == "$":
                word = lexer.get_token()
                if not self.variables.is_existing_variable(word) and len(word) > minimum_variable_size:
                    self.generator_ref.set_environmental_variable_information(word)

            elif word[0:1] == '"':  # shlex doesn't returns whole string so for searching in strings I'm using recursion
                self.get_environmental_variable(word[1:-1])
            word = lexer.get_token()

    def get_function_list(self):
        """
        :return: list of functions
        """
        return self.func_list

    def get_phase_credibility(self):
        Credibility = bkrdoc.analysis.credibility.DocumentationCredibility
        return Credibility(self.get_unknown_commands(), self.get_total_commands())

    def get_total_commands(self):
        return len(self.statement_list)

    def get_unknown_commands(self):
        Par = bkrdoc.analysis.bkrdoc_parser.Parser
        return sum(st.partition(' ')[0] not in Par.all_commands for st in self.statement_list)
