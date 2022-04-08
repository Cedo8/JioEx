import numpy
from numpy import dot
from numpy.linalg import norm
import math

from .gps_locator import distance


def top10(curr_user,user_list):

    curr_user_info, curr_user_dist = get_user_info(curr_user)
    result = {}
    waiting_list = {}

    for usr in user_list:
        other_user_info, other_user_dist = get_user_info(usr)

        info_score = scoring(curr_user_info, other_user_info)
        dist = distance(curr_user_dist, other_user_dist)
        location_score = 1 if dist == 0 else 1/math.log(dist)
        gender_score = 0.51 if curr_user.gender == usr.gender else 0.49

        pos_sentiment = usr.positive_post
        neu_sentiment = usr.neutral_post
        neg_sentiment = usr.negative_post

        score = 0.50 * info_score + 0.45 * location_score + 0.02 * gender_score + 0.03 * (pos_sentiment + neu_sentiment - neg_sentiment)

        if dist > 3500:
            waiting_list[usr] = score
        else:
            result[usr] = score

    sorted_result = [k for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)]
    final_result = sorted_result[:10]
    result_len = len(final_result)

    if result_len < 10:
        sorted_waiting = [k for k, v in sorted(waiting_list.items(), key=lambda item: item[1], reverse=True)]
        final_result = numpy.concatenate((final_result, sorted_waiting[:10 - result_len]))

    return final_result


def get_user_info(user):
    user_age = user.age / 100
    user_fitness = math.log(user.fitness * 100) if user.fitness != 0 else 0
    user_lat = user.latitude
    user_lng = user.longitude

    return [user_age, user_fitness], [user_lat, user_lng]


def scoring(curr_user, user):
    return dot(curr_user, user)/(norm(curr_user)*norm(user))


'''
def top10(curr_user,user_list):

    name_1, curr_user_info, curr_user_dist, h_pos, h_neu, h_neg, u_gender = curr_user #get_user_info(curr_user)

    result = {}
    waiting_list = {}
    i = 2
    for usr in user_list:
        name, other_user_info, other_user_dist, pos, neu, neg, o_gender = usr  # get_user_info(usr)
        dist = distance(curr_user_dist, other_user_dist)

        info_score = scoring(curr_user_info, other_user_info)
        location_score = 1 if dist == 0 else 1/math.log(dist)
        #print(location_score)
        #print(info_score)
        gender_score = 0.51 if u_gender == o_gender else 0.49

        #pos_sentiment = usr.positive_post
        #neu_sentiment = usr.neutral_post
        #neg_sentiment = usr.negative_post
        score = 0.50 * info_score + 0.45 * location_score + 0.02 * gender_score + 0.03 * (pos + neu - neg)
        if dist > 3500:
            waiting_list[name] = score
        else:
            result[name] = score
        i += 1

    sorted_result = [k for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)]
    final_result = sorted_result[:10]
    result_len = len(final_result)

    if result_len < 10:
        sorted_waiting = [k for k, v in sorted(waiting_list.items(), key=lambda item: item[1], reverse=True)]
        final_result = numpy.concatenate((final_result, sorted_waiting[:10 - result_len]))

    return final_result

test1 = "pgp",[0.19, math.log(78)], (1.290733508328698, 103.78137548665377), 0.5, 0.3, 0.2, "Male"
test2 = "ke",[0.22, math.log(6)], (1.2927968416866438, 103.78108150612293), 0.5, 0.3, 0.2, "Female"
test3 = "kr",[0.23, math.log(3)], (1.29223908416083, 103.77479440821136), 0.5, 0.3, 0.2, "Male"
test4 = "eu",[0.19, math.log(27)], (1.2932044336368314, 103.77138263833228), 0.5, 0.3, 0.2, "Female"
test5 = "ut",[0.19, math.log(2)], (1.3056681350037735, 103.77389318593198), 0.6, 0.3, 0.1, "Male"
test6 = "rh",[0.30, math.log(4)], (1.300348008415707, 103.7740219319935), 0.5, 0.3, 0.2, "Female"
test7 = "wc",[0.40, math.log(9)], (1.312793655010831, 103.75994178697941), 0.5, 0.3, 0.2, "Male"
test8 = "mcd",[0.50, math.log(5)], (1.2977428830661588, 103.76349546648105), 0.5, 0.3, 0.2, "Female"
test9 = "rvp",[0.70, math.log(3)], (1.3920318624171144, 103.904341234299), 0.5, 0.3, 0.2, "Male"
test10 = "clem",[0.19, math.log(7)], (1.3157004460298074, 103.76478771351344), 0.6, 0.3, 0.1, "Male"
test11 = "rec",[0.20, math.log(9)], (1.3907007423868016, 103.90376100524107), 0.5, 0.3, 0.2, "Female"
test12 = "seng",[0.23, math.log(6)], (1.3899334979896163, 103.90010195607287), 0.5, 0.3, 0.2, "Male"

result = [test12, test2, test3, test4, test5, test6, test7, test8, test9, test10,test11]



print(top10(test1,result))'''
