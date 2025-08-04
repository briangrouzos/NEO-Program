"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # open the file and read the information
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)

        # Create an empty list to store the objects in
        neos = []

        # Use a try statement to catch Type Error exceptions
        try:
            for row in reader:
                # Use if statements to ensure blank information is handled appropriately and convert hazards to booleans
                if row['name'] == '':
                    name = None
                else:
                    name = row['name']
                if row['diameter'] == '':
                    diameter = -1.0
                else:
                    diameter = float(row['diameter'])
                if row['pha'] == 'Y':
                    hazard = True
                else:
                    hazard = False

                # Append neo objects to the list
                neos.append(NearEarthObject(row['pdes'], hazard, name, diameter))
        except TypeError:
            print(TypeError)
    # Return NEO objects in list format
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # read information from JSON file
    with open(cad_json_path, 'r') as infile:
        data = json.load(infile)

    # Create empty approaches array
    approaches = []

    # iterate through the data and create objects
    for row in data['data']:
        time = row[3]
        distance = row[4]
        velocity = row[7]
        neo = row[0]
        approaches.append(CloseApproach(time, distance, velocity, neo))

    # Return approaches array
    return approaches
