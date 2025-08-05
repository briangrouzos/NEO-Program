"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
import math
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    # initialize the object with the required and optional arguments
    def __init__(self, designation, hazardous, name=None, diameter=float('nan'), **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        Parameters
        ---------
        designation : string, required, unique, mixed letters and numbers
        hazardous : boolean, required, True or False
        name : string, optional, may not be unique
        diameter : float, optional, may be unknown
        """
        # check hazardous to ensure it's a boolean or raise a TypeError
        if not isinstance(hazardous, bool):
            raise TypeError("Hazardous must be a boolean")
        # check diameter to ensure a float
        if not isinstance(diameter, float):
            raise TypeError("Diameter must be a float")

        # Initialize variables with provided arguments
        self.designation = str(designation)
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name is not None:
            return self.designation + " (" + self.name + ")"
        else:
            return self.designation

    def get_designation(self):
        """Return the designation of this NEO."""
        return self.designation

    def __str__(self):
        """Return `str(self)`."""
        # Update diameter if there is a diameter
        if not math.isnan(self.diameter):
            temp_diameter = " has a diameter of " + str(self.diameter) + "km"
        else:
            temp_diameter = ""

        # Update string based on if NEO is hazardous
        if self.hazardous:
            temp_haz = "is potentially hazardous"
        else:
            temp_haz = "is not potentially hazardous"
        return f"NearEarthObject {self.fullname}{temp_diameter} and {temp_haz}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r}, approaches={self.approaches!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, time, distance, velocity, neo, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        time : the time of the closest approach to Earth in UTC
        distance : the nominal approach distance in astronomical units
        velocity : the relative approach velocity in kilometers per second
        neo : the designation of the near-Earth object
        """
        # Set attributes for the Close Approach object
        self._designation = neo
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.neo.fullname

    def get_designation(self):
        """Return the designation of this NEO."""
        return self._designation

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, {self.fullname} approaches Earth at a distance of {self.distance:.2f} AU and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
