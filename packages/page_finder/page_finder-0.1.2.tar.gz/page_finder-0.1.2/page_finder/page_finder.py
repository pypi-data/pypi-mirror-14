import heapq
import re

import numpy as np

from .edit_distance import levenshtein


class PointSpace(object):
    """Given a point will assign numeric IDs"""
    def __init__(self):
        self.points = set()
        self.point_to_id = {}
        self._updated = True

    def _update(self):
        if self._updated:
            return
        current_id = 0
        for point in self.points:
            self.point_to_id[point] = current_id
            current_id += 1
        self._updated = True

    def add(self, point):
        self.points.add(point)
        self._updated = False

    def delete(self, point):
        self.points.discard(point)
        self._updated = False

    def get_id(self, point):
        self._update()
        return self.point_to_id.get(point)


class OrderedPoint(object):
    """A pair made of a point and a distance from a reference"""
    def __init__(self, point, distance):
        self.point = point
        self.distance = distance

    def __cmp__(self, other):
        """Farthest point first"""
        return -cmp(self.distance, other.distance)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '({0}, distance={1})'.format(self.point, self.distance)

    @property
    def as_tuple(self):
        return (self.point, self.distance)



class Neighborhood(object):
    """A neighborhood is made from a reference point and a finite set of
    nearest points.

    Arguments:
    - point        : reference point
    - distance_func: function to use when computing distances
    - k            : neighborhood maximum size


    Attributes:
    - point        : reference point
    - near         : a collection (heap) of near OrderedPoint
    """
    def __init__(self, point, distance_func, k=5):
        self.point = point
        self.near = []
        self.distance = distance_func
        self.k = k

    def add_point(self, new_point):
        new_pair = OrderedPoint(new_point,
                                self.distance(new_point, self.point))
        heapq.heappush(self.near, new_pair)
        while len(self.near) >= self.k:
            furthest = heapq.nsmallest(1, self.near)[0]
            if furthest.distance > new_pair.distance:
                heapq.heappop(self.near)
            else:
                break

    def del_point(self, del_point):
        update = False
        for pair in self.near:
            if pair.point == del_point:
                update = True
                break
        if update:
            self.near = [pair for pair in self.near if pair.point != del_point]
            heapq.heapify(self.near)

    def __str__(self):
        return '{0} <- {1}'.format(self.point, self.near)


class KNNGraph(object):
    def __init__(self, distance_func, k=5):
        self.point_space = PointSpace()
        self.graph = [] # A list of neighborhoods
        self.k = k
        self.distance = distance_func

    def add_point(self, point):
        if point in self.point_space.points:
            return False
        self.point_space.add(point)
        new_nb = Neighborhood(point, self.distance, k=self.k)
        for nb in self.graph:
            nb.add_point(point)
            new_nb.add_point(nb.point)
        self.graph.append(new_nb)
        return True

    def del_point(self, point):
        if point not in self.point_space.points:
            return
        self.point_space.delete(point)
        new_graph = []
        for nb in self.graph:
            if nb.point != point:
                nb.del_point(point)
                new_graph.append(nb)
        self.graph = new_graph

    def gaussian_kernel(self, sigma=1.0, size=None):
        if size is None:
            n = len(self.graph)
        else:
            n = size
        G = np.zeros((n, n))
        for nb in self.graph:
            i = self.point_space.get_id(nb.point)
            for ordered_point in nb.near:
                j = self.point_space.get_id(ordered_point.point)
                G[i, j] = np.exp(-ordered_point.distance**2/(2*sigma**2))
        return G


def label_propagation(kernel, labels, alpha=0.1, eps=1e-3):
    """Apply label propagation algorithm as described in:

    Learning with Local and Global Consistency
    Zhou et al, 2003


    kernel: an square similarity matrix of shape NxN
    labels: a matrix of shape Nx2
    alpha : between 0 and 1
    eps   : convergence residue
    """
    W = kernel
    Y = labels
    D = np.sum(W, axis=1)
    D[D == 0] = 1
    D = np.diag(1.0/np.sqrt(D))
    S = np.dot(np.dot(D, W), D)
    F1 = Y
    err = eps
    while err >= eps:
        F2 = alpha*np.dot(S, F1) + (1.0 - alpha)*Y
        err = np.max(np.abs(F2 - F1))
        F1 = F2
    return F2


ANY_NUMBER = re.compile('\d+')
def number_preprocessor(url):
    return re.sub(ANY_NUMBER,
                  lambda match: '{' + (match.end() - match.start())*'D' + '}',
                  url)


def dont_preprocess(url):
    return url


class LinkAnnotation(object):
    def __init__(self, k=5, alpha=0.95,
                 sigma=None, eps=1e-3, preprocess=number_preprocessor):
        self.marked = {}
        def distance_func(a, b):
            if not isinstance(a, str):
                a = a.encode('ascii', 'ignore')
            if not isinstance(b, str):
                b = b.encode('ascii', 'ignore')
            return levenshtein(preprocess(a), preprocess(b))
        self.knn_graph = KNNGraph(
            distance_func=distance_func,
            k=k)
        self.alpha = alpha
        self.sigma = sigma
        self.min_score = 0
        self.eps = eps
        self._labels = None
        self._update = False

    @property
    def links(self):
        return self.knn_graph.point_space.points

    def add_link(self, link):
        if self.knn_graph.add_point(link):
            self._update = True

    def del_link(self, link):
        self.knn_graph.del_point(link)
        try:
            del self.marked[link]
        except KeyError:
            pass

    def load(self, links):
        for link in links:
            self.add_link(link)

    def mark_link(self, link, follow=True):
        self.add_link(link)
        self.marked[link] = follow

    def _sigma_estimation(self):
        sigma = 0.0
        n = 0
        for nb in self.knn_graph.graph:
            if self.marked.get(nb.point):
                for op in nb.near:
                    if self.marked.get(op.point):
                        sigma += op.distance
                        n += 1
        if n == 0 or sigma == 0:
            return 1.0
        else:
            return sigma/float(n)

    def _min_score_estimation(self):
        min_score = 0.0
        n = 0
        for link, follow in self.marked.iteritems():
            min_score += self.link_scores(link)[0]
            n += 1
        if n > 0:
            return 0.25*min_score/float(n)
        else:
            return 0.0

    def _propagate_labels(self):
        n = len(self.links)
        Y = np.zeros((n, 2))
        for link, follow in self.marked.iteritems():
            link_id = self.knn_graph.point_space.get_id(link)
            Y[link_id, 0] = follow
            Y[link_id, 1] = not follow

        sigma = self._sigma_estimation() if self.sigma is None else self.sigma
        self._labels = label_propagation(
            self.knn_graph.gaussian_kernel(sigma, size=n), Y, self.alpha, self.eps)
        self._update = False
        self.min_score = self._min_score_estimation()

    def link_scores(self, link):
        self.add_link(link)
        if self._update:
            self._propagate_labels()
        link_id = self.knn_graph.point_space.get_id(link)
        return (self._labels[link_id, 0], self._labels[link_id, 1])

    def is_follow_link(self, link):
        s1, s2 = self.link_scores(link)
        if s1 >= self.min_score or s2 >= self.min_score:
            return s1 >= s2
        else:
            return False

    def follow_links(self):
        return [link for link in self.links if self.is_follow_link(link)]

    def best_links_to_follow(self):
        follow_scores = []
        for link in self.links:
            s1, s2 = self.link_scores(link)
            if s1 > 0:
                if s2 > 0:
                    score = s1 / s2
                else:
                    score = s1
                follow_scores.append((score, link))
        return [link for _, link in sorted(follow_scores, reverse=True)]

    def prune(self, max_links=400):
        n_prune = len(self.links) - max_links
        if n_prune > 0:
            total_score = []
            for link in self.links:
                s1, s2 = self.link_scores(link)
                total_score.append((s1 + s2, link))
            to_prune = {link for _, link in sorted(total_score)[:n_prune]}
            for link in to_prune:
                self.del_link(link)
            self._propagate_labels()
