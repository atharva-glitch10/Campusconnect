def calculate_similarity(user1_interests, user2_interests):
    """Jaccard similarity between two interest lists."""
    set1 = set(user1_interests)
    set2 = set(user2_interests)
    if not set1 and not set2:
        return 0.0

    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return round(intersection / union, 4)


def find_matches(user_data):
    """
    Given { username: [interests...], ... },
    return a list of matches sorted by similarity (descending).
    Only pairs with at least one shared interest are included.
    """
    users = list(user_data.keys())
    matches = []

    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            u1, u2 = users[i], users[j]
            score = calculate_similarity(user_data[u1], user_data[u2])

            if score > 0:
                matches.append({
                    "user1": u1,
                    "user2": u2,
                    "similarity": score
                })

    matches.sort(key=lambda x: x["similarity"], reverse=True)
    return matches