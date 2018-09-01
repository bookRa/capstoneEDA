import requests
import json
import pandas as pd

# test


def pushshift_to_the_limit(search_term):
    '''Aggregates mentions of term on Reddit thru comments and submissions'''

    comment_url = "https://api.pushshift.io/reddit/search/comment/"
    subm_url = "https://api.pushshift.io/reddit/search/submission/"

    comm_json = requests.get(
        f"{comment_url}?q={search_term}&aggs=created_utc&frequency=day&size=0")
    subm_json = requests.get(
        f"{subm_url}?q={search_term}&aggs=created_utc&frequency=day&size=0")
    comm_data = json.loads(comm_json.content)['aggs']['created_utc']
    # Now the data are in array format
    subm_data = json.loads(subm_json.content)['aggs']['created_utc']

    # Organize the responses into dicts, to load to pandas

    comm_dict = {
        "day": [x['key'] for x in comm_data],
        f"comments": [x['doc_count'] for x in comm_data],
    }
    subm_dict = {
        "day": [x['key'] for x in subm_data],
        f"submissions": [x['doc_count'] for x in subm_data],
    }

    comm_df = pd.DataFrame(comm_dict)
    comm_df.day = pd.to_datetime(comm_df.day, unit='s')

    subm_df = pd.DataFrame(subm_dict)
    subm_df.day = pd.to_datetime(subm_df.day, unit='s')

    tot_df = comm_df.merge(subm_df, on='day', how='outer').fillna(0)

    tot_df['total'] = tot_df['comments']+tot_df['submissions']

    return tot_df
