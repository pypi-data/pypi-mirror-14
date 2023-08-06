import collections
import re

from fuzzle import mfs
from fuzzle import operators
from fuzzle.exceptions import FuzzleError, ParseError


class RuleBlock(dict):
    """ Contains all the rules of the inference engine. """

    def __init__(self,
                 and_op=operators.Minimum(),
                 or_op=operators.Maximum(),
                 not_op=operators.Zadeh(),
                 agg_op=operators.AlgebraicProduct(),
                 acc_op=operators.AlgebraicSum()):
        """ Initializes this rule block.

        :param and_op: the AND operator. Defaults to the minimum t-norm.
        :param or_op: the OR operator. Defaults to the maximum s-norm
        :param not_op: the NOT operator. Defaults to Zadeh's complement.
        :param agg_op: the aggregator operator (related with THEN operator).
            Defaults to algebraic product t-norm.
        :param acc_op: the accumulation operator. Defaults to algebraic sum
            s-norm.
        """
        super().__init__()

        self.and_op = and_op
        self.or_op = or_op
        self.not_op = not_op
        self.agg_op = agg_op
        self.acc_op = acc_op

        self.__rule_parser = RuleParser(and_op, or_op, not_op)

    def eval(self, finput, ovars):
        """ Evaluates a fuzzy input.

        Evaluates one by one the rules contained in this rules block against
        the fuzzy inputs and the definition of the output linguistic variables.

        :param finput: the fuzzy input.
        :param ovars: the fuzzy output.

        :returns: the fuzzy output, i.e. the membership function for all the
            output variables which appears in the rules after evaluating them.
        """
        # Evaluation
        rules_output = [rule.eval(finput) for rule in self.values()]

        # Aggregation (only those output vars whose value is greater than 0)
        agg_mf = collections.defaultdict(lambda: [])
        for output in rules_output:
            for o_var, f_set, val in output:
                if val:
                    agg_mf[o_var].append(
                            mfs.BinOpMF(
                                    self.agg_op,
                                    mfs.ConstantMF(val),
                                    ovars[o_var][f_set]
                            )
                    )

        # Accumulation
        foutput = {}
        for o_var in agg_mf:
            acc_mf = None
            for mf in agg_mf[o_var]:
                if acc_mf is None:
                    acc_mf = mf
                else:
                    acc_mf = mfs.BinOpMF(self.acc_op, acc_mf, mf)
            foutput[o_var] = acc_mf

        return foutput

    def as_dict(self):
        return {
            'and': str(self.and_op),
            'or': str(self.or_op),
            'not': str(self.not_op),
            'agg': str(self.agg_op),
            'acc': str(self.acc_op),
            'rules': {k: str(v) for (k, v) in self.rules.items()}
        }

    def __setitem__(self, name, rule):
        if name in self:
            raise FuzzleError('Rule {} exists in ruleblock'.format(name))

        super().__setitem__(name, self.__rule_parser.parse(rule))


class RuleParser:
    """ A parser to process fuzzy rules. """
    PATTERNS = '''
        (?P<if>if|IF)
        |(?P<then>then|THEN)
        |(?P<with>with|WITH)
        |(?P<open_parenthesis>[(])
        |(?P<close_parenthesis>[)])
        |(?P<comma>[,])
        |(?P<blank>[\s|\n]+)
        |(?P<is>is|IS)
        |(?P<not>not|NOT)
        |(?P<logical_op>and|or|AND|OR)
        |(?P<hedge>very|fairly|VERY|FAIRLY)
        |(?P<literal>[a-zA-Z_][a-zA-Z0-9_]*)
        |(?P<decimal>[-+]?(\d*)\.?(\d+))
    '''

    def __init__(self, and_op, or_op, complement_op):
        self.and_op = and_op
        self.or_op = or_op
        self.complement_op = complement_op

        self.tokens = []

    def tokenize(self, value):
        compiler = re.compile(self.PATTERNS, re.VERBOSE)
        tokens = []
        pos = 0
        while True:
            m = compiler.match(value, pos)
            if m:
                pos = m.end()
                token_name = m.lastgroup
                token_value = m.group(token_name)
                tokens.append((token_name, token_value))
            else:
                break
        if pos != len(value):
            raise SyntaxError('Syntax error at position {0}'.format(pos))
        else:
            tokens = list(filter(lambda t: t[0] != 'blank', tokens))
            tokens.reverse()
            return tokens

    def head(self, x):
        """ Checks if the next token of tokens is of a specified class.

        Given a class, the method will return whether or not the next element of
        the tokens stack is of the specified class. If there are no elements,
        then the method will return false.

        When head is called, the stack will not be modified.

        :param x: the class to check.
        :type x: str

        :returns: If the next item is or not of the specified class.
        :rtype: bool
        """
        if self.tokens:
            token_type, token_value = self.tokens[len(self.tokens) - 1]
            return token_type == x
        else:
            return False

    def pop(self, x):
        """ Extracts the next element from the stack iff belongs to a specified
        class.

        Given a class, the method will return the next element of the stack iff
        that element belongs to the specified class. In that's not the case, the
        method will fail and an error will be raised.

        When pop is called, the stack will be modified, removing the top element
        of the stack.

        :param x: the class to check.
        :type x: str

        :returns: the element on the top of the stack.
        :rtype: str

        :raises: SyntaxError
        """
        if len(self.tokens) > 0:
            token_type, token_value = self.tokens.pop()
            if token_type != x:
                raise ParseError(x, token_type, token_value)
            else:
                return token_value
        else:
            raise SyntaxError('Illegal end of rule')

    def parse(self, rule):
        """ Parses a rule in string form.

        Translates string rule (e.g "IF Speed IS High THEN Brake IS On") to a
        object Rule.

        :param rule: a rule in string format
        :type rule: str

        :returns: the rule as an instance of Rule.
        :rtype: Rule
        """
        self.tokens = self.tokenize(rule)

        return self.__parse_rule(rule)

    def __parse_rule(self, rule):
        self.pop('if')
        antecedent = self.__parse_antecedent()
        self.pop('then')
        consequent = self.__parse_consequent()
        if self.head('with'):
            self.pop('with')
            weight = self.__parse_weight()
        else:
            weight = 1.0

        return Rule(rule, antecedent, consequent, weight)

    def __parse_antecedent(self):
        if self.head('open_parenthesis'):
            self.pop('open_parenthesis')
            antecedent = self.__parse_antecedent()
            self.pop('close_parenthesis')
        elif self.head('not'):
            self.pop('not')
            antecedent = UnaryOpAntecedent(self.complement_op,
                                           self.__parse_antecedent())
        else:
            antecedent = self.__parse_antecedent_statement()

        if self.head('logical_op'):
            op_str = self.pop('logical_op').lower()
            if op_str == 'and':
                op = self.and_op
            elif op_str == 'or':
                op = self.or_op
            else:
                raise ParseError('logical_op', op_str)

            return BinaryOpAntecedent(op, antecedent, self.__parse_antecedent())
        else:
            return antecedent

    def __parse_antecedent_statement(self):
        l_var, negat, hedge, f_set = self.__parse_statement()
        statement = StatementAntecedent(l_var, f_set)
        return statement if not negat else UnaryOpAntecedent(
                self.complement_op, statement)

    def __parse_consequent(self):
        consequent = []
        while True:
            consequent.append(self.__parse_consequent_statement())
            if self.head('comma'):
                self.pop('comma')
            else:
                break
        return consequent

    def __parse_consequent_statement(self):
        l_var, negat, hedge, f_set = self.__parse_statement()
        if not negat:
            return StatementConsequent(l_var, f_set)
        else:
            return UnaryOpConsequent(self.complement_op, l_var, f_set)

    def __parse_statement(self):
        """Parses a statement no the form:
        - 'a is b',
        - 'a is not b'
        - 'a is very b'
        - 'a is not very b'"""
        negat = False
        hedge = False
        l_var = self.pop('literal')
        self.pop('is')
        if self.head('not'):
            self.pop('not')
            negat = True
        if self.head('hedge'):
            hedge = self.pop('hedge')
        if self.head('literal'):
            f_set = self.pop('literal')
        elif self.head('decimal'):
            f_set = self.pop('decimal')
        else:
            raise SyntaxError('Expected logical operator')

        return l_var, negat, hedge, f_set

    def __parse_weight(self):
        return float(self.pop('decimal'))


class Rule:
    """ Represents a fuzzy rule. """

    def __init__(self, rule, antecedent, consequent, weight):
        """ Initializes this rule.

        :param rule: the rule in string format.
        :param antecedent: The antecedent of the rule (the "IF" part)
        :param consequent: The consequent of the rule (the "THEN" part)
        :param weight: The importance of the rule (1 is normal importance)
        """
        self.__rule = rule
        self.__antecedent = antecedent
        self.__consequent = consequent
        self.__weight = weight

    def eval(self, x):
        """ Evaluates the fuzzy input against this rule.

        :param x: the fuzzy values for the fuzzy sets to eval.

        :returns: the fuzzy values evaluated against the rule for all the fuzzy
            sets included in the consequent.
        """
        result = self.__antecedent(x)
        return [c(result) for c in self.__consequent]

    def __repr__(self):
        return self.__rule


class Antecedent:
    """ Antecedent in a 'IF antecedent THEN consequent WITH weight' rule."""

    def __call__(self, x):
        raise NotImplementedError('Abstract class')


class StatementAntecedent(Antecedent):
    """Represents an 'A IS B' part of a rule."""

    def __init__(self, l_var, f_set):
        self.__l_var = l_var
        self.__f_set = f_set

    def __call__(self, x):
        return x[self.__l_var][self.__f_set]


class BinaryOpAntecedent(Antecedent):
    """ Represents an antecedent in the form 'antecedent1 BOp antecedent2'. """

    def __init__(self, binary_op, antecedent1, antecedent2):
        self.__a1, self.__op, self.__a2 = antecedent1, binary_op, antecedent2

    def __call__(self, x):
        return self.__op(self.__a1(x), self.__a2(x))


class UnaryOpAntecedent(Antecedent):
    """ Represents an antecedent in the form 'NOT antecedent' """

    def __init__(self, unary_op, antecedent):
        self.__op, self.__a = unary_op, antecedent

    def __call__(self, x):
        return self.__op(self.__a(x))


class Consequent:
    """ Consequent in an 'IF antecedent THEN consequent WITH weight' rule."""

    def __call__(self, x):
        raise NotImplementedError('Abstract class')


class StatementConsequent(Consequent):
    """Represents an 'A IS B' on a consequent."""

    def __init__(self, l_var, f_set):
        self.__l_var = l_var
        self.__f_set = f_set

    def __call__(self, value):
        return self.__l_var, self.__f_set, value


class UnaryOpConsequent(Consequent):
    """ Representa un antecedente de una regla borrosa para una sentencia del
    tipo 'NOT Consequente'. """

    def __init__(self, unary_op, l_var, f_set):
        self.unary_op = unary_op
        self.l_var = l_var
        self.fuzzy_set = f_set

    def __call__(self, value):
        return self.l_var, self.fuzzy_set, self.unary_op(value)
