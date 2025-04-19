"""
This tests extracts the full dataset with the dlt rest_api source
# NOTE: for speed reasons we limit to orders in january 2017
"""

import dlt
import pytest
import requests
from dlt.common.destination.dataset import SupportsReadableDataset
from dlt.destinations import duckdb
from dlt.sources.rest_api import rest_api_source
from fastapi.testclient import TestClient

from app.main import app
from tests.utils import EXPECTED_TABLES_COUNTS_JANUARY_2017

app = TestClient(app)


class FastAPISession(requests.Session):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def send(self, prepared_request, **kwargs):
        return self.client.request(
            method=prepared_request.method, url=prepared_request.url
        )


def row_counts(
    dataset: SupportsReadableDataset, tables: list[str] = []
) -> dict[str, int]:
    counts = dataset.row_counts(table_names=tables).arrow()
    if counts is None:
        return {}

    counts = counts.to_pydict()
    return {t: c for t, c in zip(counts["table_name"], counts["row_count"])}


def test_extract_full_dataset():
    """
    This tests extracts the full dataset with the dlt rest_api source
    """
    source = rest_api_source(
        {
            "client": {
                "base_url": "http://localhost:8000/api/v1",
                "paginator": {
                    "type": "header_link",
                },
                "session": FastAPISession(app),
            },
            "resources": [
                "customers",
                "products",
                "stores",
                "supplies",
                # orders includes items
                # we only load orders for january 2017
                {
                    "name": "orders",
                    "endpoint": {
                        "path": "orders",
                        "params": {
                            "page_size": 1000,
                            "start_date": "2017-01-01",
                            "end_date": "2017-01-31",
                        },
                    },
                },
            ],
        },
    )

    pipeline = dlt.pipeline(
        pipeline_name="rest_api_example",
        destination=duckdb(credentials="test.db"),
        dataset_name="rest_api_data",
        dev_mode=True,
    )

    pipeline.run(source)
    assert row_counts(pipeline.dataset()) == EXPECTED_TABLES_COUNTS_JANUARY_2017


@pytest.mark.skip(reason="This is a live test against the deployed shop")
def test_live_jaffle_shop():
    """
    This tests extracts the full dataset with the dlt rest_api source
    """
    source = rest_api_source(
        {
            "client": {
                "base_url": "https://fast-api-jaffle-shop-jz2mh.ondigitalocean.app",
                "paginator": {
                    "type": "header_link",
                },
                "session": FastAPISession(app),
            },
            "resources": [
                "customers",
                "products",
                "stores",
                "supplies",
                # orders includes items
                # we only load orders for january 2017
                {
                    "name": "orders",
                    "endpoint": {
                        "path": "orders",
                        "params": {
                            "start_date": "2017-01-01",
                            "end_date": "2017-01-31",
                        },
                    },
                },
            ],
        },
    )

    pipeline = dlt.pipeline(
        pipeline_name="rest_api_example",
        destination=duckdb(credentials="test.db"),
        dataset_name="rest_api_data",
        dev_mode=True,
    )

    pipeline.run(source)
    assert row_counts(pipeline.dataset()) == {
        "customers": 935,
        "products": 10,
        "stores": 6,
        "supplies": 65,
        "orders": 3303,  # 3303 orders in january 2017
        "orders__items": 5072,
    }
