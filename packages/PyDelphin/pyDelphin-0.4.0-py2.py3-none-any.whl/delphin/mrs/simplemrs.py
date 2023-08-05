
# SimpleMRS codec
# Summary: This module implements serialization and deserialization of
#          the SimpleMRS encoding of Minimal Recusion Semantics. It
#          provides the standard Pickle API calls of load, loads, dump,
#          and dumps.
# Author: Michael Wayne Goodman <goodmami@uw.edu>

from __future__ import print_function

from collections import deque, defaultdict
import re
from delphin.mrs import Xmrs, Mrs
from delphin.mrs.components import (
    ElementaryPredication, Pred, Lnk, HandleConstraint, IndividualConstraint,
    sort_vid_split, var_sort, var_re, hcons, icons
)
from delphin.mrs.config import (HANDLESORT, CONSTARG_ROLE)
from delphin.mrs.util import rargname_sortkey
from delphin._exceptions import XmrsDeserializationError as XDE

try:
    from pygments import highlight as highlight_
    from pygments.formatters import TerminalFormatter
    from delphin.extra.highlight import SimpleMrsLexer, mrs_colorscheme
    lexer = SimpleMrsLexer()
    formatter = TerminalFormatter(bg='dark', colorscheme=mrs_colorscheme)
    def highlight(text):
        return highlight_(text, lexer, formatter)
except ImportError:
    # warnings.warn
    def highlight(text):
        return text

# versions are:
#  * 1.0 long running standard
#  * 1.1 added support for MRS-level lnk, surface and EP-level surface
_default_version = 1.1
_latest_version = 1.1

_left_bracket = r'['
_right_bracket = r']'
_left_angle = r'<'
_right_angle = r'>'
_colon = r':'
_hash = r'#'
_at = r'@'
_top = r'TOP'
_ltop = r'LTOP'
_index = r'INDEX'
_rels = r'RELS'
_hcons = r'HCONS'
_icons = r'ICONS'
_lbl = r'LBL'
# possible relations for handle constraints
_qeq = r'qeq'
_lheq = r'lheq'
_outscopes = r'outscopes'
_valid_hcons = [_qeq, _lheq, _outscopes]

# pretty-print options
_default_mrs_delim = '\n'

##############################################################################
##############################################################################
# Pickle-API methods


def load(fh, single=False, strict=False):
    """
    Deserialize SimpleMRSs from a file (handle or filename)

    Args:
      fh: filename or file object
      single: if True, only return the first read |Xmrs| object
    Returns:
      a generator of Xmrs objects (unless the *single* option is True)
    """
    if isinstance(fh, str):
        return loads(open(fh, 'r').read(), single=single, strict=strict)
    return loads(fh.read(), single=single, strict=strict)


def loads(s, single=False, strict=False):
    """
    Deserialize SimpleMRS string representations

    Args:
      s: a SimpleMRS string
      single: if True, only return the first read Xmrs object
    Returns:
      a generator of Xmrs objects (unless the *single* option is True)
    """
    ms = deserialize(s, strict=strict)
    if single:
        return next(ms)
    else:
        return ms


def dump(fh, ms, single=False, version=_default_version,
         pretty_print=False, color=False, **kwargs):
    """
    Serialize Xmrs objects to a SimpleMRS representation and write to a
    file

    Args:
      fh: filename or file object
      ms: an iterator of Xmrs objects to serialize (unless the
        *single* option is True)
      single: if True, treat ms as a single Xmrs object instead of
        as an iterator
      pretty_print: if True, the output is formatted to be easier to
        read
      color: if True, colorize the output with ANSI color codes
    Returns:
      None
    """
    print(dumps(ms,
                single=single,
                version=version,
                pretty_print=pretty_print,
                color=color,
                **kwargs),
          file=fh)


def dumps(ms, single=False, version=_default_version,
          pretty_print=False, color=False, **kwargs):
    """
    Serialize an Xmrs object to a SimpleMRS representation

    Args:
      ms: an iterator of Xmrs objects to serialize (unless the
        *single* option is True)
      single: if True, treat ms as a single Xmrs object instead of
        as an iterator
      pretty_print: if True, the output is formatted to be easier to
        read
      color: if True, colorize the output with ANSI color codes
    Returns:
        a SimpleMrs string representation of a corpus of Xmrs
    """
    if single:
        ms = [ms]
    return serialize(ms, version=version,
                     pretty_print=pretty_print, color=color, **kwargs)


# for convenience

load_one = lambda fh, **kwargs: load(fh, single=True, **kwargs)
loads_one = lambda s, **kwargs: loads(s, single=True, **kwargs)
dump_one = lambda fh, m, **kwargs: dump(fh, m, single=True, **kwargs)
dumps_one = lambda m, **kwargs: dumps(m, single=True, **kwargs)

##############################################################################
##############################################################################
# Deserialization

# The tokenizer has 3 sub-regexen:
#   the first is for strings (e.g. "_dog_n_rel", "\"quoted string\"")
#   the second looks for unquoted type preds (lookahead for space or lnk)
#   the second is for args, variables, preds, etc (e.g. ARG1, _dog_n_rel, x4)
#   the last is for contentful punctuation (e.g. [ ] < > : # @)

tokenizer = re.compile(r'("[^"\\]*(?:\\.[^"\\]*)*"'
                       r'|_(?:[^\s<]|<(?![-0-9:#@ ]*>))*'
                       r'|[^\s:#@\[\]"<>]+'
                       r'|[:#@\[\]<>])')


def tokenize(string):
    """Split the SimpleMrs string into tokens."""
    return deque(tokenizer.findall(string))


def validate_token(token, expected):
    """Make sure the given token is as expected, or raise an error. This
       comparison is case insensitive."""
    # uppercase the input, since expected tokens are all upper case
    if token.upper() != expected:
        invalid_token_error(token, expected)


def validate_tokens(tokens, expected):
    for exp_tok in expected:
        validate_token(tokens.popleft(), exp_tok)


def invalid_token_error(token, expected):
    raise XDE('Invalid token: "{}"\tExpected: "{}"'.format(token, expected))


def deserialize(string, strict=True):
    if strict:
        read = read_mrs
    else:
        read = _read_mrs
    # FIXME: consider buffering this so we don't read the whole string at once
    tokens = tokenize(string)
    while tokens:
        yield read(tokens)


def _read_mrs(tokens, version=_default_version):
    #return read_mrs(tokens)
    try:
        if tokens[0] != _left_bracket:
            return None
        top = idx = surface = lnk = None
        vars_ = {}
        tokens.popleft()  # [
        if tokens[0] == _left_angle:
            lnk = read_lnk(tokens)
        if tokens[0].startswith('"'):  # and tokens[0].endswith('"'):
            surface = tokens.popleft()[1:-1]  # get rid of first quotes
        if tokens[0].upper() in (_ltop, _top):
            tokens.popleft()  # LTOP / TOP
            tokens.popleft()  # :
            top = tokens.popleft()
            vars_[top] = []
        if tokens[0].upper() == _index:
            tokens.popleft()  # INDEX
            tokens.popleft()  # :
            idx = tokens.popleft()
            vars_[idx] = _read_props(tokens)
        rels = _read_rels(tokens, vars_)
        hcons = _read_cons(tokens, _hcons, vars_)
        icons = _read_cons(tokens, _icons, vars_)
        tokens.popleft()  # ]
        # at this point, we could uniquify proplists in vars_, but most
        # likely it isn't necessary, and might night harm things if we
        # leave potential dupes in there. let's see how it plays out.
        m = Xmrs(top=top, index=idx, eps=rels,
                 hcons=hcons, icons=icons, vars=vars_,
                 lnk=lnk, surface=surface)
    except IndexError:
        unexpected_termination_error()
    return m


def _read_props(tokens):
    props = []
    if tokens[0] == _left_bracket:
        tokens.popleft()  # [
        vartype = tokens.popleft()  # this gets discarded though
        while tokens[0] != _right_bracket:
            key = tokens.popleft()
            tokens.popleft()  # :
            val = tokens.popleft()
            props.append((key, val))
        tokens.popleft()  # ]
    return props


def _read_rels(tokens, vars_):
    rels = None
    nid = 10000
    if tokens[0].upper() == _rels:
        rels = []
        tokens.popleft()  # RELS
        tokens.popleft()  # :
        tokens.popleft()  # <
        while tokens[0] != _right_angle:
            rels.append(_read_ep(tokens, nid, vars_))
            nid += 1
        tokens.popleft()  # >
    return rels


def _read_ep(tokens, nid, vars_):
    # reassign these locally to avoid global lookup
    CARG = CONSTARG_ROLE
    _var_re = var_re
    # begin parsing
    tokens.popleft()  # [
    pred = Pred.string_or_grammar_pred(tokens.popleft())
    lnk = read_lnk(tokens)
    surface = label = None
    if tokens[0].startswith('"'):
        surface = tokens.popleft()[1:-1]  # get rid of first quotes
    if tokens[0].upper() == _lbl:
        tokens.popleft()  # LBL
        tokens.popleft()  # :
        label = tokens.popleft()
        vars_[label] = []
    args = {}
    while tokens[0] != _right_bracket:
        role = tokens.popleft().upper()
        tokens.popleft()  # :
        val = tokens.popleft()
        if _var_re.match(val) is not None and role.upper() != CARG:
            props = _read_props(tokens)
            if val not in vars_:
                vars_[val] = []
            vars_[val].extend(props)
        args[role] = val
    tokens.popleft()  # ]
    return (nid, pred, label, args, lnk, surface)


def _read_cons(tokens, constype, vars_):
    cons = None
    if tokens[0].upper() == constype:
        cons = []
        tokens.popleft()  # (H|I)CONS
        tokens.popleft()  # :
        tokens.popleft()  # <
        while tokens[0] != _right_angle:
            left = tokens.popleft()
            lprops = _read_props(tokens)
            reln = tokens.popleft().lower()
            rght = tokens.popleft()
            rprops = _read_props(tokens)
            cons.append((left, reln, rght))
            # update properties
            if left not in vars_: vars_[left] = []
            vars_[left].extend(lprops)
            if rght not in vars_: vars_[rght] = []
            vars_[rght].extend(lprops)
        tokens.popleft()  # >
    return cons


def read_mrs(tokens, version=_default_version):
    """Decode a sequence of Simple-MRS tokens. Assume LTOP, INDEX, RELS,
       HCONS, and ICONS occur in that order."""
    # variables needs to be passed to any function that can call read_variable
    variables = defaultdict(list)
    # [ LTOP : handle INDEX : variable RELS : rels-list HCONS : hcons-list ]
    try:
        validate_token(tokens.popleft(), _left_bracket)
        ltop = index = surface = lnk = None
        # SimpleMRS extension for encoding surface string
        if tokens[0] == _left_angle:
            lnk = read_lnk(tokens)
        if tokens[0].startswith('"'): # and tokens[0].endswith('"'):
            surface = tokens.popleft()[1:-1] # get rid of first quotes
        if tokens[0] in (_ltop, _top):
            _, ltop = read_featval(tokens, variables=variables)
        if tokens[0] == _index:
            _, index = read_featval(tokens, feat=_index, variables=variables)
        rels = read_rels(tokens, variables=variables)
        hcons = read_hcons(tokens, variables=variables)
        icons = read_icons(tokens, variables=variables)
        validate_token(tokens.popleft(), _right_bracket)
        m = Mrs(top=ltop,
                index=index,
                rels=rels,
                hcons=hcons,
                icons=icons,
                lnk=lnk,
                surface=surface,
                vars=variables)
    except IndexError:
        unexpected_termination_error()
    return m


def read_featval(tokens, feat=None, sort=None, variables=None):
    # FEAT : (var-or-handle|const)
    name = tokens.popleft()
    if feat is not None:
        validate_token(name, feat)
    validate_token(tokens.popleft(), _colon)
    # if it's not a variable, assume it's a constant
    if var_re.match(tokens[0]) is not None:
        value = read_variable(tokens, sort=sort, variables=variables)
    else:
        value = tokens.popleft()
    return name, value


def read_variable(tokens, sort=None, variables=None):
    """
    Read and return the variable and update a property dict.
    Fail if the sort does not match the expected.
    """
    # var [ vartype PROP : val ... ]
    if variables is None:
        variables = defaultdict(list)
    var = tokens.popleft()
    srt, vid = sort_vid_split(var)
    # consider something like not(srt <= sort) in the case of subsumptive sorts
    if sort is not None and srt != sort:
        raise XDE('Variable {} has sort "{}", expected "{}"'
                  .format(var, srt, sort))
    vartype, props = read_props(tokens)
    if vartype is not None and srt != vartype:
        raise XDE('Variable "{}" and its cvarsort "{}" are not the same.'
                  .format(var, vartype))
    if srt == 'h' and props:
        raise XDE('Handle variable "{}" has a non-empty property set {}.'
                  .format(var, props))
    variables[var].extend(props)
    return (var, props)


def read_props(tokens):
    """
    Read and return a list of variable properties paired with their values.
    """
    # [ vartype PROP1 : val1 PROP2 : val2 ... ]
    props = []
    if not tokens or tokens[0] != _left_bracket:
        return None, props
    tokens.popleft()  # get rid of bracket (we just checked it)
    vartype = tokens.popleft()
    # check if a vartype wasn't given (next token is : )
    if tokens[0] == _colon:
        invalid_token_error(vartype, "variable type")
    while tokens[0] != _right_bracket:
        prop = tokens.popleft()
        validate_token(tokens.popleft(), _colon)
        val = tokens.popleft()
        props.append((prop, val))
    tokens.popleft()  # we know this is a right bracket
    return vartype, props


def read_rels(tokens, variables=None):
    """Read and return a RELS set of ElementaryPredications."""
    # RELS: < ep* >
    if tokens[0] != _rels:
        return None
    tokens.popleft()  # pop "RELS"
    if variables is None:
        variables = {}
    rels = []
    validate_tokens(tokens, [_colon, _left_angle])
    while tokens[0] != _right_angle:
        rels += [read_ep(tokens, variables=variables)]
    tokens.popleft()  # we know this is a right angle
    return rels


def read_ep(tokens, variables=None):
    """Read and return an ElementaryPredication."""
    # [ pred LBL : lbl ARG : variable-or-handle ... ]
    # or [ pred < lnk > ...
    if variables is None:
        variables = {}
    validate_token(tokens.popleft(), _left_bracket)
    pred = Pred.string_or_grammar_pred(tokens.popleft())
    lnk = read_lnk(tokens)
    if tokens[0].startswith('"'):
        surface = tokens.popleft()[1:-1] # get rid of first quotes
    else:
        surface = None
    _, label = read_featval(tokens, feat=_lbl, sort=HANDLESORT,
                            variables=variables)
    args = []
    while tokens[0] != _right_bracket:
        args.append(read_argument(tokens, variables=variables))
    tokens.popleft()  # we know this is a right bracket
    return ElementaryPredication(None,  # no nodeid in MRS
                                 pred,
                                 label,
                                 args=args,
                                 lnk=lnk,
                                 surface=surface)


def read_argument(tokens, variables=None):
    """Read and return an Argument."""
    # ARGNAME: (VAR|CONST)
    if variables is None:
        variables = {}
    argname, value = read_featval(tokens, variables=variables)
    return (argname, value) #Argument.mrs_argument(argname, value)


def read_lnk(tokens):
    """Read and return a tuple of the pred's lnk type and lnk value,
       if a pred lnk is specified."""
    # < FROM : TO > or < FROM # TO > or < TOK... > or < @ EDGE >
    lnk = None
    if tokens[0] == _left_angle:
        tokens.popleft()  # we just checked this is a left angle
        if tokens[0] == _right_angle:
            pass  # empty <> brackets the same as no lnk specified
        # edge lnk: ['@', EDGE, ...]
        elif tokens[0] == _at:
            tokens.popleft()  # remove the @
            lnk = Lnk.edge(tokens.popleft())  # edge lnks only have one number
        # character span lnk: [FROM, ':', TO, ...]
        elif tokens[1] == _colon:
            lnk = Lnk.charspan(tokens.popleft(), tokens[1])
            tokens.popleft()  # this should be the colon
            tokens.popleft()  # and this is the cto
        # chart vertex range lnk: [FROM, '#', TO, ...]
        elif tokens[1] == _hash:
            lnk = Lnk.chartspan(tokens.popleft(), tokens[1])
            tokens.popleft()  # this should be the hash
            tokens.popleft()  # and this is the to vertex
        # tokens lnk: [(TOK,)+ ...]
        else:
            lnkdata = []
            while tokens[0] != _right_angle:
                lnkdata.append(int(tokens.popleft()))
            lnk = Lnk.tokens(lnkdata)
        validate_token(tokens.popleft(), _right_angle)
    return lnk


def read_hcons(tokens, variables=None):
    # HCONS:< HANDLE (qeq|lheq|outscopes) HANDLE ... >
    """Read and return an HCONS list."""
    if tokens[0] != _hcons:
        return None
    tokens.popleft()  # pop "HCONS"
    if variables is None:
        variables = {}
    hcons = []
    validate_tokens(tokens, [_colon, _left_angle])
    while tokens[0] != _right_angle:
        hi = read_variable(tokens, sort='h', variables=variables)[0]
        # rels are case-insensitive and the convention is lower-case
        rel = tokens.popleft().lower()
        if rel == _qeq:
            rel = HandleConstraint.QEQ
        elif rel == _lheq:
            rel = HandleConstraint.LHEQ
        elif rel == _outscopes:
            rel = HandleConstraint.OUTSCOPES
        else:
            invalid_token_error(rel, '('+'|'.join(_valid_hcons)+')')
        lo = read_variable(tokens, sort='h', variables=variables)[0]
        hcons.append(HandleConstraint(hi, rel, lo))
    tokens.popleft()  # we know this is a right angle
    return hcons

def read_icons(tokens, variables=None):
    # ICONS:< TARGET RELATION CLAUSE ... >
    if tokens[0] != _icons:
        return None
    tokens.popleft()  # pop "ICONS"
    if variables is None:
        variables = {}
    icons = []
    validate_tokens(tokens, [_colon, _left_angle])
    while tokens[0] != _right_angle:
        # NOTE: This ignores any properties specified on the variables
        #  (I don't think this is allowed anyway, but i'm not sure yet)
        left = read_variable(tokens, variables=variables)[0]
        relation = tokens.popleft().lower()
        right = read_variable(tokens, variables=variables)[0]
        icons.append(IndividualConstraint(left, relation, right))
    tokens.popleft()  # we know this is a right angle
    return icons


def unexpected_termination_error():
    raise XDE('Invalid MRS: Unexpected termination.')

##############################################################################
##############################################################################
# Encoding


def serialize(ms, version=_default_version, pretty_print=False, color=False):
    """Serialize an MRS structure into a SimpleMRS string."""
    delim = '\n' if pretty_print else _default_mrs_delim
    output = delim.join(
        serialize_mrs(m, version=version, pretty_print=pretty_print)
        for m in ms
    )
    if color:
        output = highlight(output)
    return output


def serialize_mrs(m, version=_default_version, pretty_print=False):
    # note that varprops is modified as a side-effect of the lower
    # functions
    varprops = {v: vd['props'] for v, vd in m._vars.items() if vd['props']}
    toks = []
    if version >= 1.1:
        header_toks = []
        if m.lnk is not None and m.lnk.data != (-1, -1):  # don't do <-1:-1>
            header_toks.append(serialize_lnk(m.lnk))
        if m.surface is not None:
            header_toks.append('"{}"'.format(m.surface))
        if header_toks:
            toks.append(' '.join(header_toks))
    if m.top is not None:
        toks.append(serialize_argument(
            _top if version >= 1.1 else _ltop, m.top, varprops
        ))
    if m.index is not None:
        toks.append(serialize_argument(
            _index, m.index, varprops
        ))
    delim = ' ' if not pretty_print else '\n          '
    toks.append('RELS: < {eps} >'.format(
        eps=delim.join(serialize_ep(ep, varprops, version=version)
                       for ep in m.eps())
    ))
    toks += [serialize_hcons(hcons(m))]
    icons_ = icons(m)
    if icons_:  # make unconditional for "ICONS: < >"
        toks += [serialize_icons(icons_)]
    delim = ' ' if not pretty_print else '\n  '
    return '{} {} {}'.format(_left_bracket, delim.join(toks), _right_bracket)


def serialize_argument(rargname, value, varprops):
    """Serialize an MRS argument into the SimpleMRS format."""
    _argument = '{rargname}: {value}{props}'
    props = ''
    if value in varprops:
        props = ' [ {} ]'.format(
            ' '.join(
                [var_sort(value)] +
                list(map('{0[0]}: {0[1]}'.format,
                         [(k.upper(), v) for k, v in varprops[value]]))
            )
        )
        del varprops[value]  # only print props once
    return _argument.format(
        rargname=rargname,
        value=str(value),
        props=props
    )


def serialize_ep(ep, varprops, version=_default_version):
    """Serialize an Elementary Predication into the SimpleMRS encoding."""
    # ('nodeid', 'pred', 'label', 'args', 'lnk', 'surface', 'base')
    args = ep[3]
    arglist = ' '.join([serialize_argument(rarg, args[rarg], varprops)
                        for rarg in sorted(args, key=rargname_sortkey)])
    if version < 1.1 or len(ep) < 6 or ep[5] is None:
        surface = ''
    else:
        surface = ' "%s"' % ep[5]
    lnk = None if len(ep) < 5 else ep[4]
    pred = ep[1]
    predstr = pred.string
    return '[ {pred}{lnk}{surface} LBL: {label}{s}{args} ]'.format(
        pred=predstr,
        lnk=serialize_lnk(lnk),
        surface=surface,
        label=str(ep[2]),
        s=' ' if arglist else '',
        args=arglist
    )


def serialize_lnk(lnk):
    """Serialize a predication lnk to surface form into the SimpleMRS
       encoding."""
    s = ""
    if lnk is not None:
        s = _left_angle
        if lnk.type == Lnk.CHARSPAN:
            cfrom, cto = lnk.data
            s += ''.join([str(cfrom), _colon, str(cto)])
        elif lnk.type == Lnk.CHARTSPAN:
            cfrom, cto = lnk.data
            s += ''.join([str(cfrom), _hash, str(cto)])
        elif lnk.type == Lnk.TOKENS:
            s += ' '.join([str(t) for t in lnk.data])
        elif lnk.type == Lnk.EDGE:
            s += ''.join([_at, str(lnk.data)])
        s += _right_angle
    return s


def serialize_hcons(hcons):
    """Serialize |HandleConstraints| into the SimpleMRS encoding."""
    toks = [_hcons + _colon, _left_angle]
    for hc in hcons:
        toks.extend(hc)
        # reln = hcon[1]
        # toks += [hcon[0], rel, str(hcon.lo)]
    toks += [_right_angle]
    return ' '.join(toks)

def serialize_icons(icons):
    """Serialize |IndividualConstraints| into the SimpleMRS encoding."""
    toks = [_icons + _colon, _left_angle]
    for ic in icons:
        toks.extend(ic)
        # toks += [str(icon.left),
        #          icon.relation,
        #          str(icon.right)]
    toks += [_right_angle]
    return ' '.join(toks)

# default defs:
# '': r'\s*'
# '_': r'\s+'
# 'INT': r'-?\d+'
# 'QSTRING' : '{DQSTRING|SQSTRING}'
# 'DQSTRING': r'"..."'
# 'SQSTRING': r"'...'"
# SimpleMrsSerializer = XmrsSerializer(
#     grammar={
#         'start':    '{MRS}',
#         'MRS':      '[{LNK:?}{SURFACE:?} {TOP} {INDEX} {RELS}{HCONS}{ICONS}]',
#         'LNK':      '<{CHARSPAN|CHARTSPAN|TOKENS|EDGE}>',
#         'CHARSPAN': '{INT}:{INT}',
#         'CHARTSPAN':'{INT}#{INT}',
#         'TOKENS':   '{INT:*}',
#         'EDGE':     '@{INT}',
#         'SURFACE':  '{DQSTRING}',
#         'TOP':      'TOP: {VAR}',
#         'INDEX':    'INDEX: {VARDEF}',
#         'RELS':     'RELS: < {EP:*} >',
#         'EP':       '[{PRED}{LNK:?}{SURFACE:?} LBL:{VAR} {RARG:*}]',
#         'PRED':     '{TPRED|SPRED}',
#         'TPRED':    re(r'_?...', Pred.string_or_grammar_pred),
#         'GPRED':    '{DQSTRING}',
#         'RARG':     '{ROLE}:{ARG}',
#         'ROLE':     '{SYM}',
#         'ARG':      '{VARDEF|DQSTRING}',
#         'HCONS':    'HCONS: < {HCON:*} >',
#         'HCON':     '{VAR} {HCRELN} {VAR}',
#         'HCRELN':   re(r'qeq|lheq|outscopes'),
#         'ICONS':    'ICONS: < {ICON:*} >',
#         'ICON':     '{VAR} {ICRELN} {VAR}',
#         'ICRELN':   re(r'[-\w]+'),
#         'VARDEF':   '{VAR}{VARPROPS:?}',
#         'VAR':      re(r'[-\w]+\d+'),
#         'VARPROPS': '[ {VARSORT} {EXTRAPAIR:*} ]',
#         'VARSORT':  '{SYM}',
#         'EXTRAPAIR':'{FEAT}: {VAL}',
#         'FEAT':     '{SYM}',
#         'VAL':      '{SYM}',
#         'SYM':      re(r'[-\w]+')
#     },
#     conversions={'d': dict},
#     flags=re.I
# )
