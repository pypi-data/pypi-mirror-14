import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D, proj3d
import pyphi
from pyphi.convert import holi_index2state, loli_index2state
import numpy as np
import logging
from . import string_formatters as fmt

# Set default figure background (area outside axes) color to white
mpl.rcParams['figure.facecolor'] = 'white'
# Use Latex for text rendering
mpl.rc('text', usetex=True)
# Create a logger for this module.
log = logging.getLogger(__name__)

def plot_repertoire(repertoire, partitioned_repertoire=None, legend=False,
                    label_with_values=False, label_axes=False, node_labels=False,
                    sep=True, ax=None):
    """Plot a cause or effect repertoire as a probability vs. state barchart.

    Examples:
        >>> A = pyphi.compute.concept(sub, ('A',))
        >>> plot_repertoire(A.cause.repertoire)
        >>> matplotlib.pyplot.show()

    Args:
        repertoire (np.ndarray): An array that, when flattened, gives the
            probability of each state in loli order. Any PyPhi repertoire satisfies
            these conditions.

    Keyword Args:
        partitioned_repertoire (np.ndarray): The partitioned analogue of 'repertoire',
            which is assumed to be unpartitioned. Both repertoires are plotted
            side-by-side.
        legend (bool): Plot a legend. Default *False*.
        label_with_values (bool): Plot numeric probabilitites above each bar.
            Default *False*.
        label_axes (bool): Label the x and y axes. Default *False*.
        node_labels (list(str)): If provided, node labels will be used instead
            of bits when printing states (e.g. ABC rather than 111).
        sep (str): If provided, use this string to separate elements when printing
            states (e.g. 1,1,1 if sep=',').
        ax (matplotlib.Axes): The axes on which to plot. If none are provided,
            the current axes are used.
    """
    # TODO: expose state probability label text properties

    if ax is None:
        ax = plt.gca()

    assert(isinstance(repertoire, np.ndarray))
    assert(isinstance(partitioned_repertoire, (np.ndarray, type(None))))
    n_states = len(repertoire.flatten())
    state_inds = np.arange(n_states)
    n_nodes = int(np.log2(n_states))

    # Plot
    bar_width = .35 if partitioned_repertoire is not None else 0.7
    unpartitioned_bars = ax.bar(state_inds, repertoire.flatten(),
                                width=bar_width, color='black')
    if partitioned_repertoire is not None:
        partitioned_bars = ax.bar(state_inds + bar_width,
                                  partitioned_repertoire.flatten(),
                                  width=bar_width, color='gray')
        if legend:
            ax.legend((unpartitioned_bars[0], partitioned_bars[0]),
                      ('unpartitioned', 'partitioned'))
        bar_centers = state_inds + bar_width
    else:
        bar_centers = state_inds + bar_width / 2

    ax.set_xlim(0, n_states) # make sure no bins get clipped
    ax.set_ylim(0, 1) # probabilities range from 0 to 1
    ax.yaxis.grid(True)

    ax.set_yticks([0, .25, .5, .75, 1])
    ax.set_yticklabels([0, '',.5, '', 1])

    # Set x-axis (i.e. state) labels
    states = [holi_index2state(i, n_nodes) for i in range(n_states)]
    state_labels = [fmt.state(state, node_labels=node_labels, sep=sep) for state in states]
    ax.set_xticks(bar_centers)
    ax.set_xticklabels(state_labels, rotation='-45')

    # Plot state probabilities above each bar if requested
    font_size = 8 # size of labels, in pts.
    def add_probability_labels(repertoire, bar_centers):
        """ Given an array of state probabiltities and the x coordinate of each
            state's bar, plot numeric labels above each bar."""

        # for each bin, plot the label above it
        for state_probability, bar_center in zip(repertoire.flatten(), bar_centers):
            ax.annotate('{:.2f}'.format(state_probability), # round label to 2 decimal places
                        xy=(bar_center, state_probability), # the point being labeled
                        xycoords=('data', 'axes fraction'), # metadata about what's being labeled
                        xytext=(0, font_size), # location of label relative to xy
                        textcoords='offset points',
                        size=font_size,
                        va='top', # vertical alignment
                        ha='center') # horizontal alignment

    if label_with_values:
        if partitioned_repertoire is not None:
            # Calculate where each label needs to go
            unpartitioned_bar_centers = bar_centers - bar_width / 2
            partitioned_bar_centers = bar_centers + bar_width / 2
            # Plot unpartitioned and partitioned repertoire labels separately
            add_probability_labels(repertoire, unpartitioned_bar_centers)
            add_probability_labels(partitioned_repertoire, partitioned_bar_centers)
        else:
            add_probability_labels(repertoire, bar_centers)

    # Label axes if requested
    if label_axes:
        ax.set_xlabel(r"State")
        ax.set_ylabel(r'p(State)')

def plot_cause_repertoire(concept, show_partitioned=True, expand=True,
                          title_fmt='M', title_size=12, state_fmt='1,', ax=None,
                          **kwargs):
    """Plot a cause-repertoire barchart.

    Examples:
        >>> A = pyphi.compute.concept(sub, ('A',))
        >>> # Title plot with MICE, phi, and cut info. Shrink title to fit.
        >>> plot_cause_repertoire(A, title_fmt='MPC,', title_size=8)
        >>> plt.show()

    Args:
        concept (pyphi.models.Concept): The concept whose cause to plot.

    Keyword args:
        show_partitioned (bool): Plot the partitioned repertoire alongside the
            unpartitioend repertoire. Default *True*.
        expand (bool): Expand and plot the repertoires over all subsystem elements,
            rather than just over their purviews. Default *True*.
        title_fmt (str): Specifies how the plot should be titled. If the string
            contains an...
                'M', the MICE will be plotted.
                'P', the smallphi_cause will be plotted.
                'C', the partition/cut will be plotted.
                ',', element names will be separated when printing.
            Default *M* (print only MICE with no element separation).
        title_size (int): Font size of title. Default *12*.
        state_fmt (str): Specifies how the states will be printed. If the string
            begins with a 1, the binary reperestation will be used. If the string
            beings with an alphabetic character, node labels will be used. If a
            ',' is present, element names will be separated when printing.
        ax (matplotlib.Axes): The axes on which to plot. If none are provided,
            the current axes are used.
        Any unmatched kwargs are relayed to `plot_repertoire`.
    """

    if ax is None:
        ax = plt.gca()

    assert(isinstance(concept, pyphi.models.Concept))

    if expand and show_partitioned:
        unpartitioned_repertoire = concept.expand_cause_repertoire()
        partitioned_repertoire = concept.expand_partitioned_cause_repertoire()
    if expand and not show_partitioned:
        unpartitioned_repertoire = concept.expand_cause_repertoire()
        partitioned_repertoire = None
    if not expand and show_partitioned:
        unpartitioned_repertoire = concept.cause.mip.unpartitioned_repertoire
        partitioned_repertoire = concept.cause.mip.partitioned_repertoire
    if not expand and not show_partitioned:
        unpartitioned_repertoire = concept.cause.mip.unpartitioned_repertoire
        partitioned_repertoire = None

    node_labels, state_sep = fmt.parse_spec(concept, state_fmt)
    plot_repertoire(unpartitioned_repertoire,
                    partitioned_repertoire=partitioned_repertoire,
                    node_labels=node_labels, sep=state_sep, ax=ax, **kwargs)

    if title_fmt is not None:
        ax.set_title(fmt.repertoire_title(concept, 'past', title_fmt),
                     fontsize=title_size)

def plot_effect_repertoire(concept, show_partitioned=True, expand=True,
                           title_fmt='M', title_size=12, state_fmt='1,',
                           ax=None, **kwargs):
    """Plot an effect-repertoire barchart. See `plot_cause_repertoire` for
        details.
    """

    if ax is None:
        ax = plt.gca()

    assert(isinstance(concept, pyphi.models.Concept))

    if expand and show_partitioned:
        unpartitioned_repertoire = concept.expand_effect_repertoire()
        partitioned_repertoire = concept.expand_partitioned_effect_repertoire()
    if expand and not show_partitioned:
        unpartitioned_repertoire = concept.expand_effect_repertoire()
        partitioned_repertoire = None
    if not expand and show_partitioned:
        unpartitioned_repertoire = concept.effect.mip.unpartitioned_repertoire
        partitioned_repertoire = concept.effect.mip.partitioned_repertoire
    if not expand and not show_partitioned:
        unpartitioned_repertoire = concept.effect.mip.unpartitioned_repertoire
        partitioned_repertoire = None

    node_labels, state_sep = fmt.parse_spec(concept, state_fmt)
    plot_repertoire(unpartitioned_repertoire, partitioned_repertoire=partitioned_repertoire,
                    node_labels=node_labels, sep=state_sep, ax=ax, **kwargs)

    if title_fmt is not None:
        ax.set_title(fmt.repertoire_title(concept, 'future', title_fmt), fontsize=title_size)

def plot_concept(concept, fig=None, subplot_spec=None, **kwargs):
    """Plot a concept's cause- and effect-repertoires side-by-side, with some
    additional metainfo.

    Examples:
        >>> # Create an 8-inch by 2-inch figure and plot on it.
        >>> A = pyphi.compute.concept(sub, ('A',))
        >>> fig = matplotlib.pyplot.figure(1, (8, 2))
        >>> plot_concept(A, fig=fig, state_fmt='ABC') # use node labels
        >>> matplotlib.pyplot.show()

    Args:
        concept (pyphi.models.Concept): The concept to plot.

    Keyword args:
        fig (matplotlib.Figure): A figure on which to plot. If none is provided,
            a new figure is created and used. Default *None*.
        subplot_spec (matplotlib.gridspec.GridSpec): A gridspec object indicating
            where on a figure to plot. If none is provided, the whole figure is
            used. Default *None*.
        Any unmatched kwargs are passed to `plot_cause_repertoire` and
            `plot_effect_repertoire`.
    """

    if fig is None:
        fig = plt.figure()

    if subplot_spec is None and fig is not None:
        # Divide the plotting area into a 1-row by 9-column grid.
        gs = gridspec.GridSpec(1, 9)
    else:
        gs = gridspec.GridSpecFromSubplotSpec(1, 9, subplot_spec=subplot_spec)

    summary_ax = plt.Subplot(fig, gs[0, 4]) # Use the middle column for metainfo
    cause_ax = plt.Subplot(fig, gs[0, 0:4]) # Span the leftmost 4 columns
    effect_ax = plt.Subplot(fig, gs[0, 5:9]) # Span the rightmost 4 columns
    fig.add_subplot(summary_ax)
    fig.add_subplot(cause_ax)
    fig.add_subplot(effect_ax)
    summary_ax.text(.5, .5, fmt.concept_summary(concept),
                    horizontalalignment='center', verticalalignment='center',
                    multialignment='center')
    summary_ax.axis('off')
    plot_cause_repertoire(concept, ax=cause_ax, **kwargs)
    plot_effect_repertoire(concept, ax=effect_ax, **kwargs)
    effect_ax.set_yticklabels([])

    fig.tight_layout()

def plot_concept_list(constellation, fig=None, **kwargs):
    """Vertically stack a constellation's concept plots (uses `plot_concept`).

    Examples:
        >>> big_mip = pyphi.compute.big_mip(sub)
        >>> plot_concept_list(big_mip.unpartitioned_constellation,
                             title_fmt='MP', state_fmt='1')
        >>> matplotlib.pyplot.show()

    Args:
        constellation (list(pyphi.models.Concept)): A list of concepts to plot.

    Keyword args:
        fig (matplotlib.Figure): A figure on which to plot. If *None*, a new
            figure is created and used. Default *None*.
        Any unmatched kwargs are passed to `plot_concept`.
    """
    DEFAULT_WIDTH = 8 # in inches
    DEFAULT_CONCEPT_HEIGHT = 1.75 # in inches
    n_concepts = len(constellation)
    if fig is None:
        fig = plt.figure(1, (DEFAULT_WIDTH, DEFAULT_CONCEPT_HEIGHT * n_concepts))


    gs = gridspec.GridSpec(n_concepts, 1)

    for concept_idx in range(n_concepts):
        plot_concept(constellation[concept_idx],
                     fig=fig,
                     subplot_spec=gs[concept_idx, 0],
                     **kwargs)

    fig.tight_layout()

def plot_3D_constellation(constellation, label_axes=False, label_stars=True,
                          color_code_axes=False, state_fmt='A'):
    """Generate a 3D-plot of a constellation of concepts in cause-effect space.

    Examples:
        >>> big_mip = pyphi.compute.big_mip(sub)
        >>> plot_3D_constellation(big_mip.unpartitioned_constellation)

    Written by Billy Marshall, modified by Graham Findlay.
    Cause-effect space is a high dimensional space, one for each possible past
    and future state of the system (2 ** (n+1) dimensional for a system of
    binary elements). Each concept in the constellation is a point in
    cause-effect space. The size of the point is proportional to the small-phi
    value of the concept. The location on each axis represents the probability
    of the corresponding past / future state in the cause-effect repertoires of
    the concept. Only three dimensions are shown in the plot, the two future
    states and one past state with greatest variance in the repertoire values.

    Args:
        constellation (list(pyphi.models.Concept)): A list of concepts to plot.
    """
    if not constellation:
        return

    sub = constellation[0].subsystem
    n_nodes = sub.size
    n_states = 2 ** n_nodes
    n_concepts = len(constellation)
    node_labels, sep = fmt.parse_spec(constellation[0], state_fmt)

    # Get an array of cause-effect repertoires, expanded over the system
    cause_repertoires = np.zeros((n_concepts, n_states))
    effect_repertoires = np.zeros((n_concepts, n_states))
    for i, concept in enumerate(constellation):
        cause_repertoires[i] = concept.expand_cause_repertoire().flatten('F')
        effect_repertoires[i] = concept.expand_effect_repertoire().flatten('F')

    # Find the one cause state and two effect states with greatest variance
    cause_variance = np.var(cause_repertoires, 0)
    effect_variance = np.var(effect_repertoires, 0)
    cause_arg = cause_variance.argsort()[-1:]
    effect_arg = effect_variance.argsort()[-2:]

    # Set of points in cause-effect space and their size (phi)
    x = effect_repertoires[:, effect_arg[0]]
    y = effect_repertoires[:, effect_arg[1]]
    z = cause_repertoires[:, cause_arg[0]]
    size = [concept.phi for concept in constellation]

    # Initialize plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Turn off grid background
    ax.axis('off')

    # Draw axes anchor at the origin
    ax1 = (0, 0)
    ax3 = (0, 1)

    # Plan axis colors
    if color_code_axes:
        x_ax_color = y_ax_color = 'green'
        z_ax_color = 'blue'
    else:
        x_ax_color = y_ax_color = z_ax_color = 'black'

    # Draw axes
    ax.plot(ax1, ax1, ax3, z_ax_color, linewidth=2, zorder=0.3)
    ax.plot(ax1, ax3, ax1, y_ax_color, linewidth=2, zorder=0.3)
    ax.plot(ax3, ax1, ax1, x_ax_color, linewidth=2, zorder=0.3)

    # Label axes with states
    if label_axes:
        xs = (1, -0.1, -0.1)
        ys = (-0.1, 1, -0.1)
        zs = (-0.1, -0.1, 1)
        dirs = ('x', 'y', 'z')

        x_ax_state = loli_index2state(effect_arg[0], n_nodes)
        y_ax_state = loli_index2state(effect_arg[1], n_nodes)
        z_ax_state = loli_index2state(cause_arg[0], n_nodes)

        x_ax_label = r'${}^f$'.format(fmt.state(x_ax_state, node_labels=node_labels, sep=sep))
        y_ax_label = r'${}^f$'.format(fmt.state(y_ax_state, node_labels=node_labels, sep=sep))
        z_ax_label = r'${}^p$'.format(fmt.state(z_ax_state, node_labels=node_labels, sep=sep))

        ax_labels = [x_ax_label, y_ax_label, z_ax_label]
        for S, D, X, Y, Z in zip(ax_labels, dirs, xs, ys, zs):
            ax.text(X, Y, Z, S, D)

    # Add appropriately sized concepts
    for i in range(n_concepts):
        ax.scatter(x[i], y[i], z[i], s=size[i]*1000, marker=u"*", c=u'yellow', zorder=0.1)

    # Set the ticks for the grid on the plot, no tick labels
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_zticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    # Set the size of the space
    ax.set_zlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)

    # Default view in elevation and azimuth angle
    ax.view_init(elev=25, azim=0)

    # Make actual axes and ticks invisible - using homemade axes
    ax.w_xaxis.line.set_color((1, 1, 1, 0))
    ax.w_yaxis.line.set_color((1, 1, 1, 0))
    ax.w_zaxis.line.set_color((1, 1, 1, 0))
    ax.tick_params(colors=(1, 1, 1, 0))

    # Label stars with their mechanisms
    if label_stars:
        star_labels = [] # Holds matplotlib annotation objects
        for i in range(n_concepts):
            # Get 2d projection (think "screen coordinates") of the star, since
            # there's no direct way in matplotlib to annotate a 3D point.
            x2d, y2d, _ = proj3d.proj_transform(x[i], y[i], z[i], ax.get_proj())
            # Get the mechanism's label
            node_labels, _ = fmt.parse_spec(constellation[0], 'A,')
            mech_node_labels = [node_labels[x] for x in constellation[i].mechanism]
            mech_label = ','.join(mech_node_labels)
            # plot and save the label
            label = ax.annotate(mech_label, xy=(x2d, y2d), xytext=(10, 10),
                                textcoords='offset points')
            star_labels.append(label)

        # This callback will update the label positions if the user changes
        #   the plot's perspective interactively.
        def update_star_labels(event):
            for i in range(n_concepts):
                x2d, y2d, _ = proj3d.proj_transform(x[i], y[i], z[i], ax.get_proj())
                star_labels[i].xy = x2d, y2d
                star_labels[i].update_positions(fig.canvas.renderer)
            fig.canvas.draw()

        # Register the callback
        fig.canvas.mpl_connect('button_release_event', update_star_labels)

    # Show plot
    plt.show()

# adapted from http://stackoverflow.com/questions/24659005/
class ConstellationRadar(object):
    """A radarchart used to plot constellations.

    Examples:
        >>> fig = matplotlib.pyplot.figure()
        >>> titles = ['00p', '01p', '10p', '11p', '00f', '01f', '10f', '11f']
        >>> radar = ConstellationRadar(fig, titles)

    Args:
        fig (matplotlib.Figure): The figure on which to plot.
        titles (list(str)): The state labels used to title each spoke.

    Keyword args:
        ticks (list(float)): The probability values to grid on the plot. 0 and 1
            are done automatically. Default [0.25, 0.5, 0.75]
        rect (list(int)): A rectangle specifying where on the figure to plot.
            Format is [left_border, bottom_border, width, height].
    """
    def __init__(self, fig, titles, ticks=[.25, .5, .75], rect=None):
        if rect is None:
            rect = [0.1, 0.1, 0.8, 0.8]

        self.n = len(titles)
        self.angles = np.arange(0, 360, 360.0/self.n)
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i)
                         for i in range(self.n)]

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles, labels=titles)
        self.ax.set_yticks(ticks)

        for ax in self.axes[1:]:
            ax.set_yticks([])
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(ticks, angle=angle, labels=[])
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, 1)

        self.ax.set_rgrids(ticks, angle=self.angles[0], labels=ticks)

    def plot(self, values, *args, **kw):
        """Plot a concept's cause-effect repertoire on the radarchart.

        Examples:
            >>> full_rep = np.hstack([cause_rep, effect_rep])
            >>> radar.plot(full_rep, '-', lw=2, label=mechanism_label)

        Args:
            values (np.ndarray): A flat array of state probabilitites, given in
                the same order as the `titles` argument to the ConstellationRadar
                constructor.

        Also takes standard matplotlib linespec arguments, such as color, style,
            linewidth, etc.
        """
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)

def plot_radar_constellation(constellation, state_fmt='A'):
    """Plot a constellation using a radarchart.

    Examples:
        >>> big_mip = pyphi.compute.big_mip(sub)
        >>> plot_radar_constellation(big_mip)

    Args:
        constellation (list(pyphi.models.Concept)): A list of concepts to plot.

    Keyword args:
        state_fmt (str): Specifies how the states will be printed. If the string
            begins with a 1, the binary reperestation will be used. If the string
            beings with an alphabetic character, node labels will be used. If a
            ',' is present, element names will be separated when printing.
    """
    # Uses labels and no separation
    sub = constellation[0].subsystem
    n_nodes = sub.size
    n_states = 2 ** n_nodes
    n_concepts = len(constellation)

    node_labels, sep = fmt.parse_spec(constellation[0], state_fmt)
    states = [holi_index2state(i, n_nodes) for i in range(n_states)]
    state_labels = [fmt.state(state, node_labels=node_labels, sep=sep) for state in states]
    cause_labels = [r'${}^p$'.format(state_label) for state_label in state_labels]
    effect_labels = [r'${}^f$'.format(state_label) for state_label in state_labels]
    titles = cause_labels + effect_labels

    fig = plt.figure()
    radar = ConstellationRadar(fig, titles)

    highest_phi = max([constellation[i].phi for i in range(n_concepts)]) # for normalization
    for i in range(n_concepts):
        cause_repertoire = constellation[i].expand_cause_repertoire().flatten()
        effect_repertoire = constellation[i].expand_effect_repertoire().flatten()
        full_rep = np.hstack([cause_repertoire, effect_repertoire])
        mech_node_labels = [node_labels[x] for x in constellation[i].mechanism]
        mech_label = ','.join(mech_node_labels)
        relative_strength = constellation[i].phi / highest_phi
        radar.plot(full_rep, "-", lw=relative_strength * 5,
                   alpha=relative_strength * 0.5, label=mech_label)

    radar.ax.legend(bbox_to_anchor=(1.25,1.05))
    plt.show()
