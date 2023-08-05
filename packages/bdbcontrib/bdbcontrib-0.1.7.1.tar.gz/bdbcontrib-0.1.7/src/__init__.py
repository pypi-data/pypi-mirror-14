# -*- coding: utf-8 -*-

#   Copyright (c) 2010-2016, MIT Probabilistic Computing Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Main bdbcontrib API.

The bdbcontrib module serves a sandbox for experimental and semi-stable
features that are not yet ready for integreation to the bayeslite repository.
"""

from bql_utils import cardinality
from bql_utils import cursor_to_df
from bql_utils import describe_generator
from bql_utils import describe_generator_columns
from bql_utils import describe_generator_models
from bql_utils import describe_table
from bql_utils import df_to_table
from bql_utils import nullify
from bql_utils import table_to_df
from bql_utils import query

from diagnostic_utils import estimate_kl_divergence
from diagnostic_utils import estimate_log_likelihood

from version import __version__

def draw_crosscat(*args, **kwargs):
    import crosscat_utils
    draw_crosscat = crosscat_utils.draw_crosscat
    return draw_crosscat(*args, **kwargs)

def plot_crosscat_chain_diagnostics(*args, **kwargs):
    import crosscat_utils
    plot_crosscat_chain_diagnostics = \
        crosscat_utils.plot_crosscat_chain_diagnostics
    return plot_crosscat_chain_diagnostics(*args, **kwargs)

def barplot(*args, **kwargs):
    import plot_utils
    barplot = plot_utils.barplot
    return barplot(*args, **kwargs)

def heatmap(*args, **kwargs):
    import plot_utils
    heatmap = plot_utils.heatmap
    return heatmap(*args, **kwargs)

def histogram(*args, **kwargs):
    import plot_utils
    histogram = plot_utils.histogram
    return histogram(*args, **kwargs)

def mi_hist(*args, **kwargs):
    import plot_utils
    mi_hist = plot_utils.mi_hist
    return mi_hist(*args, **kwargs)

def pairplot(*args, **kwargs):
    import plot_utils
    pairplot = plot_utils.pairplot
    return pairplot(*args, **kwargs)

__all__ = [
    # bql_utils
        'cardinality',
        'cursor_to_df',
        'describe_generator',
        'describe_generator_columns',
        'describe_generator_models',
        'describe_table',
        'df_to_table',
        'nullify',
        'table_to_df',
        'query',
    # crosscat_utils
        'draw_crosscat',
        'plot_crosscat_chain_diagnostics',
    # diagnostic_utils
        'estimate_kl_divergence',
        'estimate_log_likelihood',
    # plot_utils
        'barplot',
        'heatmap',
        'histogram',
        'mi_hist',
        'pairplot',
    # version
        '__version__',
]
