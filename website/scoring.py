from numpy import dot
from numpy.linalg import norm


def top10(curr_user,user_list):

    curr_user_info = get_user_info(curr_user)
    result = {}
    for usr in user_list:
        other_user = get_user_info(usr)
        score = scoring(curr_user_info, other_user)
        result[usr] = score

    sorted_result = [k for k, v in sorted(result.items(), key=lambda item: item[1])]

    return sorted_result[:10]


def get_user_info(user):
    user_age = user.age
    user_gender = 1 if (user.gender == 'Male') else 0
    user_lat = user.latitude
    user_lng = user.longitude
    user_sporty = user.sporty_post
    user_non_sporty = 1 - user_sporty
    user_pos = user.positive_post
    user_neu = user.neutral_post
    user_neg = user.negative_post

    return [user_age, user_gender, user_lat, user_lng, user_sporty, user_non_sporty, user_pos, user_neu, user_neg]


def scoring(curr_user, user):
    return dot(curr_user, user)/(norm(curr_user)*norm(user))