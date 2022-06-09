import os
import datetime
from typing import List
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (Dimension, Metric, DateRange, Metric, OrderBy, 
                                               FilterExpression, MetricAggregation, CohortSpec)
from google.analytics.data_v1beta.types import RunReportRequest, RunRealtimeReportRequest


class GA4Exception(Exception):
    '''base class for GA4 exceptions'''

class GA4RealTimeReport:
    """class to query GA4 real time report
    More information: https://support.google.com/analytics/answer/9271392?hl=en
    """

    def __init__(self, property_id):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient()

    def query_report(self, dimensions=List[str], metrics=List[Metric]):
        """
        :param dimensions: categorical attributes (age, country, city, etc)
        :type dimensions: [dimension type]
                :param dimensions: categorical attributes (age, country, city, etc)

        :param metrics: numeric attributes (views, user count, active users)
        :type metrics: [metric type]

        """
        try:
            dimension_list = [Dimension(name=dim) for dim in dimensions]
            metrics_list = [Metric(name=m) for m in metrics]
            
            report_request = RunRealtimeReportRequest(
                property=f'properties/{self.property_id}',
                dimensions=dimension_list,
                metrics=metrics_list
            )
            response = self.client.run_realtime_report(report_request)

            # construct the dataset
            headers = [header.name for header in response.dimension_headers] + [header.name for header in response.metric_headers]
            rows = []
            for row in response.rows:
                rows.append(
                    [dimension_value.value for dimension_value in row.dimension_values] + \
                    [metric_value.value for metric_value in row.metric_values])            

            return {'headers': headers, 'rows': rows}
        except Exception as e:
            raise GA4Exception(e)


class GA4:
    def __init__(self, property_id):
        self.property_id = property_id

    def test(self):
        try:
            print(1/0)
        except Exception as e:
           raise GA4Exception(e)

if __name__ == '__main__':
    # create an environment variable for GA to access the service account client file
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ga4_service_acct.json'    
    property_id = '307310528'

    lst_dimension = ['country', 'city', 'deviceCategory']
    lst_metrics = ['activeUsers']

    ga4_realtime = GA4RealTimeReport(property_id)
    report = ga4_realtime.query_report(
        dimensions=lst_dimension,
        metrics=lst_metrics
    )

    df = pd.DataFrame(columns=report['headers'], data=report['rows'])

    ga4 = GA4(property_id)
    ga4.test()