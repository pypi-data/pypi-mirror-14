# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of dreamtools software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://github.com/dreamtools
#
############################################################################### -*- python -*-
import copy
import os
import json

import numpy as np
import pylab
import pandas as pd

from . import submissions
from dreamtools.core.sageutils import Login

from .scoring import HPNScoringPrediction
from .scoring import HPNScoringPredictionInsilico
from .scoring import HPNScoringNetwork
from .scoring import HPNScoringNetworkInsilico
from . import commons

from dreamtools.dream8.D8C1 import d8c1path
from dreamtools.dream8.D8C1 import scoring


__all__ = ["SC2AggregationPlotting", "SC2A_aggregation", "SC2B_aggregation",
    "SC1AggregationPlotting", "SC1A_aggregation", "SC1B_aggregation"]


class AggregationTools(Login):
    """common class to be used for the aggregation performances

    .. warning:: cannot be used by itself. You should use
    :class:`SC1A_aggregation` for instance.


    """
    def __init__(self, name, client=None, version=2):
        assert name in ["SC1A", "SC1B", "SC2A", "SC2B"]
        self.name = name
        super(AggregationTools, self).__init__(client=client)
        self.mode = "mean"
        self.version = version

    def load_submissions(self):
        """Load all submissions"""
        if self.name == "SC1A":
            s = submissions.SC1ASubmissions(client=self.client)
        elif self.name == "SC1B":
            s = submissions.SC1BSubmissions(client=self.client)
        elif self.name == "SC2A":
            s = submissions.SC2ASubmissions(client=self.client, version=self.version)
        elif self.name == "SC2B":
            s = submissions.SC2BSubmissions(client=self.client, version=self.version)

        s.load_submissions()
        self.submissions = s.submissions[:]

    def get_best_submissions(self, N, start=0):
        """Return the N best submissions"""
        ranking = [this['ranking'] for this in self.submissions]
        indices = np.argsort(ranking)[start:N]
        subs = [self.submissions[i] for i in indices]
        return subs

    def aggregate_submissions(self, N, start=0):
        """Get the N best submissions and average them

        a method called :meth:`_aggregate` must be defined in the child class

        """
        aggregate = self._aggregate(range(start,N))
        return aggregate

    def aggregate_submissions_random(self, N=10):
        """Aggregate N submissions by picking

        a method called :meth:`_aggregate` must be defined in the child class

        """
        # select N random submissions
        indices = list(range(0, len(self.df.index)))
        pylab.shuffle(indices)
        indices = indices[0:N]
        aggregate = self._aggregate(indices)
        return aggregate

    def get_df_from_submissions(self):
        subs = self.submissions
        df = pd.DataFrame()
        df['submitterAlias'] = [this['submitterAlias'] for this in subs]

        df['userId'] = [this['userId'] for this in subs]
        df['entityId'] = [this['entityId'] for this in subs]
        df['submissionId'] = [this['id'] for this in subs]

        if self.name == "SC1A":
            df['mean_rank'] = [this['ranking'] for this in subs]
            df['mean_auc'] = [this['mean_aucs'] for this in subs]
            df['mean_zscore'] = [this['zscore'] for this in subs]

            df['ranks'] = [this['ranks'] for this in subs]
            df['aucs'] = [this['aucs'] for this in subs]
            df['zscores'] = [this['zscores'] for this in subs]

        if self.name == "SC1B":
            df['auc'] = [this['auc'] for this in subs]
            df['mean_auc'] = [this['auc'] for this in subs]
            df['zscore'] = [this['zscore'] for this in subs]

        if self.name == "SC2A":
            df['mean_rank'] = [this['ranking'] for this in subs]
            df['mean_rmse'] = [this['mean_rmse'] for this in subs]
            df['mean_zscore'] = [this['zscore'] for this in subs]

            df['ranks'] = [this['ranks'] for this in subs]
            df['rmses'] = [this['rmses'] for this in subs]
            df['zscores'] = [this['zscores'] for this in subs]

        if self.name == "SC2B":
            df['mean_rank'] = [this['ranking'] for this in subs]
            df['mean_rmse'] = [this['mean_rmse'] for this in subs]
            df['zscore'] = [this['zscore'] for this in subs]
            df['rmses'] = [this['rmses'] for this in subs]

        try:
            get_filename = lambda sub: json.loads(sub['entityBundleJSON'])['fileHandles'][0]['fileName']
            prefix = os.sep.join([d8c1path, 'submissions', self.name.lower() ])
            df['filename'] = [prefix+ os.sep + get_filename(this) for this in subs]
        except:
            df['filename'] = [this['filename'] for this in subs]

        if self.name == "SC1A" or self.name == "SC2A":
            try:
                df.sort_values(by="mean_rank", inplace=True)
            except:
                df.sort(columns="mean_rank", inplace=True)
        elif self.name == "SC1B":
            try:
                df.sort_values(by="auc", ascending=False, inplace=True)
            except:
                df.sort(columns="auc", ascending=False, inplace=True)
        elif self.name == "SC2B":
            try:
                df.sort_values(by='mean_rmse', ascending=True, inplace=True)
            except:
                df.sort(columns='mean_rmse', ascending=True, inplace=True)

        df.reset_index(inplace=True)
        return df

    def _load_submissions_from_synapse(self):
        """To be used only onece to obtain all relevant metadata

        A way to check that ranks are correct is:

        for i in range(0,74):
            ranks = df.set_index("submitterAlias")['ranks'][i]
            print(mean([ranks[k1][k2] for k1 in ranks.keys() for k2 in
            ranks[k1].keys()]) == df['mean_rank'][i])

        """
        self.load_submissions()
        df = self.get_df_from_submissions()
        return df


class SC1AggregationPlotting(object):
    """ABC class plotting common to SC2A_aggregation and SC2B_aggregation."""

    def __init__(self):
        pass

    def plot_aggr_best_score(self, M=None, marker='o', color="r",
                             markersize=6):
        """Plots scores of the aggregation of the best submissions

        The submissionsfor selected are those found in the range 0
        to M. The scores of the individual submissions are also plotted.

        :param m: use the M th best solutions

        .. seealso:: :class:`SC1A_aggregation`

        .. note:: the curve that shows the aggregation of the submissions is
            shifted by +1 on the x-axis since it must have at least 2
            submissions to aggregate.

        .. note:: takes about 250 seconds

        """
        if M is None:
            M = len(self.df.index)
        if M>len(self.df.index):
            M = len(self.df.index)

        mean_aucs = []
        span = range(1, M+1)

        # used by paper module.
        self.results = []
        for i in span:
            aggr = self.aggregate_submissions(i, start=0)
            aggr.compute_score()
            mu = self.compute_grand_mean_auc(aggr.auc)
            mean_aucs.append(mu)
            print(i, mu)
            self.results.append(aggr.auc)

        self._mean_auc = mean_aucs[:]
        self._best_results = {'x': span}
        # those are the best submitter. Nothing to recompute, can be extracted
        # from the df itself.

        iauc = [self.df.ix[x].mean_auc for x in range(0, M)]

        pylab.clf()
        pylab.plot(span, iauc, marker+color, markersize=markersize,
                   label="AUC (individual submissions)")
        pylab.plot(span, mean_aucs, 'x-',
                   label="{} aggregation (over first N submissions)".format(self.mode))
        pylab.grid(True)
        self._best_results['aggregation'] = mean_aucs
        self._best_results['individual'] = iauc

        pylab.xlabel("N", fontsize=20)
        pylab.ylabel("AUROC", fontsize=20)
        pylab.title("Aggregated AUROC (best case)", fontsize=20)
        yr = pylab.ylim()
        pylab.axis([0.5, M+1, yr[0]-0.05, yr[1]+0.05])
        pylab.ylim([0.35, 0.86])
        pylab.legend(loc="lower left")
        return self._best_results

    def plot_aggr_random(self, N=5, Nmax=10,
                         marker="o", color="r", markersize=6, results=None):
        """
        :param N: repeat N times the aggregation to obtain some errors
        :param Nmax: takes at most N values randomly chosen

        .. image:: sc1a_aggregation_random.png
            :width: 50%

        ::

            >>> from dreamtools.dream8.D8C1 import aggregation
            >>> a = aggregation.SC1A_aggregation()
            >>> a.plot_aggr_random(N=100, Nmax=74)

        .. note:: takes about 300s to compute for N=1, Nmax=74 for SC1A
        """
        assert Nmax >= 1
        span = range(1, Nmax+1)
        if results!=None:
            self.results = results.copy()
        else:
            results = np.zeros((N, Nmax))
            for i,n in enumerate(range(0, N)):
                print("Replicate %s" % (i+1) )
                for j, nmax in enumerate(range(1, Nmax+1)):
                    print('----'+str(j))
                    aggr = self.aggregate_submissions_random(nmax)
                    aggr.compute_score()
                    mu = self.compute_grand_mean_auc(aggr.auc)
                    results[i][j] = mu

            self.results = results
        #mean_aucs = results.mean(axis=0)

        self._plot_aggr_random(span, Nmax, markersize=markersize,
                                      marker=marker, color=color)
        return self._random_results

    def _plot_aggr_random(self, span, Nmax, marker='o', color='r', markersize=6):
        # those are the best submitter. Nothing to recompute, can be extracted
        # from the df itself.
        iauc = [self.df.ix[x].mean_auc for x in range(0, Nmax)]

        pylab.clf()
        pylab.plot([x for x in span], iauc, marker+color, markersize=markersize,
                   label="AUC (individual submissions)".format(self.mode))
        pylab.grid(True)
        #pylab.plot()
        pylab.xlabel("N", fontsize=20)
        pylab.ylabel("AUROC", fontsize=20)
        pylab.title("Aggregated AUROC (random case)", fontsize=20)

        pylab.errorbar(span, self.results.mean(axis=0), self.results.std(axis=0),
                       label="{} aggregation (over N submissions)".format(self.mode))
        pylab.legend(loc="lower left")

        self._random_results = {}
        self._random_results['x'] = span
        self._random_results['individual'] = iauc
        self._random_results['aggregation_mean'] = list(self.results.mean(axis=0))
        self._random_results['aggregation_std'] = list(self.results.std(axis=0))
        self._random_results['aggregation_all'] = [list(x) for x in self.results]

        xmax = pylab.xlim()[1]
        pylab.ylim([0.35, 0.86])
        pylab.xlim(0.5, xmax)

    def compute_grand_mean_auc(self, data):
        if isinstance(data, dict):
            return np.mean([data[k1][k2] for k1 in data.keys()
                for k2 in data[k1].keys() if k2
                in self.valid_ligands_final[k1]])
        else:
            return data


class SC2AggregationPlotting(object):
    """ABC class plotting common to SC2A_aggregation and SC2B_aggregation."""
    def __init__(self):
        pass

    def plot_aggr_best_score(self, N=2):
        """plots aggregation using best N submissions

        .. seealso:: :class:`SC2A_aggregation`

        """
        self._best_results= {}
        assert N>=2
        if N > len(self.df.index):
            N = len(self.df.index)
        mean_rmses = []

        span = range(1, N+1)
        for i in span:
            aggr = self.aggregate_submissions(i)
            aggr.compute_all_rmse()
            rmse = self._get_mean_rmse(aggr.rmse)
            mean_rmses.append(rmse)
            print(i, rmse)

        iauc = [self.df.ix[x].mean_rmse for x in range(0,N)]

        pylab.clf()
        pylab.plot(span, mean_rmses, 'x-', label="first N aggregation")
        pylab.grid(True)

        newspan = [x for x in span]

        self._best_results['aggregation'] = mean_rmses
        self._best_results['individual'] = iauc


        pylab.plot(newspan, iauc, 'or', label="individual mean RMSE")
        pylab.xlabel("N", fontsize=20)
        pylab.ylabel("RMSE", fontsize=20)
        pylab.title("RMSE for the first N best submissions", fontsize=20)

        pylab.legend(loc="upper left")
        return self._best_results

    def plot_aggr_random(self, N=5, Nmax=14):
        """plots aggregation using N random submissions

        .. seealso:: :class:`SC2A_aggregation`

        """
        mean_aucs = []

        assert Nmax>=1
        span = range(1, Nmax+1)
        results = np.zeros((N, Nmax))
        for i,n in enumerate(range(0,N)):
            print("Replicate %s" %i )
            for j,nmax in enumerate(range(1, Nmax+1)):
                aggr = self.aggregate_submissions_random(nmax)
                aggr.compute_all_rmse()
                results[i][j] = self._get_mean_rmse(aggr.rmse)
        self.results = results

        mean_aucs = results.mean(axis=0)

        iauc = [self.df.ix[x].mean_rmse for x in range(0,Nmax)]
        #newspan = [x+1.5 for x in range(start,start+Nmax)]

        pylab.clf()
        self.results = results

        pylab.plot(span, mean_aucs, 'x-', label="Random aggregation ({}) for each N".format(N))
        pylab.grid(True)
        pylab.plot([x for x in span], iauc, 'or', label="individual mean RMSE")

        pylab.xlabel("N", fontsize=20)
        pylab.ylabel("{} RMSE".format(self.mode), fontsize=20)
        pylab.title("{} RMSE using N random submissions".format(self.mode), fontsize=20)
        pylab.errorbar(range(1,Nmax+1), results.mean(axis=0), results.std(axis=0))
        pylab.legend(loc="upper left")
        return iauc


class SC1A_aggregation(AggregationTools, SC1AggregationPlotting):
    """Investigating the aggregation over several teams.

    ::

        >>> from dreamtools.dream8.D8C1 import aggregation
        >>> a = aggregation.SC1A_aggregation()
        >>> a.plot_aggr_random(N=100, Nmax=74)

    By default, uses the submissions from the challenge itself (up to week 9)

    You need to download the file before hand:

    2 regimes ignored while doing the scoring/aggregation.

    """
    valid_ligands_final = commons.valid_ligands_final
    def __init__(self, best=2, client=None, version=None):
        """

        :param best: default to 2
        :param client: an existing synapse client
        :param submissions: list of submissions already downloaded. Otherwise
            reload all of them
        :param startweek: default is begining of the challenge (week 1)
        :param endweek: default is end of the challenge (week 9)

        """
        super(SC1A_aggregation, self).__init__(name="SC1A", client=client)
        self.best = 2
        self.startweek = 1
        self.endweek = 9

        self._individuals = {}
        self.directory = os.sep.join([d8c1path, 'submissions', 'sc1a'])


        self.df = self._load_submissions_from_synapse()

        scoring = HPNScoringNetwork()
        self.true_descendants = copy.deepcopy(scoring.true_descendants)

    def remove_correlated_submissions(self):
        teams = ['AHAT', 'NIPL', 'T4', 'Taylor Swift', 'Hatric',
                'ScreamingGoats', 'dftt', 'bdalab']

        self.submissions = [sub for sub in self.submissions if
            sub['submitterAlias'] not in teams]

        self.df = self.get_df_from_submissions()

    def _get_seed_aggregate(self, index):
        if index in self._individuals.keys():
            aggregate = copy.deepcopy(self._individuals[index])
        else:
            filename = self.df.ix[index].filename
            aggregate = HPNScoringNetwork(filename=filename,
                                          true_descendants=self.true_descendants)
            try:
                # to allow a deepcopy
                del aggregate.zip_data
            except:
                pass
            self._individuals[index] = copy.deepcopy(aggregate)
        return aggregate

    def _aggregate(self, subs):
        # let us pick up one submissions and score it just to get the data
        # structure. Could be saved once for all ?

        aggregate = self._get_seed_aggregate(subs[0])
        edge_scores = {'BT20':{}, 'BT549':{}, 'MCF7':{}, 'UACC812':{}}
        for c in aggregate.edge_scores.keys():
            for l in aggregate.edge_scores[c].keys():
                edge_scores[c][l] = [aggregate.edge_scores[c][l]]

        if len(subs)>1:
            for sub in subs[1:]:
                if sub in self._individuals.keys():
                    individual = copy.deepcopy(self._individuals[sub])
                else:
                    filename =self.df.ix[sub].filename
                    individual = HPNScoringNetwork(filename=filename,
                        true_descendants=self.true_descendants)
                    del individual.zip_data
                    self._individuals[sub] = copy.deepcopy(individual)
                for c in aggregate.edge_scores.keys():
                    for l in aggregate.edge_scores[c].keys():
                        #aggregate.edge_scores[c][l] += individual.edge_scores[c][l]
                        edge_scores[c][l].append(individual.edge_scores[c][l])

                        if edge_scores[c][l][0].max()>1:
                            print(c,l,edge_scores[c][l][0].max())

        for c in aggregate.edge_scores.keys():
            for l in aggregate.edge_scores[c].keys():
                if self.mode == "mean":
                    #aggregate.edge_scores[c][l] /= float(N)
                    aggregate.edge_scores[c][l] = np.mean(edge_scores[c][l], axis=0)
                elif self.mode == "median":
                    aggregate.edge_scores[c][l] = np.median(edge_scores[c][l], axis=0)
        self._edge_scores = edge_scores.copy()
        return aggregate

    def plot_aggregate_edge_rank(self, N=None, ss=None, method="min"):
        """

        See paper for the vectors of aggregsation (best weighted scores)
        and submissions AUCs

        Then chose a method and loop over this function::

            auc_min = []
            for i in range(0,74):
                es = s.plot_aggregate_edge_rank(i, ss=ss)
                print(es)
                auc_min.append(es)
            plot(auc, label="min")

        with 66 submissions, and method=min we reach 84%
        """

        # first does not really work
        assert method in ["average", "max", "min", "first"]

        # first, we need to load all edge scores.
        if ss is None:
            print("loading a scoring function")
            filename = os.sep.join([d8c1path, 'submissions', 'sc1a', 'DC_GFP-Network.zip'])
            ss = HPNScoringNetwork(filename, true_descendants=self.true_descendants)
        else:
            pass

        if N is None:
            N = len(self.submissions)

        print("Loading all edge scores")
        for sub in range(0, N):
            if sub in self._individuals.keys():
                pass
            else:
                filename = self.df.ix[sub].filename
                individual = HPNScoringNetwork(filename=filename,
                                               true_descendants=self.true_descendants)
                self._individuals[sub] = copy.deepcopy(individual)

        print("Extracting the edge ranks")
        edge_scores = {'BT20':{}, 'BT549':{}, 'MCF7':{}, 'UACC812':{}}
        for sub in range(0, N):
            for c in self.valid_ligands_final.keys():
                for l in self.valid_ligands_final[c]:
                    data = self._individuals[sub].edge_scores[c][l].copy()
                    shape = data.shape
                    ts = pd.TimeSeries(data.flatten())
                    ranks = ts.rank(ascending=True, method=method).as_matrix().reshape(shape)
                    try:
                        edge_scores[c][l].append(ranks)
                    except:
                        edge_scores[c][l] = [ranks]

        print("averaging")
        for c in edge_scores.keys():
            for l in edge_scores[c].keys():
                if self.mode == "mean":
                    #aggregate.edge_scores[c][l] /= float(N)
                    edge_scores[c][l] = np.mean(edge_scores[c][l], axis=0)
                elif self.mode == "median":
                    edge_scores[c][l] = np.median(edge_scores[c][l], axis=0)

        ss.descendancy_matrices = dict([(x,{}) for x in ss.valid_cellLines])
        for c in edge_scores.keys():
            for l in edge_scores[c].keys():
                ss.edge_scores[c][l] = edge_scores[c][l].copy()
        ss.compute_all_aucs()
        return ss.get_auc_final_scoring(), ss


class SC1B_aggregation(AggregationTools, SC1AggregationPlotting):
    """Investigating the aggregation over several teams.

    ::

        >>> from dreamtools.dream8.D8C1 import aggregation
        >>> a = aggregation.SC1B_aggregation()
        >>> a.plot_aggr_random(N=100, Nmax=5)

    By default, uses the submissions from the challenge itself (up to week 9)


    """
    def __init__(self, best=2, client=None, version=None):
        """

        :param best:
        :param client: an existing synapse client
        :param submissions: list of submissions already downloaded. Otherwise
            reload all of them
        :param startweek: default is begining of the challenge (week 1)
        :param endweek: default is end of the challenge (week 9)

        """
        super(SC1B_aggregation, self).__init__(name="SC1B", client=client)
        self.best = 2

        self._individuals = {}

        self.directory = os.sep.join([d8c1path, 'submissions', 'sc1b'])

        self.df = self._load_submissions_from_synapse()

    def remove_correlated_submissions(self):
        # same  as in SC1A actually...
        teams = ['AHAT', 'NIPL', 'T4', 'Taylor Swift', 'Hatric',
                'ScreamingGoats', 'dftt', 'bdalab']

        self.submissions = [sub for sub in self.submissions if
            sub['submitterAlias'] not in teams]
        self.df = self.get_df_from_submissions()

    def _get_seed_aggregate(self, index):
        if index in self._individuals.keys():
            aggregate = copy.deepcopy(self._individuals[index])
        else:
            filename = self.df.ix[index].filename
            aggregate = HPNScoringNetworkInsilico(filename=filename)
            try:
                del aggregate.zip_data
            except:
                pass
            self._individuals[index] = copy.deepcopy(aggregate)
        return aggregate

    def _aggregate(self, subs):
        # let us pick up the first submissions and score it just to get the data
        # structure.
        aggregate = self._get_seed_aggregate(subs[0])
        user_graph = []
        user_graph.append(aggregate.user_graph)

        if len(subs)>1:
            for sub in subs[1:]:
                if sub in self._individuals.keys():
                    individual = copy.deepcopy(self._individuals[sub])
                else:
                    filename =self.df.ix[sub].filename
                    individual = HPNScoringNetworkInsilico(filename=filename)
                    try:
                        del individual.zip_data
                    except:
                        pass
                    self._individuals[sub] = copy.deepcopy(individual)
                user_graph.append(individual.user_graph)
        if self.mode == "mean":
            aggregate.user_graph = np.mean(np.array(user_graph), axis=0)
        elif self.mode == "median":
            aggregate.user_graph = np.median(np.array(user_graph), axis=0)
        return aggregate

    def _get_mean_auc2(self, aggr):
        # nothing special is done here. This is just for
        #the plot_aggr_best_score in sc1a and sc1b to be identical
        return aggr.get_auc()


class SC2A_aggregation(AggregationTools, SC2AggregationPlotting):
    """Investigating the aggregation over several teams.

    ::

        >>> from dreamtools.dream8.D8C1 import aggregation
        >>> a = aggregation.SC2A_aggregation()
        >>> a.plot_aggr_random(N=100, Nmax=14)

    By default, uses the submissions from the challenge itself (up to week 9)


    """
    def __init__(self, client=None, version=2):
        """.. rubric:: constructor

        :param best:
        :param client: an existing synapse client
        :param submissions: list of submissions already downloaded. Otherwise
            reload all of them

        """
        super(SC2A_aggregation, self).__init__(name="SC2A", client=client, version=version)

        self._individuals = {}

        self.directory = os.sep.join([d8c1path, 'submissions', 'sc2a'])

        self.df = self._load_submissions_from_synapse()


    def _get_seed_aggregate(self, index):
        if index in self._individuals.keys():
            aggregate = copy.deepcopy(self._individuals[index])
        else:
            filename = self.df.ix[index].filename
            aggregate = HPNScoringPrediction(filename=filename, version=self.version)
            try:
                del aggregate.zip_data  # not serialisable in py3
            except:
                pass
            self._individuals[index] = copy.deepcopy(aggregate)
        return aggregate

    def _aggregate(self, subs):
        # let us pick up the first submissions and score it just to get the data
        # structure.

        aggregate = self._get_seed_aggregate(subs[0])

        # store all data inside lists to be able to compute median
        values = aggregate.user_prediction.copy()
        for c in aggregate.user_prediction.keys():
            for l in aggregate.user_prediction[c].keys():
                if l not in aggregate.phosphos_to_exclude[c]:
                    for k in aggregate.user_prediction[c][l].keys():
                        values[c][l][k] = [aggregate.user_prediction[c][l][k]]

        if len(subs)>1:
            for sub in subs[1:]:
                if sub in self._individuals.keys():
                    individual = copy.deepcopy(self._individuals[sub])
                else:
                    filename = self.df.ix[sub].filename
                    individual = HPNScoringPrediction(filename=filename, version=self.version)
                    try:
                        del individual.zip_data
                    except:
                        pass
                    self._individuals[sub] = copy.deepcopy(individual)
                for c in aggregate.user_prediction.keys():
                    for l in aggregate.user_prediction[c].keys():
                        if l not in aggregate.phosphos_to_exclude[c]:
                            for k in aggregate.user_prediction[c][l].keys():
                                #data1 = aggregate.user_prediction[c][l][k]
                                data2 = individual.user_prediction[c][l][k]
                                #aggregate.user_prediction[c][l][k] = [x+y for x,y in zip(data1, data2)]
                                values[c][l][k].append(data2)

        for c in aggregate.user_prediction.keys():
            for l in aggregate.user_prediction[c].keys():
                if l not in aggregate.phosphos_to_exclude[c]:
                    for k in aggregate.user_prediction[c][l].keys():

                        if self.mode == "mean":
                            aggregate.user_prediction[c][l][k] = np.mean(values[c][l][k], axis=0)
                        elif self.mode=="median":
                            aggregate.user_prediction[c][l][k] = np.median(values[c][l][k], axis=0)
        return aggregate

    def _get_mean_rmse(self, data):
        d = data
        return np.nanmean([d[k1][k2] for k1 in d.keys() for k2 in d[k1].keys()])


class SC2B_aggregation(AggregationTools, SC2AggregationPlotting):
    """Investigating the aggregation over several teams.

    ::

        >>> from dreamtools.dream8.D8C1 import aggregation
        >>> a = aggregation.SC2B_aggregation()
        >>> a.plot_aggr_random(N=100, Nmax=5)

    By default, uses the submissions from the challenge itself (up to week 9)

    """
    def __init__(self, client=None, version=2):
        """

        :param client: an existing synapse client

        """
        super(SC2B_aggregation, self).__init__(name="SC2B", client=client, version=version)
        self._individuals = {}
        self.directory = os.sep.join([d8c1path, 'submissions', 'sc2b'])
        self.version = version

        self.df = self._load_submissions_from_synapse()

    def _get_seed_aggregate(self, index):
        if index in self._individuals.keys():
            aggregate = copy.deepcopy(self._individuals[index])
        else:
            filename = self.df.ix[index].filename
            aggregate = HPNScoringPredictionInsilico(filename=filename, version=self.version)
            #try:
            #    del aggregate.zip_data
            #except;
            #   pass
            self._individuals[index] = copy.deepcopy(aggregate)
        return aggregate

    def _aggregate(self, subs):
        # let us pick up the first submissions and score it just to get the data
        # structure.
        aggregate = self._get_seed_aggregate(subs[0])

        # store all data inside lists to be able to compute median
        values = aggregate.user_prediction.copy()
        for c in aggregate.user_prediction.keys():
            for l in aggregate.user_prediction[c].keys():
                for k in aggregate.user_prediction[c][l].keys():
                    values[c][l][k] = [aggregate.user_prediction[c][l][k]]

        if len(subs)>1:
            for sub in subs[1:]:
                if sub in self._individuals.keys():
                    individual = copy.deepcopy(self._individuals[sub])
                else:
                    filename = self.df.ix[sub].filename
                    individual = HPNScoringPredictionInsilico(filename=filename,
                                                              version=self.version)

                    try:
                        del individual.zip_data
                    except:
                        pass
                    self._individuals[sub] = copy.deepcopy(individual)
                for c in aggregate.user_prediction.keys():
                    for l in aggregate.user_prediction[c].keys():
                        for k in aggregate.user_prediction[c][l].keys():
                            #data1 = aggregate.user_prediction[c][l][k]
                            data2 = individual.user_prediction[c][l][k]
                            #aggregate.user_prediction[c][l][k] = [x+y for x,y in zip(data1, data2)]
                            values[c][l][k].append(data2)

        # now compute the mean
        for c in aggregate.user_prediction.keys():
            for l in aggregate.user_prediction[c].keys():
                for k in aggregate.user_prediction[c][l].keys():
                    #data = aggregate.user_prediction[c][l][k]
                    #aggregate.user_prediction[c][l][k] = [x/float(N) for x in data]
                    if self.mode == "mean":
                        aggregate.user_prediction[c][l][k] = np.mean(values[c][l][k], axis=0)
                    elif self.mode=="median":
                        aggregate.user_prediction[c][l][k] = np.median(values[c][l][k], axis=0)

        return aggregate

    def _get_mean_rmse(self, data):
        d = data
        return np.mean([d[k1][k2] for k1 in d.keys() for k2 in d[k1].keys() if
            np.isnan(d[k1][k2])==False])


# NOTE: filename do not match team name in some cases:
"""
                        u'AUTO-Network.zip': u'Auto',
                        u'CGR-Network.zip': u'CGR',
                        u'CMK-Network.zip': u'CMK4',
                        u'DC_GFP-Network.zip': u'DC_TDC',
                        u'DynamoBios-Network.zip': u'Dynamo Bios',
                        u'GoatTower-Network.zip': u'Goat Tower',
                        u'HD_Systems6-Network.zip': u'HD_Systems',
                        u'MA5-Network.zip': u'DoNET',
                        u'Reptar1-Network.zip': u'Reptar',
                        u'TaylorSwift-Network.zip': u'Taylor Swift',
                        u'Tongji-Network.zip': u'tongji team',
                        u'Try1-Network.zip': u'TEST-1roni',
                        u'guanlab18-Network.zip': u'GuanLab',
                        u'result.zip': u'ICHING',
                        u'sakev-Network.zip': u'sakev',
"""

"""
            'Bing(Cai)-Network-Insilico.zip': u'Cai',
             u'DC_GFInS-Network-Insilico.zip': u'DC_TDC',
             u'DynamoBios-Network-Insilico.zip': u'Dynamo Bios',
             u'GoatTower-Network-Insilico.zip': u'Goat Tower',
             u'Gupta2-Network-Insilico.zip': u'Gupta',
             u'HD_Systems7-Network-Insilico.zip': u'HD_Systems',
             u'MA1-Network-Insilico.zip': u'DoNET',
             u'TaylorSwift-Network-Insilico.zip': u'Taylor Swift',
             u'Tongji-Network-Insilico.zip': u'tongji team',
             u'UCSD_DING-Network-Insilico.zip': u'ding',
             u'WH-Network-Insilico.zip': u'WH',
             u'biomecis2-Network-Insilico.zip': u'Biomecis',
             u'guanlab18-Network-Insilico.zip': u'GuanLab',
             u'insilico.zip': u'ICHING',
"""


def create_all_aggregation_figures():

    # SC1A, best, mean
    sc1a = SC1A_aggregation()
    try:
        pylab.figure(1)
        pylab.clf()

        sc1a.plot_aggr_best_score()
        pylab.savefig("sc1a_aggregation_best_mean.png")
        pylab.savefig("sc1a_aggregation_best_mean.svg")
        pylab.savefig("sc1a_aggregation_best_mean.pdf")
    except:
        print("SC1A best mean failed")

    # SC1A, best, mean
    try:
        pylab.figure(2)
        pylab.clf()
        sc1a.mode = "median"
        sc1a.plot_aggr_best_score()
        pylab.savefig("sc1a_aggregation_best_median.png")
        pylab.savefig("sc1a_aggregation_best_median.svg")
        pylab.savefig("sc1a_aggregation_best_median.pdf")
    except:
        print("SC1A best median failed")


     # SC1A, random, mean
    sc1a = SC1A_aggregation()
    try:
        pylab.figure(1)
        pylab.clf()

        sc1a.plot_aggr_random()
        pylab.savefig("sc1a_aggregation_random_mean.png")
        pylab.savefig("sc1a_aggregation_random_mean.svg")
        pylab.savefig("sc1a_aggregation_random_mean.pdf")
    except:
        print("SC1A random mean failed")


    # SC1A, random, mean
    try:
        pylab.figure(2)
        pylab.clf()
        sc1a.mode = "median"
        sc1a.plot_aggr_best_score()
        pylab.savefig("sc1a_aggregation_random_median.png")
        pylab.savefig("sc1a_aggregation_random_median.svg")
        pylab.savefig("sc1a_aggregation_random_median.pdf")
    except:
        print("SC1A random median failed")
