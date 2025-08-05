"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # Create dictionary of NEOs by designation and by name for faster searching
        self.neo_by_designation = {}
        self.neo_by_name = {}

        # Create a dictionary of approaches by designation for faster DB setup
        self.approaches_by_designation = {}

        # Create a dictionary of hazardous and non-hazardous NEOs
        hazardous = {'hazardous':[], 'non-hazardous':[]}

        # Populate the approaches by designation dictionary
        for approach in self._approaches:
            if approach.get_designation() not in self.approaches_by_designation:
                self.approaches_by_designation[approach.get_designation()] = [
                    approach
                ]
            else:
                self.approaches_by_designation[approach.get_designation()].append(approach)

        # Connect neos and approaches
        for neo in self._neos:
            try:
                for approach in self.approaches_by_designation[neo.designation]:
                    approach.neo = neo
                    neo.approaches.append(approach)

                # Create a hazardous and non-hazardous database
                if neo.hazardous:
                    hazardous['hazardous'].append(neo)
                else:
                    hazardous['non-hazardous'].append(neo)

            # Handle KeyError by skipping that item and continuing
            except KeyError:
                continue

            # Add neo to dictionary of designations and dictionary of names for faster searching
            self.neo_by_designation[neo.designation] = neo
            if neo.name is not None:
                self.neo_by_name[neo.name] = neo

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        if designation not in self.neo_by_designation:
            return None
        return self.neo_by_designation[designation]

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        if name not in self.neo_by_name:
            return None
        return self.neo_by_name[name]

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # Iterate over approaches to validate against filters
        for approach in self._approaches:
            valid = True

            # Iterate over filters and change valid to false, break for loop if filter doesn't match approach
            for f in filters:
                if not f(approach):
                    valid = False
                    break

            # Only print approach if it meets all the filter criteria
            if valid:
                yield approach
