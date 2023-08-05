"""Sorting components for use in evolutionary algorithms.

As some important orderings in evolutionary computation are only partial,
the Python facilities for sorting are not sufficient. Thus, we provide
the classes in this module. Lower objective values are always considered
better.

"""
from collections import defaultdict

import evoalgos.performance
from evoalgos.individual import Individual


class NotComparableError(ValueError):
    """Error indicating that two objects cannot be compared.

    Inherits from :class:`ValueError`.

    """
    def __init__(self, object1, object2):
        message = "Cannot compare " + str(object1) + " and " + str(object2)
        ValueError.__init__(self, message)



class SortingComponent(object):
    """Interface for a sorting component."""

    def sort(self, population):
        """Sort a population.

        The sorting shall be carried out in-place.
        This is an abstract method.

        Parameters
        ----------
        population : list of Individual

        """
        raise NotImplementedError()


    def identify_groups(self, population):
        """Identify groups of equal objective values.

        This is an abstract method.

        Parameters
        ----------
        population : list of Individual

        Returns
        -------
        groups : list of lists

        """
        raise NotImplementedError()


    def identify_best_group(self, population):
        """Identify the group of best objective values.

        This is an abstract method.

        Parameters
        ----------
        population : list of Individual

        Returns
        -------
        best_group : list of Individual

        """
        raise NotImplementedError()



class LexicographicSorting(SortingComponent):
    """Lexicographic sorting."""

    @staticmethod
    def sort_key(individual):
        """Sort key for lexicographic sorting with special treatment for None.

        None is replaced with infinity (the worst possible value).

        """
        try:
            iter(individual.objective_values)
            key = []
            for objective in individual.objective_values:
                if objective is None:
                    objective = float("inf")
                key.append(objective)
        except TypeError:
            key = individual.objective_values
            if key is None:
                key = float("inf")
        return key


    def sort(self, population):
        """Sort according to lexicographic order of objective values.

        Parameters
        ----------
        population : list of Individual
            The individuals, which are sorted in-place.

        """
        if len(population) <= 1:
            return
        num_obj_values = len(population[0].objective_values)
        for individual in population:
            if num_obj_values != len(individual.objective_values):
                raise NotComparableError(population[0], individual)
        population.sort(key=self.sort_key)


    def identify_groups(self, population):
        """Identify groups of equal objective values.

        As the lexicographic order is a total order, this means that all
        individuals in a group have identical objective values.

        Parameters
        ----------
        population : list of Individual

        Returns
        -------
        groups : list of lists

        """
        sort_key = self.sort_key
        population_copy = population[:]
        self.sort(population_copy)
        prev_key = sort_key(population_copy[0])
        # groups of individuals with equal objective value
        groups = [[]]
        for individual in population_copy:
            curr_key = sort_key(individual)
            if curr_key != prev_key:
                groups.append([])
            groups[-1].append(individual)
            prev_key = curr_key
        return groups


    def identify_best_group(self, population):
        """Identify the group of best objective values.

        As the lexicographic order is a total order, this means that all
        individuals in the best group have identical objective values.

        Parameters
        ----------
        population : list of Individual

        Returns
        -------
        best_group : list of Individual

        """
        sort_key = self.sort_key
        population_copy = population[:]
        if not population_copy:
            return []
        self.sort(population_copy)
        best = [population_copy[0]]
        best_key = sort_key(population_copy[0])
        for individual in population_copy[1:]:
            if sort_key(individual) == best_key:
                best.append(individual)
            else:
                break
        return best



class NonDominatedSorting(SortingComponent):
    """Non-dominated sorting according to Pareto-dominance."""

    def __init__(self, dominance_relation=None):
        """Constructor.

        Parameters
        ----------
        dominance_relation : callable, optional
            A callable that takes two individuals as arguments and returns
            True or False. Default is :func:`dominates`.

        """
        self.dominance_relation = dominance_relation
        if dominance_relation is None:
            self.dominance_relation = self.dominates
        self.lexi_sorter = LexicographicSorting()


    @staticmethod
    def weakly_dominates(individual1, individual2):
        """Evaluate weak Pareto-dominance relation.

        None is treated as worst objective value.

        """
        ind1_objectives = individual1.objective_values
        ind2_objectives = individual2.objective_values
        num_objectives = len(ind1_objectives)
        if num_objectives != len(ind2_objectives):
            raise NotComparableError(ind1_objectives, ind2_objectives)
        for i in range(num_objectives):
            value1 = ind1_objectives[i]
            value2 = ind2_objectives[i]
            if value1 is None and value2 is not None:
                # None is worse than value2
                return False
            elif not (value1 is None or value2 is None) and value1 > value2:
                # value1 worse than value2, comparison with None bypassed
                return False
        return True


    @staticmethod
    def dominates(individual1, individual2):
        """Evaluate normal Pareto-dominance relation.

        None is treated as worst objective value.

        """
        ind1_objectives = individual1.objective_values
        ind2_objectives = individual2.objective_values
        num_objectives = len(ind1_objectives)
        if num_objectives != len(ind2_objectives):
            raise NotComparableError(ind1_objectives, ind2_objectives)
        is_one_strictly_less = False
        for i in range(num_objectives):
            value1 = ind1_objectives[i]
            value2 = ind2_objectives[i]
            if value1 is None:
                if value2 is not None:
                    # None is worse than value2
                    return False
            elif not (value1 is None or value2 is None) and value1 > value2:
                # value1 worse than value2, comparison with None bypassed
                return False
            elif (value1 is not None and value2 is None) or value1 < value2:
                # value1 better than value2 or value1 better than None
                is_one_strictly_less = True
        return is_one_strictly_less



    @staticmethod
    def strongly_dominates(individual1, individual2):
        """Evaluate strong Pareto-dominance relation.

        None is treated as worst objective value.

        """
        ind1_objectives = individual1.objective_values
        ind2_objectives = individual2.objective_values
        num_objectives = len(ind1_objectives)
        if num_objectives != len(ind2_objectives):
            raise NotComparableError(ind1_objectives, ind2_objectives)
        for i in range(num_objectives):
            value1 = ind1_objectives[i]
            value2 = ind2_objectives[i]
            if value1 is None:
                # None worse or equal to everything
                return False
            elif value2 is not None and value1 >= value2:
                # value1 worse or equal to value2, comparison with None bypassed
                return False
        return True


    def sort(self, population):
        """Reorder population to be concatenation of non-dominated fronts.

        This sorting is stable.

        """
        fronts = self.identify_groups(population)
        del population[:]
        for front in fronts:
            population.extend(front)


    def identify_groups(self, population):
        """Return a partition of the population into non-dominated fronts.

        In the identified partition, front i would be non-dominated if
        fronts 0 to i-1 were not in the population. The worst-case run time
        is :math:`O(mN^3)` for m objectives and N individuals in the
        population. Guarantees stability and exploits 1-D and 2-D special
        cases if possible.

        """
        if len(population) == 0:
            return []
        orig_indices = {ind: i for i, ind in enumerate(population)}
        fronts = []
        # check for easier special cases
        with_dim = defaultdict(int)
        for individual in population:
            with_dim[len(individual.objective_values)] += 1
        if with_dim[1] == len(population):
            # exploit 1-D special case
            fronts = self.lexi_sorter.identify_groups(population)
        else:
            input_set = set(population)
            if with_dim[2] == len(population):
                compute_non_dom_front = self.compute_non_dom_front_2d
            else:
                compute_non_dom_front = self.compute_non_dom_front_arbitrary_dim
            while len(input_set) > 0:
                # find the non-dominated elements
                min_elements = compute_non_dom_front(input_set)
                fronts.append(min_elements)
                # remove them from the input for the next iteration
                input_set.difference_update(min_elements)
        # ensure stability
        for front in fronts:
            front.sort(key=orig_indices.get)
        return fronts


    def identify_best_group(self, population):
        """Return all non-dominated in the given population.

        Guarantees stability and exploits 1-D and 2-D special cases if
        possible.

        """
        if len(population) == 0:
            return []
        orig_indices = {ind: i for i, ind in enumerate(population)}
        # check for easier special cases
        with_dim = defaultdict(int)
        for individual in population:
            with_dim[len(individual.objective_values)] += 1
        if with_dim[1] == len(population):
            min_elements = self.lexi_sorter.identify_best_group(population)
        elif with_dim[2] == len(population):
            min_elements = self.compute_non_dom_front_2d(population)
        else:
            min_elements = self.compute_non_dom_front_arbitrary_dim(population)
        # ensure stability
        min_elements.sort(key=orig_indices.get)
        return min_elements


    def compute_non_dom_front_arbitrary_dim(self, population):
        """Return the minimal elements for arbitrary dimension.

        Does neither ensure stability nor exploit special cases, but can
        handle an arbitrary number of objectives. Run time is
        :math:`O(mN^2)` for m objectives and N individuals.

        """
        if len(population) == 0:
            return []
        dominance_relation = self.dominance_relation
        min_elements = set(population)
        population = set(population)
        for candidate in population:
            for individual in min_elements:
                if dominance_relation(individual, candidate):
                    # the candidate is dominated, so we can exit the loop
                    min_elements.remove(candidate)
                    break
        return list(min_elements)


    def compute_non_dom_front_2d(self, population):
        """Return the minimal elements in the special case of two objectives.

        Does not ensure stability. Only call directly if you are absolutely
        sure you have two objectives. Run time is :math:`O(N \\log N)` for N
        individuals.

        """
        if len(population) == 0:
            return []
        dominance_relation = self.dominance_relation
        population_copy = list(population)
        self.lexi_sorter.sort(population_copy)
        min_elements = [population_copy[0]]
        for individual in population_copy[1:]:
            if not dominance_relation(min_elements[-1], individual):
                min_elements.append(individual)
        return min_elements



class CrowdingDistanceSorting(NonDominatedSorting):
    """Sort by non-domination rank and crowding distance.

    Implements the sorting order suggested in [Deb2000]_.

    """
    def sort(self, population):
        """Sort descending by fitness.

        The first priority is the index of the front an individual belongs
        to (ascending). The second priority is the individual's crowding
        distance in its front (descending).

        """
        fronts = self.identify_groups(population)
        crowding_dist_sort = self.sort_front
        for front in fronts:
            crowding_dist_sort(front)
        del population[0:]
        # concatenation of fronts is the now ordered population
        for front in fronts:
            population.extend(front)


    def sort_front(self, front):
        """Sort a front according to the crowding distance."""
        num_objectives = len(front[0].objective_values)
        # set initial values
        crowding_distances = {ind: 0.0 for ind in front}
        # crowding-distance assignment
        for i in range(num_objectives):

            def get_obj(individual):
                return individual.objective_values[i]

            front.sort(key=get_obj)
            # mark boundary individuals
            crowding_distances[front[0]] = -1.0
            crowding_distances[front[-1]] = -1.0
            # calculate distance for the other individuals
            for j in range(1, len(front) - 1):
                if crowding_distances[front[j]] >= 0:
                    obj1 = front[j-1].objective_values[i]
                    obj2 = front[j+1].objective_values[i]
                    dist = abs(obj1 - obj2)
                    crowding_distances[front[j]] += dist
        front.sort(key=crowding_distances.get, reverse=True)
        # give boundary individuals highest priority
        counter = 0
        while counter < len(front) and crowding_distances[front[-1]] == -1.0:
            individual = front.pop(-1)
            front.insert(0, individual)
            counter += 1



class HyperVolumeContributionSorting(NonDominatedSorting):
    """Sort by non-domination rank and exclusive contribution to the front.

    This sorting is required for
    :class:`HyperVolumeContributionSelection<evoalgos.selection.HyperVolumeContributionSelection>`.
    Further information can be found in [Emmerich2005]_ and [Naujoks2005]_.

    """
    def __init__(self, reference_point=None,
                 hv_indicator=None,
                 prefer_boundary_points=True):
        """Constructor.

        Parameters
        ----------
        reference_point : Individual or iterable, optional
            This point is used to bound the hypervolume.
        hv_indicator : HyperVolumeIndicator, optional
            An instance with the interface of
            :class:`QualityIndicator<evoalgos.performance.QualityIndicator>`.
            :class:`FonsecaHyperVolume<evoalgos.performance.FonsecaHyperVolume>`
            is chosen as default. It is only used for three or more
            objectives. The 2-D special case is treated directly here, to
            save some time.
        prefer_boundary_points : bool, optional
            This flag only pertains to the two-dimensional case. If it is
            set to True, the two boundary points (but not their potentially
            existing duplicates) of a 2-D front are put to the front of
            the sorted population.

        """
        NonDominatedSorting.__init__(self)
        if hv_indicator is None:
            hv_indicator = evoalgos.performance.FonsecaHyperVolume(reference_point)
        self.hypervolume_indicator = hv_indicator
        self._reference_point = None
        self.reference_point = reference_point
        self.prefer_boundary_points = prefer_boundary_points


    @property
    def reference_point(self):
        return self._reference_point


    @reference_point.setter
    def reference_point(self, ref_point):
        """Set a new reference point.

        The point is also propagated to the hypervolume indicator.

        """
        self.hypervolume_indicator.reference_point = ref_point
        self._reference_point = ref_point


    def sort(self, population):
        """Sort descending by fitness.

        The first priority is the index of the front an individual belongs
        to (ascending). The second priority is the individual's hypervolume
        contribution to this front (descending).

        """
        fronts = self.identify_groups(population)
        # check for easier special case
        is_2d = True
        for individual in population:
            is_2d &= len(individual.objective_values) == 2
        if is_2d:
            for front in fronts:
                self.sort_front_2d(front)
        else:
            for front in fronts:
                self.sort_front(front)
        del population[0:]
        # concatenation of fronts is the now ordered population
        for front in fronts:
            population.extend(front)


    def sort_front(self, front):
        """Sort a set of minimal elements.

        This is the code which calls the hypervolume indicator.

        """
        hv_indicator = self.hypervolume_indicator
        ref_point = self.reference_point
        dim = len(ref_point)
        hv_contributions = {ind: 0.0 for ind in front}
        # translate, so that reference point is [0, ..., 0]
        shifted_front = []
        for individual in front:
            obj_values = individual.objective_values
            assert len(obj_values) == dim
            shifted_point = [individual.objective_values[i] - ref_point[i] for i in range(dim)]
            shifted_front.append(shifted_point)
        hv_indicator.reference_point = [0.0] * len(ref_point)
        # max_volume is constant for this front, thus it's not necessary for
        # the right order
        #max_volume = hv_indicator.assess_non_dom_front(shifted_front)
        max_volume = 0.0
        for i in range(len(front)):
            point = shifted_front.pop(i)
            # compute volume without this individual
            remaining_volume = hv_indicator.assess_non_dom_front(shifted_front)
            # difference is what it contributed exclusively
            hv_contributions[front[i]] = max_volume - remaining_volume
            shifted_front.insert(i, point)
        # sort (descending)
        front.sort(key=hv_contributions.get, reverse=True)


    def sort_front_2d(self, front):
        """Sort minimal elements in the special case of 2 objectives.

        This code does not call the hypervolume indicator.

        """
        reference_point = self.reference_point
        prefer_boundary_points = self.prefer_boundary_points
        hv_contributions = {ind: 0.0 for ind in front}
        if not isinstance(reference_point, Individual) and not prefer_boundary_points:
            reference_point = Individual(objective_values=reference_point)
            self.reference_point = reference_point
        if prefer_boundary_points:
            dominating_ref_point = front
        else:
            dominating_ref_point = []
            for individual in front:
                if self.weakly_dominates(individual, reference_point):
                    dominating_ref_point.append(individual)
        decorated = [(ind.objective_values, i, ind) for i, ind in enumerate(dominating_ref_point)]
        decorated.sort()
        if not prefer_boundary_points:
            dummy = (reference_point.objective_values, -1, reference_point)
            decorated.insert(0, dummy)
            decorated.append(dummy)
        for i in range(1, len(decorated) - 1):
            vol = (decorated[i+1][0][0] - decorated[i][0][0])
            vol *= (decorated[i-1][0][1] - decorated[i][0][1])
            hv_contributions[decorated[i][2]] = vol
        if prefer_boundary_points:
            hv_contributions[decorated[0][2]] = float("inf")
            hv_contributions[decorated[-1][2]] = float("inf")
        # sort (descending)
        front.sort(key=hv_contributions.get, reverse=True)
