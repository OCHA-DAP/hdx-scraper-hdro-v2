from typing import Dict, List
from pathlib import Path
import csv
import logging

from hdx.data.dataset import Dataset
from hdx.data.resource import Resource

from hdro import get_country_data

logger = logging.getLogger(__name__)

_LOOKUP = "hdx-scraper-hdro"


def main():
    # Setup
    folder = Path(_LOOKUP)
    # Get the data from the API
    country_dict = get_country_data()
    # Now loop through each country and create the datasets
    for country_iso3, country_data in country_dict.items():
        # Create a dataset
        name = f"hdro-{country_iso3}"
        dataset = get_dataset(title=name, tags=["development indicator"], name=name)
        # Add the resource
        resource = generate_resource_from_dict(
            dataset=dataset,
            folder=folder,
            filename=f"hdro-{country_iso3}.csv",
            data_json=country_data,
            resourcedata={"name": name, "title": name},
        )


def get_dataset(title: str, tags: List, name):
    logger.info(f"Creating dataset: {title}")
    dataset = Dataset({"name": name, "title": title})
    dataset.set_maintainer("196196be-6037-4488-8b71-d786adf4c081")
    dataset.set_organization("647d9d8c-4cac-4c33-b639-649aad1c2893")
    dataset.set_expected_update_frequency("Every year")
    dataset.set_subnational(False)
    dataset.add_tags(tags)
    return dataset


def generate_resource_from_dict(
    dataset: Dataset,
    folder: Path,
    filename: str,
    data_json: Dict,
    resourcedata: Dict,
) -> Resource:
    """Adapted from generate_resource_from_csv. Could add to HDX libraries
    if Mike agrees.

    Args:
        dataset: (Dataset) - should be self if this becomes a method in the
        dataset class
        folder (Path): Folder to which to write csv file
        filename (str): Filename of csv file
        data_json (dict): The data taken from the API JSON
        resourcedata (Dict): Resource data

    Returns:
        Resource: The created resource
    """
    filepath = folder / filename
    with open(filepath, "w") as f:
        writer = csv.DictWriter(f, fieldnames=data_json[0])
        writer.writeheader()
        writer.writerows(data_json)
    resource = Resource(resourcedata)
    resource.set_file_type("csv")
    resource.set_file_to_upload(str(filepath))
    dataset.add_update_resource(resource)
    return resource


if __name__ == "__main__":
    main()
