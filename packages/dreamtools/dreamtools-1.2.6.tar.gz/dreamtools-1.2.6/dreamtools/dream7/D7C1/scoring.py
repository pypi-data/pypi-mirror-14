# -*- python -*-
#
#  This file is part of DREAMTools software
#
#  Copyright (c) 2014-2015 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://github.org/dreamtools
#
##############################################################################
"""DREAM7 Challenge 1 (Parameter estimation and network topology prediction)

:References:
    * http://dreamchallenges.org/project-list/dream7-2012/
    * https://www.synapse.org/#!Synapse:syn2821735/wiki/

:Publications: http://www.biomedcentral.com/1752-0509/8/13/abstract

"""
import os
import glob

import pandas as pd
import numpy as np

from dreamtools.core.challenge import Challenge


__all__ = ['D7C1']


class D7C1(Challenge):
    """DREAM 7 - Network Topology and Parameter Inference Challenge

    Here is a quick example on calling the scoring methods::

        from dreamtools import D7C1
        s = D7C1()
        s.score_model1_timecourse(filename)
        s.score_model1_parameters(filename)
        s.score_topology(filename)


    This class provides 3 main scoring functions:

    #. :meth:`score_topology`
    #. :meth:`score_model1_timecourse`
    #. :meth:`score_model1_parameters`

    Each takes as an input a valid submission as described in the official
    `synapse page <https://www.synapse.org/#!Synapse:syn2821735/wiki/>`_.

    Templates are also provided within the source code on `github dreamtools <https://github.com/dreamtools>`_
    in the directory dreamtools/dream7/D7C1/templates.

    D7C1 scoring function are also included in the standalone code **dreamtools-scoring**.

    For the details of the scoring functions, please refer to the paper (see module documentation)
    Some details are provided in the methods themselves as well.

    There are other methods (starting with leaderboard) that should not be used. Those are
    draft version used to compute pvalues and report scores as in the final leaderboard.

    .. note:: the scoring functions were implemented following Pablo Meyer's matlab **codescore_dream7_c1s1.m**

    For admin only: put the submissions in ./submissions/ directory and call the :meth:
    """

    def __init__(self, path='submissions'):
        """.. rubric:: constructor

        :param path: path to a directory containing submissions
        :return:
        """
        Challenge.__init__(self, challenge_name='D7C1')
        self.sub_challenges = ['parameter', 'topology', 'timecourse']

        self.path = path

        teams = glob.glob(path + os.sep +'*')
        self.teams = [this for this in teams if os.path.isdir(this) is True]

        self.N = len(self.teams)
        self.distances = np.zeros((self.N, 4))
        self.pvalues = np.zeros((self.N, 4))

        self.scores = {}
        self._load_gold_standard()

        #self.load_submissions()
        #self.compute_score_distance_model1()
        #self.compute_score_parameter_prediction_model1()
        #self.compute_score_topology()

        # data structure to store null distances
        self.rdistance_pred1 = []
        self.rdistance_param1 = []

    def download_template(self, name):
        """Return filename of a template

        :param str name: one in 'topology', 'parameter', 'timecourse'
        """
        if name == 'parameter':
            return self.getpath_template('model1_parameters_alphabeta.txt')
        elif name == 'topology':
            return self.getpath_template('network_topology_alphabeta.txt')
        elif name == 'timecourse':
            return self.getpath_template('model1_timecourse_alphabeta.txt')
        else:
            raise ValueError("Incorrect challenge name. Use one of %s " % self.sub_challenges)

    def load_submissions(self):
        """Load a bunch of submissions to be found in the submissions directory

        The directory name is defined in :attr:`path`

        :return: nothing. Populates :attr:`data` attribute and :attr:`team_names`.
        """

        tag_param1 = 'dream7_netparinf_parameters_model_1'
        tag_param2 = 'dream7_netparinf_parameters_model_2'
        tag_pred1 = 'dream7_netparinf_timecourse_model_1'
        tag_topo2 = 'dream7_netparinf_networktopo_model_2'

        self.data = {}
        self.data['param1'] = {}
        self.data['param2'] = {}
        self.data['pred1'] = {}
        self.data['topo2'] = {}
        self.team_names = []

        for team in self.teams:
            team_name = team.split(os.sep)[1]
            self.team_names.append(team_name)

            filename = team + os.sep + tag_param1 + '_' + team_name + '.txt'
            self.data['param1'][team_name] = self._read_df(filename, 'param')

            filename = team + os.sep + tag_param2 + '_' + team_name + '.txt'
            self.data['param2'][team_name] = self._read_df(filename, 'param')

            filename = team + os.sep + tag_pred1 + '_' + team_name + '.txt'
            self.data['pred1'][team_name] = self._read_df(filename, 'pred')

            filename = team + os.sep + tag_topo2 + '_' + team_name + '.txt'
            self.data['topo2'][team_name] = self._read_df(filename, 'topo')

    def _read_df(self, filename, mode, sep='\s+'):

        def error_message(msg):
            txt = 'Error while parsing %s\n' % filename
            txt += msg
            return txt
        if mode == 'param':
            df = pd.read_csv(filename, sep=sep, index_col=0,
                header=None, names=['values'])
        elif mode == 'pred':
            df = pd.read_csv(filename, sep=sep, index_col=0)
            assert all(df.columns == ['p3','p5','p8']), \
                error_message('Header columns  must be p3 p5 p8. Found %s' % df.columns)
        elif mode == 'topo':
            df = pd.read_csv(filename, sep=sep, index_col=None, header=None,
                    names=['regulator','sign1','g1','sign2','g2'])

        return df

    ###########################################################   standalone scoring functions:
    def score(self, filename, subname=None):
        """Return score for a given sub challenge

        :param str filename: input filemame.
        :return: name of a sub_challenge. See :attr:`sub_challenges` attribute.
        """
        if subname == 'parameter':
            score = self.score_model1_parameters(filename)
            pvalue = self.get_pvalues_parameter(score)
            over = -np.log10(pvalue)
            return {'score':score,  'pvalue':pvalue, 'overallScore':over}
        elif subname == 'timecourse':
            score = self.score_model1_timecourse(filename)
            pvalue = self.get_pvalues_timecourse(score)
            over = -np.log10(pvalue)
            return {'score':score,  'pvalue':pvalue, 'overallScore':over}
        elif subname == 'topology':
            print("Note: Null distribution used to compute p-value and overall score is stochastic " +
                  "but should be close to the one used in the official LB.\n")
            score =  self.score_topology(filename)
            pvalue = self.get_pvalues_topology(score)
            over = -np.log10(pvalue)
            return {'score':score,  'pvalue':pvalue, 'overallScore':over}

        else:
            raise ValueError("Incorrect challenge name. Use one of %s " % self.sub_challenges)

    def score_model1_parameters(self, filename):
        r"""Return distance between submission and gold standard for parameters challenge (model1)

        :param filename: must be valid templates
        :return: score (distance)


        ::

            >>> from dreamtools import D7C1
            >>> s = D7C1()
            >>> filename = s.download_template('parameter')
            >>> s.score(filename, 'parameter')
            0.022867555017785129


        The score is computed using the square of the ratio of the user prediction and the gold standard.
        Taking the mean of the log10 :

        .. math::

            S = \overline{\log10 \left( \left( \frac{X}{X_{\rm{gold\;standard}}} \right)^2\right)}


        """
        data = self._read_df(filename, mode='param')
        distance = self._compute_score_model1_parameters(data)
        return distance

    def score_model1_timecourse(self, filename):
        r"""Returns distance between prediction and gold standard (model1)


        :param filename: must be valid templates
        :return: score (distance)

        ::

            >>> from dreamtools import D7C1
            >>> s = D7C1()
            >>> filename = s.download_template('timecourse')
            >>> s.score_model1_timecourse(filename)
            0.0024383612676804048


        There are 3 time courses to be predicted.
        The score for each time course is

        .. math::

            S_i = \frac{(X_i - \hat{X_i}) ^ 2}{0.01 + 0.04 * X_i^2}

        where :math:`X` is the gold standard and :math:`\hat{X}` the prediction.
        and final score is just the average across the 3 time courses.

        """
        data = self._read_df(filename, mode='pred')
        distance = self._compute_score_timecourse_model1(data, 10,39)
        return distance

    def score_topology(self, filename):
        """Standalone version of the network topology scoring

        :param str filename:

        ::

            >>> from dreamtools import D7C1
            >>> s = D7C1()
            >>> filename = s.download_template('topology')
            >>> s.score(filename, 'topology')
            12


        :scoring details:

            The challenge requests predictions for 3 missing links, knowing that
            a gene can regulate up to two genes when they are in the same operon,
            6 gene interactions have to be indicated by the participants (3 links*2 genes)
            and whether these interactions are activating (+) or repressing (-).

            For each of the predicted links i=1,2,3, we define a score:

            :math:`S_i^{link} = L_i + N_i`

            where :math:`L_j` is 6 if the nature of
            the regulation iscorrect (that is, the source gene, the sign of the connection, and
            the destination gene are all correct) and :math:`L_i = 12` if the link
            regulates an operon composed of two genes and both connections are
            correct. If :math:`L_i >0` then :math:`N_i=0`.

            In case a link is NOT correctly predicted (:math:`L_i=0`) :math:`N_i`
            is defined as follows. It is increased by 1 for each correctly
            regulated gene, 2 if the regulated gene and the nature of the
            regulation (i.e +/-) are correct and 1 if the regulator gene is
            correct


            The gold standard contains 3 lines similar to ::

                5 + 7 + 11

            It means gene 5 positively regulates gene 7 and gene 11.  If a prediction is ::

                5 + 7 + 2

            Then L =6. If the prediction is ::

                2 + 7 + 2

            L = 0 so N may be updated. Here the regulon (2) is not correct, However, one gene (7) is correctly predicted
            with the good sign so N = 2.

        """
        data = self._read_df(filename, mode='topo')
        distance = self._compute_score_topology(data)
        return distance

    ##################################################################### Load gold standard files
    def download_goldstandard(self, name):
        if name == 'parameter':
            return self._get_gs('model1_parameters_answer.txt')
        elif name == 'timecourse':
            return self._get_gs('model1_prediction_answer.txt')
        elif name == 'topology':
            return self._get_gs('model2_topology_answer.txt')
        else:
            raise ValueError("Incorrect challenge name. Use one of %s " % self.sub_challenges)

    def _get_gs(self, filename):
        filename = self.getpath_gs(filename)
        return filename

    def _load_gold_standard(self):
        self.gs = {}
        self.gs['param1'] = self._read_df(self._get_gs("model1_parameters_answer.txt"), mode='param')
        self.gs['param2'] = self._read_df(self._get_gs("model2_parameters_answer.txt"), mode='param')
        self.gs['pred1'] = self._read_df(self._get_gs("model1_prediction_answer.txt"), mode='pred')
        self.gs['topo2'] = self._read_df(self._get_gs("model2_topology_answer.txt"), mode='topo')


    ################################## compute all submissions from challenge
    def leaderboard_compute_score_topology(self):
        """Computes all scores (topology) for loaded submissions

        For the metric, see :meth:`score_topology`.

        :return: fills :attr:`scores`.


        .. seealso:: :meth:`load_submissions`
        """
        scores = {}
        for team in self.team_names:
            data = self.data['topo2'][team]
            score = self._compute_score_topology(data, team=team)
            scores[team] = score
        df = pd.TimeSeries(scores)
        df = pd.DataFrame({'scores':df, 'rank':df.rank()})
        self.scores['topo2'] = df.sort(columns='rank')

    def leaderboard_compute_score_parameters_model1(self):
        """Computes all scores (parameters model1)

        :return: Nothing but fills :attr:`scores`.

        For the metric, see :meth:`score_model1_parameters`.


        .. seealso:: :meth:`load_submissions`

        """
        # parameter model1
        scores = {}
        for team in self.team_names:
            data = self.data['param1'][team]
            score = self._compute_score_model1_parameters(data)
            scores[team] = score
        df = pd.TimeSeries(scores)
        df = pd.DataFrame({'scores':df, 'rank':df.rank()})
        self.scores['param1'] = df.sort(columns='rank')

    def leaderboard_compute_score_timecourse_model1(self, startindex=10, endindex=39):
        """Computes all scores (timecourse model1)

        :return: Nothing but fills :attr:`scores`

        For the metric, see :meth:`score_model1_parameters`.

        Note that *endindex* is set to 39 so it does not take into account last value at time=20
        This is to be in agreement with the implemenation used in the final leaderboard

        https://www.synapse.org/#!Synapse:syn2821735/wiki/71062

        If you want to take into account final point, set endindex to 40

        """
        scores = {}
        for team in self.team_names:
            data = self.data['pred1'][team]
            scores[team] = self._compute_score_timecourse_model1(data, 
                    startindex, endindex)
        self.scores['pred1'] = pd.TimeSeries(scores)
        self.scores['pred1'].sort()
        self.scores['pred1'] = self.scores['pred1'].to_frame()
        self.scores['pred1'].columns = ['scores']

    def _compute_score_model1_parameters(self, data):
        diff = data / self.gs['param1']
        diff = (np.log10(diff)**2).mean()
        score = diff.values[0] # should be a single float
        return score

    def _compute_score_timecourse_model1(self, data, startindex, endindex):
        d1 = (self.gs['pred1'] - data) ** 2
        d1 /= (0.01 + 0.04 * self.gs['pred1'].values**2)
        # let us ignore the first 10 points

        # faster to use numpy array and indices
        data = d1.values[startindex:endindex+1,:]
        N = endindex - startindex + 1.
        distance = np.sum(data) / (3*N)  # normalisation
        return distance

    ##################################### NULL distribution (draft do not use)
    def _get_random_parameters_model1(self, N=10000):
        """Null distribution for the model1 parameter

        :param N: number of distribution
        :param int Nbest: In the official challenge, 12 submissions wre provided. Here, we use only the 9 best submissions
            like in the paper.
        :return: a dataframe with null distributions


        .. note:: submissions are loaded and scored before creating the null
            distributions.

        """
        self.load_submissions()
        self.leaderboard_compute_score_parameters_model1()
        # select only best 9 as in the paper
        Nbest = 9
        best_teams = list(self.scores['param1'].ix[0:Nbest].index)

        # create a dataframe to hold all teams and
        p = pd.DataFrame(dict([(key, self.data['param1'][key].T.values[0])
            for key in best_teams]))

        nulls = []
        for k in xrange(0, 45):
            null = p.ix[k][np.random.randint(0, Nbest, N)]
            nulls.append(null)

        indexnames = list(self.gs['param1'].index)
        df = pd.DataFrame(dict([(name, nulls[i].values)
            for i, name in enumerate(indexnames)]))
        df = df[self.gs['param1'].index]
        return df

    def get_null_parameters_model1(self, N=10000):
        """Returns score distribution (parameter model1)"""
        df = self._get_random_parameters_model1(N=N)

        distances =[]
        from easydev import progress_bar
        pb = progress_bar(N)
        for i in xrange(0, N):
            df1 = df.ix[i].to_frame(name='values')
            distance = self._compute_score_model1_parameters(df1)
            distances.append(distance)
            pb.animate(i+1)
        return distances

    def get_pvalues_parameter(self, score):
        filename = self._pj([self.classpath, 'data', 'D7C1_param_proba.npy'])
        data = np.load(filename)
        X = data[:, 0]
        Y = data[:, 1]
        return sum(Y[X<score]) * (X[2]-X[1])

    def _get_random_timecourse_model1(self, N=10000):
        """Null distributions for the model1 timecourse challenge

        :param N: number of random models
        :return: a dataframe with the null distribution
        """
        # In the official LB, 12 submissions wre provided. Here, we use only the 9 best submissions
        # like in the paper.

        self.load_submissions()
        self.leaderboard_compute_score_timecourse_model1()
        Nbest = 11
        best_teams = list(self.scores['pred1'].ix[0:Nbest].index)

        # data mangling to extract random values easily
        p3 = pd.DataFrame(dict([(key, self.data['pred1'][key]['p3']) for key in best_teams]))
        p5 = pd.DataFrame(dict([(key, self.data['pred1'][key]['p5']) for key in best_teams]))
        p8 = pd.DataFrame(dict([(key, self.data['pred1'][key]['p8']) for key in best_teams]))

        df = self.gs['pred1'].copy()

        data = np.zeros((41,3, N))
        for ik,k in enumerate(list(self.gs['pred1'].index)):
            data[ik,0] = p3.ix[k][np.random.randint(0,Nbest,N)]
            data[ik,1] = p5.ix[k][np.random.randint(0,Nbest,N)]
            data[ik,2] = p8.ix[k][np.random.randint(0,Nbest,N)]
        return data

    def get_null_timecourse_model1(self, N=10000):
        data = self._get_random_timecourse_model1(N=N)
        distances = []
        from easydev import progress_bar
        pb = progress_bar(N)
        for i in xrange(0,N):
            df = data[:,:,i]
            # FIXME those values 10,39 should not be hardcoded
            distance = self._compute_score_timecourse_model1(df, 10,39)
            distances.append(distance)
            pb.animate(i)
        return distances

    def get_pvalues_timecourse(self, score):
        # The code that computs the p-values does not provide similiar results as in the LB
        #
        # for now, we use the LB scores and pvalues and interpolate
        scores = np.array([0.002438361, 0.016023721, 0.035404398, 0.047495432, 0.09791128, 0.198785197,
                      0.356429217, 0.362463945, 0.817972877, 3.222767988, 14.77443631, 19.32326868])
        pvalues = np.array([1.21E-25, 3.39E-18, 4.45E-15, 6.28E-14, 4.01E-11, 1.93E-08,
                            2.53E-06, 2.90E-06, 1.34E-03, 6.90E-01, 1.00E+00, 1.00E+00])
        return np.interp(score, scores, pvalues)

    def _leaderboard_compute_overall_score(self, N=100):
        """Based on NULL distribution, compute overall score of model1

        Not finalised.

        """
        self._compute_pvalues_pred1(N=N)
        self._compute_pvalues_param1(N=N)
        import fitter
        fit_param1 = fitter.Fitter(self.rdistance_param1)
        fit_param1.distributions = ['beta']
        fit_param1.fit()
        fit_pred1 = fitter.Fitter(self.rdistance_pred1)
        fit_pred1.distributions = ['beta']
        fit_pred1.fit()

        import scipy.stats
        self.pvalues_param1 = scipy.stats.beta.cdf(self.scores['param1'].scores,
                *fit_param1.fitted_param['beta'])
        self.pvalues_pred1 = scipy.stats.beta.cdf(self.scores['pred1'].scores,
                *fit_pred1.fitted_param['beta'])

        self.scores['pred1']['pvalues'] = self.pvalues_pred1
        self.scores['param1']['pvalues'] = self.pvalues_param1

    def leaderboard(self):
        """Computes all scores for all submissions and returns dataframe


        :return: dataframe with scores for each submissions for the
            model1 (parameter and timecourse) and model2 (topology)
        """
        self.load_submissions()
        self.leaderboard_compute_score_parameters_model1()
        self.leaderboard_compute_score_topology()
        self.leaderboard_compute_score_timecourse_model1(10,39)

        df = pd.merge(self.scores['param1'], self.scores['pred1'],
                left_index=True, right_index=True,
                suffixes=['_parameter', '_timecourse'])


        df = pd.merge(df, self.scores['topo2'],
                left_index=True, right_index=True
                )
        df.columns = [c if c!='scores' else 'scores_topology' for c in df.columns]

        return df


    #### Topology related

    def _compute_score_topology(self, data, team=''):
        """see :meth:`score_topology` for details """
        data = data.copy() # make sure we do not change the data so use copy()
        gs = self.gs['topo2'].copy()

        Li = np.array([0,0,0])
        Ni = np.array([0,0,0])

        # loop over solution
        cols1 = ['regulator', 'sign1', 'g1']
        cols2 = ['regulator', 'sign2', 'g2']
        # build list of existing genes and their signs from the GS
        # order does not matter, this is for th counting of Ni
        genes =  np.hstack([gs.g1.values , gs.g2.values])
        signs =  np.hstack([gs.sign1.values , gs.sign2.values])

        # make sure there are unique
        regulators_data = set(data.regulator)

        for i in range(0,3):
            for j in range(0,3):
                # if all 5 values are correct, L = 12 and stops there
                # Note that is the regulated gene is zero, it means
                # it does not exists so it is ignored.
                if all(gs.values[i][[0,1,2]] == data.values[j][[0,1,2]]) is True:
                    # g1 should be different from 0
                    # regulator is tested as well although the GS are no such case
                    if gs.ix[i]['g1'] != 0 and gs.ix[i]['regulator'] != 0 :
                        Li[i] += 6
                        data.iloc[j,0] = 0 # index 0 means first columns that is the regulator
                        data.iloc[j,2] = 0 # index 4 means gene1
                if all(gs.values[i][[0,3,4]] == data.values[j][[0,3,4]]) is True:
                    # g1 should be different from 0
                    # regulator is tested as well although the GS are no such case
                    if gs.ix[i]['g2'] != 0 and gs.ix[i]['regulator'] != 0 :
                        Li[i] += 6
                        data.iloc[j,0] = 0 # index 0 means first columns that is the regulator
                        data.iloc[j,4] = 0 # index 4 means gene2

        # any regulator correctly predicted ?

        for reg in set(data.regulator):
            if reg !=0 and reg in gs.regulator.values:
                Ni[i] += 1

        genes_data =  np.hstack([data.g1.values , data.g2.values])
        signs_data =  np.hstack([data.sign1.values , data.sign2.values])


        import collections

        dgenes = collections.defaultdict(list)
        for gene, sign in zip(genes,signs):
            dgenes[gene].append(sign)
        dgenes_data = collections.defaultdict(list)
        for gene, sign in zip(genes_data,signs_data):
            dgenes_data[gene].append(sign)

        # here this is ambigous: a gene may have 2 opposite signs... To be in agreement with original code
        # from pablo that was used in the dream challenge, we keep the latest values found in the submissions.
        # this is arbitrary though.
        #for key in dgenes_data.keys():
        #  if dgenes_data.

        # Why do we get rid of the gene 0 ? Probably gens are implemented as values
        # from 1 to 11 and 0 means to interactions
        try:
            del dgenes[0]
        except:
            pass
        try:
            del dgenes_data[0]
        except:
            pass

        # any gene and sign found in GS?
        for gene, signs in dgenes_data.items():
            if gene in dgenes.keys():
                Ni[i] += 1
                if signs[-1] in dgenes[gene]:
                    Ni[i] += 1

        Si = Li + Ni
        return sum(Si)

    def get_random_topology(self):
        # Create a random topology submission
        data = pd.DataFrame()

        sign1 = ["+" if x ==1 else "-" for x in np.random.randint(0, 2, 3)]
        sign2 = ["+" if x ==1 else "-" for x in np.random.randint(0, 2, 3)]
        regulator = np.random.randint(0, 12, 3)
        g1 = np.random.randint(0, 12, 3)
        g2 = np.random.randint(0, 12, 3)

        data['regulator'] = regulator
        data['sign1'] = sign1
        data['g1'] = g1
        data['sign2'] = sign2
        data['g2'] = g2

        return data

    # NULL distribution and p-values for the topology challenge
    def get_null_topology(self, N=10000):
        """Return null distribution of the topology score"""
        nulls = [self._compute_score_topology(self.get_random_topology()) for i in range(0, N)]
        return nulls

    def get_pvalues_topology(self, x):
        """Return pvalues of a given score (topology challenge)"""

        # pvalues are hardcoded and were computed using N=100000 values from :meth:`get_null_topo`
        # nulls = s.get_null_prop(100000)
        # Y, X = np.histogram(nulls, bins=range(0,20), normed=True)
        # X  = X[1:]

        Y = np.array([  1.65600000e-02,   7.03700000e-02,   1.54750000e-01,
            2.15260000e-01,   2.12310000e-01,   1.53090000e-01,
            8.32200000e-02,   3.86100000e-02,   2.12100000e-02,
            1.48600000e-02,   9.95000000e-03,   5.78000000e-03,
            2.32000000e-03,   8.60000000e-04,   3.90000000e-04,
            3.00000000e-04,   1.00000000e-04,   4.00000000e-05,
            2.00000000e-05])

        X = np.array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

        return sum(Y[X>=x] * 1)





