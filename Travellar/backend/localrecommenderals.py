import pandas as pd
import numpy as np

from .models import Rating, Destination


def initLocalRecommenderALS():

    destination = pd.DataFrame(list(Destination.objects.all().values('destinationID', 'destinationName', 'destinationType')))
    ratings = pd.DataFrame(list(Rating.objects.all().values('userID', 'destinationID', 'rating')))

    destination_names = destination.destinationName.tolist()

    rp = ratings.pivot_table(index=['userID'], columns=['destinationID'], values='rating')
    rp = rp.fillna(0)
    Q = rp.values

    W = Q>0.5
    W[W == True] = 1
    W[W == False] = 0
    # To be consistent with our Q matrix
    W = W.astype(np.float64, copy=False)

    lambda_ = 0.1
    n_factors = 100
    m, n = Q.shape
    n_iterations = 2
    X = 5 * np.random.rand(m, n_factors)
    Y = 5 * np.random.rand(n_factors, n)

    weighted_errors = []
    for ii in range(n_iterations):
        for u, Wu in enumerate(W):
            X[u] = np.linalg.solve(np.dot(Y, np.dot(np.diag(Wu), Y.T)) + lambda_ * np.eye(n_factors), np.dot(Y, np.dot(np.diag(Wu), Q[u].T))).T
        for i, Wi in enumerate(W.T):
            Y[:,i] = np.linalg.solve(np.dot(X.T, np.dot(np.diag(Wi), X)) + lambda_ * np.eye(n_factors),np.dot(X.T, np.dot(np.diag(Wi), Q[:, i])))
        weighted_errors.append(get_error(Q, X, Y, W))
        print('{}th iteration is completed'.format(ii))
    weighted_Q_hat = np.dot(X,Y)
    Q_hat=weighted_Q_hat

    result = print_recommendations(W,Q,Q_hat,destination_names,m)
    return result

def get_error(Q, X, Y, W):
    return np.sum((W * (Q - np.dot(X, Y)))**2)


def print_recommendations(W, Q, Q_hat, destination_names, m, user=3):
    # print(W) # 0/1 matrix
    # print(Q) # 0-5.0 matrix
    # print(Q_hat) # weighting between -5 - +5 matrix
    # print(len(destination_names)) # 642 destinations
    # print(m) # number of users

    Q_hat -= np.min(Q_hat)
    Q_hat *= float(5) / np.max(Q_hat)

    destination_ids = np.argmax(Q_hat - 5 * W, axis=1)

    for jj, destination_id in zip(range(m), destination_ids):
        if jj+1 == user:
            # print('User {} liked {}\n'.format(jj +1, ', '.join([destination_names[ii] for ii, qq in enumerate(Q[jj]) if qq > 3])))
            # print('User {} did not like {}\n'.format(jj +1, ', '.join([destination_names[ii] for ii, qq in enumerate(Q[jj]) if qq < 3 and qq != 0])))
            print('\n User {} recommended destination is {}'.format(jj +1, destination_names[destination_id]))
            place = destination_names[destination_id]
            return place
            #print('\n' + 100 *  '-' + '\n')
            # print(m)
            # print(destination_id)
# if __name__ == "__main__":
#     main()
