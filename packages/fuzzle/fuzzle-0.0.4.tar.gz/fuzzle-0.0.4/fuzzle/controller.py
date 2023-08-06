import json

from fuzzle.exceptions import UnexpectedTypeError, FuzzleError
from fuzzle.lvars import InputLVar, OutputLVar
from fuzzle.rules import RuleBlock


class FuzzyController:
    """Fuzzy controller."""

    def __init__(self, input_vars, output_vars, rule_block):
        """ Initializes this fuzzy controller.

        :param input_vars: the set of input variables available for this
            controller.
        :param output_vars: the set of output variables available for this
            controller.
        :param rule_block: the rule block with all the rules.

        """
        if not all(isinstance(lvar, InputLVar) for lvar in input_vars):
            msg = 'Input vars must be {} instances'.format(InputLVar.__name__)
            raise FuzzleError(msg)
        if not all(isinstance(lvar, OutputLVar) for lvar in output_vars):
            msg = 'Output vars must be {} instances'.format(OutputLVar.__name__)
            raise FuzzleError(msg)
        if not isinstance(rule_block, RuleBlock):
            raise UnexpectedTypeError('rule_block', RuleBlock)

        self.__rule_block = rule_block

        self.__i_vars = dict([(var.name, var) for var in input_vars])
        self.__o_vars = dict([(var.name, var) for var in output_vars])

        self.__output = dict([(var.name, 0.) for var in output_vars])

    def eval(self, c_input):
        """ Evaluates an input returning the output according the controller.

        Given a crisp input in the form:
        {
            'input_lvar_1': val_1,
             ...,
            'input_lvar_n': val_n
        }
        the method will return a crisp output in the form
        {
            'output_lvar_1': val1,
            ...,
            'output_lvar_n':val_n
        }
        after being processed by the controller.

        :param c_input: a crisp input.
        """
        return self.__defuzzify(self.__infer(self.__fuzzify(c_input)))

    def __fuzzify(self, c_input):
        fuzzy_input = {}
        for var in self.__i_vars:
            fuzzy_input[var] = self.__i_vars[var].fuzzify(c_input[var])
        return fuzzy_input

    def __infer(self, f_input):
        return self.__rule_block.eval(f_input, self.__o_vars)

    def __defuzzify(self, f_output):
        c_output = {}
        for var in self.__o_vars:
            if var in f_output:
                c_value = self.__o_vars[var].defuzzify(f_output[var])
                c_output[var] = self.__output[
                    var] if c_value is None else c_value
            else:
                c_output[var] = self.__output[var]
        self.__output = c_output
        return c_output

    def as_json(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        return {
            'in': {k: v.as_dict() for k, v in self.__i_vars.items()},
            'out': {k: v.as_dict() for k, v in self.__o_vars.items()},
            'rb': self.__rule_block.as_dict(),
        }

    def __str__(self):
        return '{0}\n{1}'.format(self.__i_vars.values(), self.__o_vars.values())
