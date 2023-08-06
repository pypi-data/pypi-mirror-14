# coding: utf8

import pandas as pd
import numpy as np
from datetime import datetime
from .json_requests import send_json_request
from .tools import is_string_type, get_json_value, build_list, to_datetime

TimeSeries_UDF_endpoint = 'TimeSeries'

Calendar_Values = ['native', 'tradingdays', 'calendardays']
Corax_Values = ['adjusted', 'unadjusted']


def get_timeseries(rics, start_date=None, end_date=None, output='pandas', interval='daily', fields=None, count=None, calendar=None, corax=None, debug=False):
    """
    Returns historical data on one or several RICs

    Parameters
    ----------
    rics: string or list
        List of RICs to retrieve historical data for
    start_date: date
        Starting date and time of the historical range
    end_date: date
        End date and time of the historical range
    output: string
        Output data format.
        Possible values ['raw','pandas'] (Default 'pandas')
    interval: string
        Data interval.
        Examples : 'tick', 'minute', 'hour', 'daily', 'weekly', 'monthly', 'quarterly', 'yearly' (Default 'tick')
    fields: list
        Use this parameter to filter the returned fields set.
        By default all fields are returned.
    count: int
        Max number of data points retrieved
    calendar: string
        Possible values ['native', 'tradingdays', 'calendardays']
    corax: string
        ['adjusted', 'unadjusted']
    debug: bool
        If true then the json request and response are logged.

    output: string
        Define the returned format : pandas or raw json
        Value in ['pandas', 'raw']
        Default : 'pandas'

    Raises
    ------
    Exception
        If request fails or if server returns an error
    ValueError
        If a parameter type or value is wrong

    Examples
    --------
    >>> import eikon as ek
    >>> ek.set_app_id('set your app id here')
    >>> req = ek.get_timeseries(["MSFT.O"], start_date = "2016-01-01T15:04:05",
    >>>                          end_date = "2016-01-29T15:04:05", interval="daily")
    """
    # set the ric(s) in the payload
    payload = {'rics': build_list(rics, 'rics')}

    if start_date is not None:
        payload.update({'startdate': to_datetime(start_date).isoformat()})

    if end_date is None:

        end_date = datetime.now().isoformat()
    else:
        end_date = to_datetime(end_date).isoformat()
    payload.update({'enddate': end_date})

    # check the output
    if output not in ['raw', 'pandas']:
        raise ValueError('output must be in ["raw","pandas"]')

    # set the interval in the payload
    if is_string_type(interval):
        payload.update({'interval': interval})
    else:
        raise ValueError('interval must be a string')

    # set the field(s) in the payload
    if fields is None:
        _fields = ['*']
    elif is_string_type(fields):
        _fields = fields.upper().split()
    elif type(fields) is list:
        _fields = [x.upper() for x in fields]
    else:
        raise ValueError('fields must be a list of string')

    if '*' in _fields:
        _fields = ['*']
    elif 'TIMESTAMP' not in _fields:
        _fields.append('TIMESTAMP')

    payload.update({'fields': _fields})

    # set the count in the payload
    if count is not None:
        if type(count) is int:
            payload.update({'count': count})
        elif is_string_type(count):
            payload.update({'count': int(count)})
        else:
            raise ValueError('count must be a integer')

    if calendar is not None:
        if is_string_type(calendar):
            payload.update({'calendar': calendar})
        else:
            raise AttributeError('calendar must be a string')

    if corax is not None:
        if is_string_type(corax):
            payload.update({'corax': corax})
        else:
            raise AttributeError('corax must be a string')

    result = send_json_request(TimeSeries_UDF_endpoint, payload, debug=debug)

    if output.lower() == 'raw':
        return result

    return convert_json_to_pandas(result['timeseriesData'])


def is_tsi_error(json_timeseries_data):
    status_code = get_json_value(json_timeseries_data, 'statusCode')
    if status_code == 'Error':
        return True


def convert_json_to_pandas(json_timeseries_data):
    timeseries_dataframes = {}
    for json_timeserie_data in json_timeseries_data:
        _ric = json_timeserie_data['ric']
        if is_tsi_error(json_timeserie_data):
            timeseries_dataframes[_ric] = None
            continue

        _fields = [field['name'] for field in json_timeserie_data['fields']]
        _timestamp_index = _fields.index('TIMESTAMP')
        # remove timestamp from fields (timestamp is used as index for dataframe)
        _fields.pop(_timestamp_index)

        # build numpy array with all datapoints
        _numpy_array = np.array(json_timeserie_data['dataPoints'])
        # build timestamp as index for dataframe
        _timestamp_array = np.array(_numpy_array[:, _timestamp_index], dtype='datetime64')
        # remove timestamp column from numpy array
        _numpy_array = np.delete(_numpy_array, np.s_[_timestamp_index], 1)

        timeseries_dataframe = pd.DataFrame(_numpy_array, columns=_fields, index=_timestamp_array, dtype='f8')
        timeseries_dataframes[_ric] = timeseries_dataframe

    return timeseries_dataframes
