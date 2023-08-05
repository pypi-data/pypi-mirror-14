# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of DREAMTools software
#
#  Copyright (c) 2015, DREAMTools Development Team
#  All rights reserved
#
#  Distributed under the BSD 3-Clause License.
#  See accompanying file LICENSE distributed with this software
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  website: http://github.com/dreamtools
#
##############################################################################
"""Provides tools related to Receiver Operating Characteristic (ROC).

Those code were directly translation of Perl or matlab
codes but we should be using scikit-learn in the future."""
import numpy as np


__all__ = ['ROC', 'ROCDiscovery', 'D3D4ROC', 'MCC']


class BinaryClassifier(object):
    """The roc module coontains lots of duplicated code that
    will be cleanup in the future. To do so, we will 
    use this class, which is used e.g., in D6C1.

    """
    def __init__(self):
        self.recall = []
        self.precision = []
        self.fpr = []
        self.tpr = []

    def roc(self):
        pass

    def compute_auc(self):
        """Compute AUC given a ROC data set (recomputed otherwise)

        :param str roc: The roc data structure must be a dictionary with "tpr"
            key. Could be a variable returned by :meth:`get_statistics`. If not
            provided, compute the ROC.
        :return: the AUC
        """
        import scipy.integrate
        value = scipy.integrate.trapz(self.tpr, x=self.fpr)
        return value

    def compute_aupr(self):
        """Compute AUPR given a ROC data set (recomputed otherwise)

        :param str roc: The roc data structure must be a dictionary with "tpr"
            key. Could be a variable returned by :meth:`get_statistics`. If not
            provided, compute the ROC.
        :return: the AUPR
        """
        import scipy.integrate
        value = scipy.integrate.trapz(self.precision, x=self.recall)
        return value


class ROCBase(object):
    """An ABC class"""

    def __init__(self):
        pass

    def get_statistics(self):
        raise NotImplementedError

    def compute_auc(self, roc=None):
        """Compute AUC given a ROC data set (recomputed otherwise)

        :param str roc: The roc data structure must be a dictionary with "tpr"
            key. Could be a variable returned by :meth:`get_statistics`. If not
            provided, compute the ROC.
        :return: the AUC

        """
        if roc is None:
            roc = self.get_statistics()
        import scipy.integrate
        value = scipy.integrate.trapz(roc['tpr'], roc['fpr'])
        return value
        #return sum(roc['tpr']) / len(roc['tpr'])

    def compute_aupr(self, roc=None):
        """Compute AUPR given a ROC data set (recomputed otherwise)

        :param str roc: The roc data structure must be a dictionary with "tpr"
            key. Could be a variable returned by :meth:`get_statistics`. If not
            provided, compute the ROC.
        :return: the AUPR
        """
        if roc == None:
            roc = self.get_statistics()
        import scipy.integrate
        value = scipy.integrate.trapz(roc['precision'], x=roc['recall'])
        return value


class ROC(ROCBase):
    """A class to compute ROC, AUC and AUPRs for a binary problem


        >>> r = ROC() # could provide scores and labels as arguments
        >>> r.scores = [0.9,0.8,0.7,.6,.6,.3]
        >>> r.classes = [1,0,1,0,1,1]
        >>> r.compute_auc()
        0.4375


    """
    def __init__(self, scores=None, classes=None):
        """.. rubric:: Constructor

        :param list scores: the scores
        :param list classes: binary class made of 1 or 0 numerical values. Also
            called labels in the literature.
        """
        super(ROC, self).__init__()
        self._scores = None
        self._classes = None

        self.scores = scores
        self.classes = classes

    def _set_scores(self, values):
        self._scores = values
    def _get_scores(self):
        return self._scores
    scores = property(_get_scores, _set_scores, doc="Read/Write the scores")

    def _set_classes(self, values):
        self._classes = values
    def _get_classes(self):
        return self._classes
    classes = property(_get_classes, _set_classes, doc="Read/Write the classes")

    def _compute_fpr_tpr(self, FP, TP, N, P):
        roc = {"fpr":[], "tpr":[], "FP":[], "TP":[]}
        roc['fpr'] = FP/float(N)
        roc['tpr'] = TP/float(P)
        roc['TP'] = TP
        roc['FP'] = FP
        return roc

    def get_roc(self):
        """See :meth:`get_statistics`"""
        return self.get_statistics()

    def get_statistics(self):
        """Compute the ROC curve X/Y vectors and some other metrics

        :return: a dictionary with different metrics such as FPR (false positive
            rate), PTR (true positive rate).

        """
        scores = self.scores
        classes = list(self.classes)

        sorted_indices = np.argsort(1-np.array(scores))
        sorted_scores = [scores[i] for i in sorted_indices]
        sorted_classes = [classes[i] for i in sorted_indices]
        P = float(classes.count(1))
        N = float(classes.count(0))
        FP = 0
        TP = 0
        #
        roc = {"fpr":[], "tpr":[], "precision":[], "FP":[], "TP":[],
            "recall":[], "accuracy":[], "Fmeasure":[], 'threshold':[]}
        fprev = 1.1 # scores are less than 1 

        # an efficient algorithm to compute ROC based on T.Fawcett Pattern
        # Recognition Letters 27, 2006
        i = 0
        while i<len(scores):
            cls = sorted_classes[i]
            score = sorted_scores[i]

            if score != fprev and cls!=None:
                thisroc = self._compute_fpr_tpr(FP, TP, N, P)
                for key in ['fpr', 'tpr', "FP", "TP"]:
                    roc[key].append(thisroc[key])
                roc['threshold'].append(fprev)
                fprev = score

            if cls == 1:
                TP += 1
            elif cls == 0:
                FP += 1
            elif cls == None or np.isnan(cls):
                pass
            else:
                raise ValueError("found a class value different from 0,1 or None")
            i += 1
        sroc = self._compute_fpr_tpr(FP, TP, N, P)
        for key in ['fpr', 'tpr', "FP", "TP"]:
            roc[key].append(thisroc[key])

        # force the last value of tpr/fpr to be one
        # TODO this is a hack to bebahve correctly when the final fpr/tpr are nt
        # (1,1) as it should be.
        roc['fpr'][-1] = 1
        roc['tpr'][-1] = 1

        roc['threshold'].append(sorted_scores[-1])

        roc = self._compute_other_metrics(roc)
        return roc

    def _compute_other_metrics(self, roc):
        #Be aware that there is alway a first value TP=0,FP=0
        # this should be handled with care the recall/precision computatio
        # This first value is used to compute fpr and tpr but should not be used 
        # here
        FP = np.array([float(x) for x in roc['FP']])
        TP = np.array([float(x) for x in roc['TP']])
        N = max(FP) + max(TP)

        # The first value of precision is undefined since FP+TP=0
        # It does not matter since it will be overwritten as explained here
        # below

        # TODO: to prevent warning, set FP[0] to 100.
        FP[0] = 100
        precision = TP / (FP + TP)
        recall = TP/float(max(TP))
        # The second value may also be be an issue. There are 2 cases.
        # 1. TP>0
        # 2. TP == 0 
        # In the second case,  TP=0 and FP==0 should not happen. FP > 0 instead.
        # In which case, recall = 0 and precision=0. No ambiguity
        # In the first case, if TP>0 then precision >0 and recall > 0. 
        # Therefore we end up without a defined value at recall==0
        # So we should set a recall=0 for which precision will be the same as
        # the one where recall >0
        # somehow, precision and recall 
        if TP[1]>0:
            precision[0] = precision[1] 
        else:
            precision[0] = 0

        # TODO
        #roc['accuracy'] = (TP+FP)/(P+N)
        #if roc['recall'] >0 and roc['precision'] != np.nan and roc['precision'] > 0 :
        #    roc['Fmeasure'] = 2./(1./roc['precision']+1./roc['recall'])
        #else:
        #    roc['Fmeasure'] = np.nan
        roc['precision'] = [float(x) for x in precision]
        roc['recall'] = [float(x) for x in recall]
        return roc

    def plot_roc(self, roc=None):
        """Plot ROC curves

        .. plot::
            :include-source:
            :width: 80%

            from dreamtools.core.rocs import ROC
            r = ROC()
            r.scores = [.9,.5,.6,.7,.1,.2,.6,.4,.7,.9, .2]
            r.classes = [1,0,1,0,0,1,1,0,0,1,1]
            r.plot_roc()

        """
        if roc == None:
            roc = self.get_statistics()
        from pylab import plot, xlim, ylim ,grid, title, xlabel, ylabel
        x = roc['fpr']
        plot(x, roc['tpr'], '-o')
        plot([0,1], [0,1],'r')
        ylim([0, 1])
        xlim([0, 1])
        grid(True)
        title("ROC curve (AUC=%s)" % self.compute_auc(roc))
        xlabel("FPR")
        ylabel("TPR")


class ROCDiscovery(ROCBase):
    """A variant of ROC statistics

    Used in D5C2 challenge.

    .. note:: Does not work if any NA are found.
    """
    def __init__(self, discovery):
        """.. rubric:: constructor


        :param discovery: a list of 0/1 where 1 means positives
        """
        super(ROCDiscovery, self).__init__()

        try:
            self.discovery = discovery.values # a pandas time series ?
        except:
            self.discovery = np.array(discovery)

        # sanity checks
        assert set(np.unique(self.discovery)) == set([0,1]),\
            'ERROR: discovery is only allowed to have (0,1) entries.'

    def get_statistics(self):
        """Return dictionary with FPR, TPR and other metrics"""
        discovery = self.discovery # an alias
        T = len(discovery)  # Total
        P = np.sum(discovery) # positives
        N = T - P # negatives

        # true positives (false positives) at depth k
        TPk = np.cumsum(discovery)
        FPk = np.cumsum(1-discovery)

        # metrics
        TPR = TPk / float(P)
        FPR = FPk / float(N)
        REC = TPR  # recall
        PREC = TPk / np.linspace(1, T+1,T) # precision

        roc = {"fpr": FPR, "tpr":TPR, "precision":PREC, "FP":[], "TP":[],
            "recall": REC, "accuracy":[], "Fmeasure":[], 'threshold':[]}
        return roc

    def compute_aupr(self, roc=None):
        """Returns AUPR normalised by (1-1/P) P being number of positives"""
        AUPR = super(ROCDiscovery, self).compute_aupr(roc=roc)
        P = np.sum(self.discovery)
        return AUPR / (1-1./P)


class D3D4ROC(ROCBase):
    def __init__(self):
        super(D3D4ROC, self).__init__()

    def plot(self):
        metrics = self.metrics
        import pylab
        fpr = metrics['fpr']
        tpr = metrics['tpr']
        rec = metrics['rec']
        prec = metrics['prec']

        pylab.figure(1)
        pylab.subplot(1,2,1)
        pylab.plot(fpr,tpr)
        pylab.title('ROC')
        pylab.xlabel('FPR')
        pylab.ylabel('TPR')
        pylab.subplot(1,2,2)
        pylab.plot(rec,prec)
        pylab.title('P-R')
        pylab.xlabel('Recall')
        pylab.ylabel('Precision')

    def get_statistics(self, gold_data, test_data, gold_index):

        T = len(gold_data)          # Total potential edges n(n-1)
        try:
            P = gold_data[2].sum()      # positives
        except:
            P = gold_data[1].sum()      # positives
        N = T - P                   # negatives
        L = len(test_data)          # length of prediction list

        # counters
        k = 0
        Ak = 0
        TPk = 0
        FPk = 0

        rec = []
        prec = []
        tpr=[]
        fpr = []
        while k < L:

            k = k + 1
            # index of the kth predicted edge
            #idx = test.index(k)
            #if gold[idx] == 1:
            if gold_index[k-1] == 1:
                #%% the edge IS present in the gold standard

                #%% increment TPk
                TPk = TPk + 1.

                #%% update area under precision-recall curve
                if k == 1:
                    delta = 1. / P
                else:
                    delta = (1. - FPk * np.log(k/(k-1.))) / P
                Ak = Ak + delta

            else: # the edge is NOT present in the gold standard
                #%% icrement FPk
                FPk = FPk + 1.

            # do NOT update area under P-R
            #remember
            rec.append(TPk/float(P))
            prec.append(TPk/float(k))
            tpr.append(rec[k-1])
            fpr.append(FPk/float(N))

        # Done with the positive predictions.

        # If the number of predictions (L) is less than the total possible edges (T),
        # we assume that they would achieve the accuracy of the null model (random guessing).

        TPL = TPk

        # rho
        if L < T:
            rh = (P-TPL)/float(T-L)
        else:
            rh = 0.

        # recall at L
        if L > 0:
            recL = rec[L-1]   # note -1 to use python syntax
        else:
            recL = 0

        # the remaining positives would eventually be predicted
        while TPk < P:
            k = k + 1
            TPk = TPk + 1.
            rec.append(TPk/float(P))
            if ((rec[k-1]-recL) * P + L * rh) != 0:
                prec.append( rh * P * rec[k-1]/((rec[k-1]-recL)*P + L * rh))
            else:
                prec.append(0)

            tpr.append(rec[k-1])
            FPk = TPk * (1-prec[k-1])/prec[k-1]
            fpr.append(FPk/float(N))

        # Now, update the area under the P-R curve
        # %% rh = (P-TPk)/(T-L);  % BP: I removed this line because it is an error in logic to redefine this here.
        AL = Ak

        #if ~isnan(rh) and rh != 0 and L != 0:
        if rh != 0 and L != 0:
            AUC = AL + rh * (1.-recL) + rh * (recL - L * rh / P) * np.log((L * rh + P * (1-recL) )/(L *rh))
        elif L == 0:
            AUC = P/float(T)
        else:
            AUC = Ak

        # Integrate area under ROC
        lc = fpr[0] * tpr[0] /2.
        for n in range(1,int(L+P-TPL-1 + 1)):
            lc = lc + ( fpr[n] + fpr[n-1]) * (tpr[n]-tpr[n-1]) / 2.

        AUROC = 1. - lc

        auroc = AUROC
        aupr = AUC

        return AUC, AUROC, prec, rec, tpr, fpr


class DREAM2(object):

    def __init__(self):
        pass

    def compute_specific_precision_values(self, P, rec):

        spec_prec = {}
        for x in [1, 2, 5, 20, 100, 500, 1000]:
            if x > P:
                break
            rec0 = x / float(P)
            i = rec.index(rec0)
            spec_prec[x] = rec[i]

        return spec_prec


def MCC(TP, TN, FP, FN):
    """Matthews correlation coefficient"""
    return (TP*TN-FP*FN) / np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
