
import os
import yaml
import json
import pathlib
from urllib import request, parse
from enetpulse.util import maybe_list

scope_data_types = yaml.load(pathlib.Path('enetpulse/static/scope_data_type.yml').open())


def json_request(url):
    resp = request.urlopen(url)
    data = resp.read()
    return json.loads(data.decode('utf-8'))


def build_url(path, query_params=None):
    query_params = query_params or {}
    scheme = 'http'
    netloc = 'demo.eapi.enetpulse.com'
    query_params.update({
        'username': os.environ['ENETPULSE_USERNAME'],
        'token': os.environ['ENETPULSE_TOKEN']
    })
    query = parse.urlencode({k: maybe_list(v) for k, v in query_params.items()}, doseq=True)
    params = ''
    fragment = ''
    url = request.urlunparse((scheme, netloc, path, params, query, fragment))
    print(url)
    return url


def get_sports():
    data = json_request(build_url('/sport/list/'))
    return data['sports']


def get_tournament_templates(sport_id):
    data = json_request(build_url('/tournament_template/list/', {'sportFK': sport_id}))
    return data['tournament_templates']


def get_tournaments(tournament_template_id):
    data = json_request(build_url('/tournament/list/', {'tournament_templateFK': tournament_template_id}))
    return data['tournaments']


def get_tournament_stages(tournament_template_id, tournament_id):
    params = {'tournament_templateFK': tournament_template_id, 'tournamentFK': tournament_id}
    data = json_request(build_url('/tournament_stage/list/', params))
    return data['tournament_stages']


def get_event_fixtures(sport_id=None, tournament_template_id=None, tournament_stage_id=None, date=None):
    params = {
        'sportFK': sport_id, 'tournament_templateFK': tournament_template_id,
        'tournament_stageFK': tournament_stage_id, 'date': date
    }
    params = {k: v for k, v in params.items() if v is not None}
    assert len(list({k for k in params if k not in ('date',)})) == 1
    data = json_request(build_url('/event/fixtures/list/', params))
    return data['events']


def get_event_results(sport_id=None, tournament_template_id=None, tournament_stage_id=None, date=None):
    params = {
        'sportFK': sport_id, 'tournament_templateFK': tournament_template_id, 'tournament_stageFK': tournament_stage_id,
        'date': date
    }
    params = {k: v for k, v in params.items() if v is not None}
    assert len(list({k for k in params if k not in ('date',)})) == 1
    data = json_request(build_url('/event/results/list/', params))
    return data['events']


def get_event_details(event_id, extended_results='yes'):
    params = {'id': event_id, 'includeExtendedResults': extended_results}
    params = {k: v for k, v in params.items() if v is not None}
    data = json_request(build_url('/event/details/list/', params))
    return data['event']


def build_event_df(event_id):
    import pandas as pd
    events = get_event_details(event_id=event_id)
    data = events['2503707']['event_participants']
    df = pd.concat([pd.DataFrame(v['scope_result']).T for v in data.values()])
    df.loc[:, 'scope_data_type'] = df['scope_data_typeFK'].astype(int).map(scope_data_types)
    return df


def main():

    event_ids = [
        '2504554', '2505039', '2505035', '2506750', '2505038', '2505564', '2507464', '2506463', '2505840', '2505584',
        '2505823', '2505511', '2506406', '2505585', '2504991', '2506756', '2504944', '2505695', '2507486', '2505563',
        '2506264', '2506549', '2506593'
    ]


if __name__ == '__main__':
    main()
