from itertools import combinations


def ouput_proba(x, y):
    return (y-x)/(2*(x+y)) + 0.5


def ouput_match(xprobs, yprobs):
    winner = {}
    loser = {}
    for x, xprob in xprobs.items():
        for y, yprob in yprobs.items():
            match_prob = xprob*yprob
            prob = ouput_proba(x, y)
            xwin = prob*match_prob
            ywin = (1-prob)*match_prob
            if x in winner:
                winner[x] += xwin
            else:
                winner[x] = xwin
            if y in winner:
                winner[y] += ywin
            else:
                winner[y] = ywin
            if x in loser:
                loser[x] += ywin
            else:
                loser[x] = ywin
            if y in loser:
                loser[y] += xwin
            else:
                loser[y] = xwin
    return winner, loser


def build_matches(data, max_rounds):
    results = {}
    results_next_round = {}
    done_keys = []
    matches = {}
    # check 3 rounds:
    for i in range(max_rounds):
        # Check all matches that we haven't seen
        for key, players in data.items():
            if key not in done_keys:
                # Get the players if they're determined
                player_probs = []
                for player in players:
                    if type(player) == type(1):
                        player_probs.append({player: 1})
                    elif player in results:
                        player_probs.append(results[player])
                    else:
                        break
                # If both players are determined
                if len(player_probs) == 2:
                    # we save it
                    matches[key] = player_probs
                    done_keys.append(key)
                    # compute and save the match output
                    winner, loser = ouput_match(player_probs[0], player_probs[1])
                    results_next_round[f'winner of {key}'] = winner
                    results_next_round[f'loser of {key}'] = loser
        results = {**results, **results_next_round}
    return matches


def get_proba_encounter(i, j, matches):
    rep = 0
    for key, el in matches.items():
        player1 = el[0]
        player2 = el[1]
        probi1 = player1[i] if i in player1 else 0
        probj1 = player1[j] if j in player1 else 0
        probi2 = player2[i] if i in player2 else 0
        probj2 = player2[j] if j in player2 else 0
        rep += probi1*probj2 + probj1*probi2
    return rep


def build_encounter_prob_matrix(nb_players, matches):
    matrix = []
    for i in range(nb_players):
        row = []
        for j in range(nb_players):
            # Ignore half of the matrix to win some time
            if j <= i:
                row.append(0)
            else:
                row.append(get_proba_encounter(i, j, matches))
        matrix.append(row)
    # Apply symmetry
    for i in range(nb_players):
        for j in range(nb_players):
            if j < i:
                matrix[i][j] = matrix[j][i]
    return matrix


def get_encounters(i, j, matches):
    encounters = {}
    for key, el in matches.items():
        player1 = el[0]
        player2 = el[1]
        probi1 = player1[i] if i in player1 else 0
        probj1 = player1[j] if j in player1 else 0
        probi2 = player2[i] if i in player2 else 0
        probj2 = player2[j] if j in player2 else 0
        prob = probi1*probj2 + probj1*probi2
        if prob != 0:
            encounters[key] = prob
    return encounters


def get_collides(matches, groups):
    '''
    groups: a dict that asociate the group name (str) to the list
    of the seedings of the different group members (Int[]).
    Keep in mind seeding starts from 0 here.
    '''
    collides = {}
    seen = []
    for group_name, members in groups.items():
        for (i, j) in combinations(members, 2):
            key = tuple(sorted([i, j]))
            # If this couple is in multiple groups
            if key in seen:
                if key in collides:
                    collides[key]['groups'].append(group_name)
            else:
                encounters = get_encounters(i, j, matches)
                total = sum([el for key, el in encounters.items()])
                if total != 0:
                    collides[key] = {
                        'groups': [group_name],
                        'prob': total,
                        'encounters': encounters,
                    }
    formatted = [{'players': [list(key)], **el} for key, el in collides.items()]
    formatted.sort(key = lambda t: t['prob'], reverse=True)
    return formatted