# coding: utf8

import eikon.json_requests
from .tools import is_string_type, to_datetime
from collections import namedtuple
import dateutil.parser
import pandas as pd
import numpy as np

News_Headlines_UDF_endpoint = "News_Headlines"
News_Story_UDF_endpoint = "News_Story"

Headline_Selected_Fields = ['versionCreated', 'text', 'storyId']
Headline_Selected_Fields_ = ['text', 'storyId', 'bodyType', 'displayDirection', 'documentType',
                             'isAlert', 'language', 'permIDs', 'products', 'rcs', 'reportCode', 'sourceCode',
                             'sourceName', 'versionCreated']


def get_news_headlines(query='Topic:TOPALL and Language:LEN', headlines_count=10, date_from=None,
                       date_to=None, output='pandas', debug=False):
    """
    Returns a list of news headlines as a pandas DataFrame

    Parameters
    ----------
    query: string, optional
        Free text string that specifies the news headline search criteria.
        The text can contain RIC codes, company names, country names and
        operators (AND, OR, NOT, parentheses, quotes for explicit search…).
        Tip: Append 'R:' in front of RIC names to improve performances.
        Default: 'Topic:TOPALL AND Language:LEN'

    headlines_count: int, optional
        Max number of headlines retrieved
        Value Range: [0-100] (Default 10)

    date_from: datetime (optional)
        Beginning of date range
        Format: ISO format ('%Y-%m-%dT%H:%M:%S')
        Example: '2016-01-01T15:04:05'
        Default: None

    date_to: '%Y-%m-%dT%H:%M:%S' datetime format (optional)
        End of date range
        Format: ISO format ('%Y-%m-%dT%H:%M:%S')
        Example: '2016-01-05T15:04:05'
        Default: None

    output: string
        Define the returned format : pandas or json
        Value in ['pandas', 'raw']
        Default: 'pandas'

    debug: bool
        If true then the json request and response are logged.
        Default: False

    Returns
    -------
    pandas.DataFrame
        Returns a DataFrame of news headlines with the following columns:

        - text                : Text of the Headline
        - story_id            : Identifier to be used to retrieve the full story using the get_news_story function
        - body_type           : Defines the story content type. Possible values are: Story, Video, Research, WebUrl
        - display_direction   : Define the text direction. Useful when the news is written in Arabic for instance.
        - document_type       : Type of the document
        - first_created       : News publication Date and Time
        - version_created     : Date of the latest update on the news
        - is_alert            : Indicates whether the news is an alert
        - language            : News Language
        - perm_IDs            : List of permanent IDs associated with the news
        - products            : Thomson Reuters internal tagging information
        - rcs                 : Reuters Code Scheme
        - report_code         : Thomson Reuters internal metadata information
        - source_code         : Code of the news issuer
        - source_name         : News issuer name

    Raises
    ----------
    Exception
        If http request fails or if server returns an error
    AttributeError
        If a parameter type is wrong

    Examples
    --------
    >>> import eikon as ek
    >>> ek.set_app_id('set your app id here')
    >>> headlines = ek.get_news_headlines("R:MSFT.O gates",5)
    """

    # check parameters type and values
    if not is_string_type(query):
        raise ValueError('query must be a string')
    if type(headlines_count) is not int:
        raise ValueError('headlines_count must be an integer')
    elif headlines_count < 0:
        raise ValueError('headlines_count must be equal or greater than 0')

    # build the payload
    payload = {'number': str(headlines_count),
               'attributionCode': 'string', 'productName': 'eikon',
               'productVersion': '1.0.0', 'query': query}

    if date_from is not None:
        payload.update({'dateFrom': to_datetime(date_from).isoformat()})

    if date_to is not None:
        payload.update({'dateTo': to_datetime(date_to).isoformat()})

    result = eikon.json_requests.send_json_request(News_Headlines_UDF_endpoint, payload, debug=debug)

    if output.lower() == 'raw':
        return result

    json_headline_array = result['headlines']

    return convert_json_headlines_to_pandas(json_headline_array)


def convert_json_headlines_to_pandas(json_headline_array):
    first_created = [headline['firstCreated'] for headline in json_headline_array]
    headlines = [[headline[field] for field in Headline_Selected_Fields]
                 for headline in json_headline_array]
    headlines_dataframe = pd.DataFrame(headlines, np.array(first_created, dtype='datetime64'), Headline_Selected_Fields)
    headlines_dataframe['versionCreated'] = headlines_dataframe.versionCreated.apply(pd.to_datetime)
    return headlines_dataframe


def get_news_story(story_id, output='pandas', debug=False):
    """
    Return a news story as a string

    Parameters
    ----------
    story_id: string
        Story identifier retrieved with a get_news_headlines request.

    output: string
        Define the returned format : pandas or json
        Value in ['pandas', 'raw']
        Default : 'pandas'

    debug: bool
        If true then the json request and response are returned.
        Default: False

    Raises
    ------
    Exception
        If http request fails or if Thomson Reuters Services return an error
    ValueError
        If a parameter type or value is wrong

    Examples
    --------
    >>> import eikon as ek
    >>> ek.set_app_id('set your app id here')
    >>> req = ek.get_news_story("urn:newsml:reuters.com:20160113:nDJAM01641:1")
    >>> print(req)
    """

    if not is_string_type(story_id):
        raise ValueError('storyId must be a string')

    # build the request
    payload = {'attributionCode': 'string', 'productName': 'TBD', 'productVersion': 'TBD', 'storyId': story_id}
    result = eikon.json_requests.send_json_request(News_Story_UDF_endpoint, payload, debug=debug)

    if output.lower() == 'raw':
        return result

    return result['story']['storyHtml']
