def state(state, node_labels=False, sep=False):
    """Format a state tuple for printing. Uses LaTeX.

    Args:
        state (tuple(bit)): The state to format.

    Keyword args:
        node_labels (list(str)): The labels of each node in the system, as ordered
            in `state`. Nodes that are on will be bolded. If none is provided,
            simply print the state bits.
        sep (str): Use this character to separate node names

    Returns:
        (str): The formatted state.
    """

    state_string = r''

    if node_labels is False:
        # if printing bits
        node_tokens = [str(node_state) for node_state in state]
    else:
        # printing node names.
        # bold the names of nodes that are on.
        node_tokens = list()
        for node_label, node_state in zip(node_labels, state):
            if node_state:
                node_tokens.append(r'\textbf{{{}}}'.format(node_label))
            else:
                node_tokens.append(node_label)

    sep_str = ',' if sep else ''
    return r'{}'.format(sep_str).join(node_tokens)

def parse_spec(concept, fmt_spec):
    """ Parse a string that specifies how to format a state.

    Args:
        concept (pyphi.models.Concept): The concept whose subsystem we're
            interested in formatting the state of. Used to fetc node labels.
        fmt_spec (str): The actual state format specifier. If the string
            begins with a 1, the binary reperestation will be used. If the string
            beings with an alphabetic character, node labels will be used. If a
            ',' is present, element names will be separated when printing.

    Returns:
        (list(str), str): The node labels and separator specified by the spec.
    """
    if fmt_spec[0].isalpha():
        # if printing node labels
        node_labels = get_node_labels(concept)
    elif fmt_spec[0].isdigit():
        # if printing state bits
        node_labels = False
    else:
        raise ValueError('Unrecognized format spec. '
                         'First character must be a letter or a digit.')

    sep = True if ',' in fmt_spec else False #

    return (node_labels, sep)

def get_node_labels(concept):
    """Get the node labels for each node in a concept's subsystem.

    Args:
        concept (pyphi.models.Concept)

    Returns:
        (list(str)): The node labels.
    """
    return [node.label for node in concept.subsystem.nodes]

def mice(concept, direction, sep=False):
    """Format a MICE for printing. Uses LaTeX.

    Args:
        concept (pyphi.models.Concept): The concept whose MICE to print.
        direction (str): 'past' or 'future'.

    Keyword args:
        sep (str): Use this separator string between element names.

    Returns:
        (str): The formatted MICE.
    """
    if direction == 'past':
        purview = concept.cause.purview
    elif direction == 'future':
        purview = concept.effect.purview
    else:
        raise ValueError("direction must be 'past' or 'future'.")

    node_labels = get_node_labels(concept)
    mech_labels = [node_labels[x] for x in concept.mechanism]
    purv_labels = [node_labels[x] for x in purview]

    sep_str = ',' if sep else ''
    mech_str = '{}'.format(sep_str).join(mech_labels)
    purv_str = '{}'.format(sep_str).join(purv_labels)
    return r'${}^c/{}^{}$'.format(mech_str, purv_str, direction[0])

def partition(concept, direction, sep=False, oneliner=True):
    """Format a partition/cut for printing. Uses LaTeX.

    Args:
        concept (pyphi.models.Concept): The concept whose MICE partition to print.
        direction (str): 'past' or 'future'.

    Keyword args:
        sep (str): Use this separator string between element names.
        oneliner (bool): If true, print partition on a single line using a
            vertical (i.e. /) symbol, rather than a horizontal bar as in pyphi.
            Default *True*.

    Returns:
        (str): The formatted partition.
    """
    if direction == 'past':
        partition = concept.cause.mip.partition
    elif direction == 'future':
        partition = concept.effect.mip.partition
    else:
        raise ValueError("direction must be 'past' or 'future'.")

    if not partition:
        return ""

    node_labels = get_node_labels(concept)
    sep_str = ',' if sep else ''
    format_tokens = lambda x: '{}'.format(sep_str).join([node_labels[i] for i in x]) if x else '[]'

    part0, part1 = partition
    numer0 = format_tokens(part0.mechanism)
    denom0 = format_tokens(part0.purview)
    numer1 = format_tokens(part1.mechanism)
    denom1 = format_tokens(part1.purview)

    if oneliner:
        return (r'${{{numer0}^c/{denom0}^{dir}}}'
                r'\times'
                r'{{{numer1}^c/{denom1}^{dir}}}$').format(
                    numer0=numer0, denom0=denom0, numer1=numer1, denom1=denom1,
                    dir=direction[0])
    else:
        return (r'$\frac{{{numer0}^c}}{{{denom0}^{dir}}}'
                r'\times'
                r'\frac{{{numer1}^c}}{{{denom1}^{dir}}}$').format(
                    numer0=numer0, denom0=denom0, numer1=numer1, denom1=denom1,
                    dir=direction[0])

def smallphi(concept, direction):
    """Format a smallphi value for printing. Uses LaTeX.

    Args:
        concept (pyphi.models.Concept): The concept whose smallphi to print.
        direction (str): 'past', 'future', or *None* determine whether to print
            smallphi_cause, smallphi_effect, or smallphi.

    Returns:
        (str): The formatted smallphi.
    """
    if direction == 'past':
        phi = concept.cause.phi
        dir_str = 'cause'
    elif direction == 'future':
        phi = concept.effect.phi
        dir_str = 'effect'
    else:
        phi = concept.phi
        return r'$\varphi={:.2f}$'.format(phi)

    return (r'$\varphi^{{{dir_str}}}: {phi:.2f}$').format(
                dir_str=dir_str, phi=phi)

def repertoire_title(concept, direction, fmt_spec):
    """Format a repertoire's tile/metainfo for printing. Uses LaTeX.

    Args:
        concept (pyphi.models.Concept): The concept in question.
        direction (str): 'past' or 'future'.
        fmt_spec (str): Specifies how the plot should be titled. If the string
            contains an...
                'M', the MICE will be plotted.
                'P', the smallphi_cause will be plotted.
                'C', the partition/cut will be plotted.
                ',', element names will be separated when printing.

    Returns:
        (str): The formatted title/metainfo.
    """
    sep = True if ',' in fmt_spec else ''
    title_parts = list()
    if 'M' in fmt_spec:
        title_parts.append("MICE: " + mice(concept, direction, sep=sep))
    if 'P' in fmt_spec:
        title_parts.append(smallphi(concept, direction))
    if 'C' in fmt_spec:
        title_parts.append("Cut: " + partition(concept, direction, sep=sep))

    if title_parts:
        return '\quad'.join(title_parts)
    elif direction == 'past':
        return r"Cause repertoire"
    elif direction == 'future':
        return r"Effect repertoire"

def concept_summary(concept):
    """Format a concept's title/metainfo for printing. Uses LaTeX.

    Args:
        concept (pyphi.models.Concept): The concept in question.

    Returns:
        (str): The formatted title/metainfo.
    """
    node_labels = get_node_labels(concept)
    mech_labels = [node_labels[x] for x in concept.mechanism]
    mech_str = ','.join(mech_labels)
    phi_str = smallphi(concept, None)
    return mech_str + r'\newline' + phi_str
