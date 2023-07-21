import csv
import logging
import tempfile
from pathlib import Path
from typing import Dict, List

from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
from hdx.utilities.path import get_uuid

from hdro import get_country_data

logger = logging.getLogger(__name__)

_LOOKUP = "hdx-scraper-hdro"
_PROJECT_CONFIG = Path("config") / "project_configuration.yaml"
# TODO: are these the same for every project? Where should they be set?
_MAINTAINER = "196196be-6037-4488-8b71-d786adf4c081"
_ORGANIZATION = "647d9d8c-4cac-4c33-b639-649aad1c2893"


def _main():
    # Setup
    config = Configuration(
        user_agent_lookup=_LOOKUP, project_config_yaml=_PROJECT_CONFIG
    )
    batch = get_uuid()
    # Get the data from the API - takes awhile to loop through all countries
    country_dict = get_country_data()
    # Now loop through each country and create the datasets
    for country_iso3, country_data in country_dict.items():
        # Get the start and end date of the dataset
        # TODO - as well, copy the other metadata
        # Create a dataset
        dataset_name = f"hdro-{country_iso3}"
        dataset = _get_dataset(
            dataset_title=dataset_name,
            dataset_name=dataset_name,
            tags=config.read()["tags"],
        )
        # Add the resource
        with tempfile.TemporaryDirectory as tempdir:
            _generate_resource_from_dict(
                dataset=dataset,
                folder=tempdir,
                filename=f"hdro-{country_iso3}.csv",
                data_json=country_data,
                resourcedata={"name": dataset_name, "title": dataset_name},
            )
            dataset.create_in_hdx(
                remove_additional_resources=True,
                hxl_update=False,
                updated_by_script="HDX Scraper: HDRO",
                batch=batch,
            )


def _get_dataset(dataset_title: str, dataset_name: str, tags: List):
    logger.info(f"Creating dataset: {dataset_title}")
    dataset = Dataset({"name": dataset_name, "title": dataset_title})
    dataset.set_maintainer(_MAINTAINER)
    dataset.set_organization(_ORGANIZATION)
    dataset.set_expected_update_frequency("Every year")
    dataset.set_subnational(False)
    dataset.add_tags(tags)
    return dataset


def _generate_resource_from_dict(
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
        # TODO: this is not going to work if we want to add a HXL row
        writer = csv.DictWriter(f, fieldnames=data_json[0])
        writer.writeheader()
        writer.writerows(data_json)
    resource = Resource(resourcedata)
    resource.set_file_type("csv")
    resource.set_file_to_upload(str(filepath))
    dataset.add_update_resource(resource)
    return resource


if __name__ == "__main__":
    _main()
