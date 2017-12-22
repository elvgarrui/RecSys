#encoding:utf-8
#Usando un sistema de recomendaciÃ³n de tipo filtrado colaborativo basado en Ã­tems. 


from math import sqrt

# Returns a distance-based similarity score for libro1 and libro2
def sim_distance(prefs, libro1, libro2):
    # Get the list of shared_usuarios
    si = {}
    for usuario in prefs[libro1]: 
        if usuario in prefs[libro2]: si[usuario] = 1

        # if they have no ratings in common, return 0
        if len(si) == 0: return 0

        # Add up the squares of all the differences
        sum_of_squares = sum([pow(prefs[libro1][usuario] - prefs[libro2][usuario], 2) 
                    for usuario in prefs[libro1] if usuario in prefs[libro2]])
        
        return 1 / (1 + sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated usuarios
    si = {}
    for usuario in prefs[p1]: 
        if usuario in prefs[p2]: si[usuario] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0: return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])	

    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den

    return r

# Returns the best matches for libro from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs, libro, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, libro, other), other) 
                for other in prefs if other != libro]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Gets recommendations for a libro by using a weighted average of every other user's rankings
def getRecommendations(prefs, libro, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == libro: continue
        sim = similarity(prefs, libro, other)
        # ignore scores of zero or lower
        if sim <= 0: continue
        for usuario in prefs[other]:
            # only score movies I haven't seen yet
            if usuario not in prefs[libro] or prefs[libro][usuario] == 0:
                # Similarity * Score
                totals.setdefault(usuario, 0)
                totals[usuario] += prefs[other][usuario] * sim
                # Sum of similarities
                simSums.setdefault(usuario, 0)
                simSums[usuario] += sim

    # Create the normalized list
    rankings = [(total / simSums[usuario], usuario) for usuario, total in totals.usuarios()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result = {}
    for libro in prefs:
        for usuario in prefs[libro]:
            result.setdefault(usuario, {})
    
            # Flip usuario and libro
            result[usuario][libro] = prefs[libro][usuario]
    return result


def calculateSimilarUsers(prefs, n=10):
    # Create a dictionary of usuarios showing which other usuarios they
    # are most similar to.
    result = {}
    # Invert the preference matrix to be usuario-centric
    usuarioPrefs = transformPrefs(prefs)
    c = 0
    for usuario in usuarioPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(usuarioPrefs))
        # Find the most similar usuarios to this one
        scores = topMatches(usuarioPrefs, usuario, n=n, similarity=sim_distance)
        result[usuario] = scores
    return result

def getRecommendedusuarios(prefs, usuarioMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over usuarios rated by this user
    for (usuario, rating) in userRatings.usuarios():
        # Loop over usuarios similar to this one
        for (similarity, usuario2) in usuarioMatch[usuario]:
            print usuario2
            # Ignore if this user has already rated this usuario
            if usuario2 in userRatings: continue
            # Weighted sum of rating times similarity
            scores.setdefault(usuario2, 0)
            scores[usuario2] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(usuario2, 0)
            totalSim[usuario2] += similarity

    # Divide each total score by total weighting to get an average
    try:
        rankings = [(score / totalSim[usuario], usuario) for usuario, score in scores.usuarios()]
    except ZeroDivisionError:
        rankings = []

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings

