import json
from lib import brackets
from lib.model import optimize

with open('brackets.json', 'r') as file:
    BRACKETS_REF = json.load(file)

MAX_ROUNDS = 3

def http_entrypoint(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using flask make_response
    """
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type, Accept',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    body_data = request.json
    nb_players = body_data['nb_players']
    groups = body_data['groups']
    minimization_power = body_data['minimization_power']
    matches = brackets.build_matches(BRACKETS_REF[str(nb_players)], MAX_ROUNDS)
    if minimization_power == 0:
        seeding_alternative = None
        deviation_score = 0
    else:
        model_result = optimize(nb_players, matches, groups, minimization_power)
        seeding_alternative = model_result['alternative_seeding']
        deviation_score = model_result['deviation_score']
        # Update groups to reflect new team seedings
        groups = {group: [seeding_alternative[el] for el in members]
                    for group, members in groups.items()}
    collides = brackets.get_collides(matches, groups)
    return ({
        "status": "OK",
        "deviation_score": deviation_score,
        "seeding_alternative": seeding_alternative,
        "collides": collides,
        "total_collide_score": sum([el['prob'] for el in collides]),

    }, 200, headers)
