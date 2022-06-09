# Google Analytics 4 Python API v1

Simple module to work with Google Analytics 4 API.

Features:
- [x] Run real time report
- [ ] Run Google Analytics report

## Installation

`pip install install google-analytics-data`
Requirements: Python 3.6+

## Basic Usage
1. [Create a Google Cloud Account](console.cloud.google.com/)
2. Start using ga4

```python
import os
import pandas as pd
from ga4 import GA4RealTimeReport

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ga4_service_acct.json'    
property_id = '307310528'

lst_dimension = ['country', 'city', 'deviceCategory']
lst_metrics = ['activeUsers']

ga4_realtime = GA4RealTimeReport(property_id)
report = ga4_realtime.query_report(
    dimensions=lst_dimension,
    metrics=lst_metrics
)

df = pd.DataFrame(data=report['rows'], columns=report['headers'])
print(df)
```
