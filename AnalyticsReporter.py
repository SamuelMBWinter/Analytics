'''
Google analytics reporter
Outputs graphs of the selcted report.
'''

# Imports
import json
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import datetime as dt

# Google Analytics Data API Imports
from google.analytics.data import AlphaAnalyticsDataClient
from google.analytics.data_v1alpha.types import DateRange
from google.analytics.data_v1alpha.types import Dimension
from google.analytics.data_v1alpha.types import Entity
from google.analytics.data_v1alpha.types import Metric
from google.analytics.data_v1alpha.types import RunReportRequest
from google.analytics.data_v1alpha.types import BatchRunReportsRequest

save_path = '/home/samwinter/dox/Data_Reports/report2021-04-05'

def create_batch_request(dc):
    propertyId = Entity(property_id=dc["entity"]["propertyId"])
    request_ls = []
    for req  in dc["requests"]:
        dateRanges = [ 
                DateRange(
                    start_date=i['startDate'],
                    end_date=i['endDate']
                )
                for i in req["dateRanges"]
            ]
        dims = [Dimension(name=i['name']) for i in req['dimensions']]
        mets = [Metric(name=i['expression']) for i in req['metrics']]

        request_ls.append(
            RunReportRequest(
                date_ranges = dateRanges,
                metrics = mets,
                dimensions = dims
            )
        )
    return BatchRunReportsRequest(entity=propertyId, requests=request_ls)

# Starup te client, make te request, get the response
client = AlphaAnalyticsDataClient()

req = {}
with open("report.json", "r") as f:
    req = json.load(f)

report_request = create_batch_request(req)
response = client.batch_run_reports(report_request)

report_tables = []
for r in response.reports:
    print([i.name for i in r.dimension_headers])
    print([i.name for i in r.metric_headers])
