import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

import datetime

from django.db.models import Count

from .models import Rating, Destination

destination = pd.DataFrame(list(Destination.objects.all().values('destinationID', 'destinationName', 'destinationType')))
rating = pd.DataFrame(list(Rating.objects.all().values('userID', 'destinationID', 'rating')))


def initLocalRecommenderPearson():
    # not working
    # rating.destinationID = rating.destinationID.map(replace_rating_destination)

    MF = rating.pivot_table(index=['userID'], columns=['destinationID'], values='rating')
    recs = get_recommendations(198, MF, 10)
    print(recs[:10])


# def replace_rating_destination(x):
#     return destination[destination['destinationID'] == x].destinationName.values[0]


def pearson_recommendation(x, y):
    #a = 0
    x_coeff = x - x.mean()
    y_coeff = y - y.mean()
    total_sum = np.sqrt(np.sum(x_coeff ** 2) * np.sum(y_coeff ** 2))
    if total_sum == 0:
        return 0
    if total_sum > 0:
        return np.sum(x_coeff * y_coeff) / np.sqrt(np.sum(x_coeff ** 2) * np.sum(y_coeff ** 2))


def get_recommendations(destination_name, matrix, n_recommendations):
    reviews = []
    for destinationName in matrix.columns:
        if destinationName == destination_name:
            continue
        cor = pearson_recommendation(matrix[destination_name], matrix[destinationName])
        if pd.isnull(cor):
            continue
        else:
            reviews.append((destinationName, cor))
    reviews.sort(key=lambda tup: tup[1], reverse=True)
    return reviews[:n_recommendations]
