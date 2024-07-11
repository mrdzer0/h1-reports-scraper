import requests
import json
import urllib.parse

x = 0
while x < 500000:
    graphql_query = {
    "operationName": "CompleteHacktivitySearchQuery",
    "variables": {
        "userPrompt": 'null',
        "queryString": "disclosed:true",
        "size": 25,
        "from": 0 + x,
        "sort": {
            "field": "disclosed_at", #latest_disclosable_activity_at 
            "direction": "DESC"
        },
        "product_area": "hacktivity",
        "product_feature": "overview"
    },
    "query": "query CompleteHacktivitySearchQuery($queryString: String!, $from: Int, $size: Int, $sort: SortInput!) {\n  me {\n    id\n    __typename\n  }\n  search(\n    index: CompleteHacktivityReportIndexService\n    query_string: $queryString\n    from: $from\n    size: $size\n    sort: $sort\n  ) {\n    __typename\n    total_count\n    nodes {\n      __typename\n      ... on CompleteHacktivityReportDocument {\n        id\n        _id\n        reporter {\n          id\n          name\n          username\n          ...UserLinkWithMiniProfile\n          __typename\n        }\n        cve_ids\n        cwe\n        severity_rating\n        upvoted: upvoted_by_current_user\n        public\n        report {\n          id\n          databaseId: _id\n          title\n          substate\n          url\n          disclosed_at\n          report_generated_content {\n            id\n            hacktivity_summary\n            __typename\n          }\n          __typename\n        }\n        votes\n        team {\n          handle\n          name\n          medium_profile_picture: profile_picture(size: medium)\n          url\n          id\n          currency\n          ...TeamLinkWithMiniProfile\n          __typename\n        }\n        total_awarded_amount\n        latest_disclosable_action\n        latest_disclosable_activity_at\n        submitted_at\n        disclosed\n        has_collaboration\n        __typename\n      }\n    }\n  }\n}\n\nfragment UserLinkWithMiniProfile on User {\n  id\n  username\n  __typename\n}\n\nfragment TeamLinkWithMiniProfile on Team {\n  id\n  handle\n  name\n  __typename\n}\n"
    }

    graphql_endpoint = 'https://hackerone.com/graphql'
    response = requests.post(graphql_endpoint, json=graphql_query)
    # print(response.text)
    if response.status_code == 200:
        data = response.json()
        with open('h1reports.txt', 'a') as f:
            for i in data["data"]["search"]['nodes']:
                url = i['report']['url']
                judul = i['report']['title']
                name = i['team']['handle']
                cwe = i['cwe']
                # print(f"{url}")
                print(f"{url} - {name} - {cwe} - {judul}")
                f.write(f"{url} - {name} - {cwe} - {judul}" + '\n')
        
    else:
        print(f"Request failed with status code: {response.status_code}")

    x += 25