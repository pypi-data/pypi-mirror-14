"""
    Unit tests for ReliefF.
"""

from ReliefF import ReliefF
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split

def test_init():
    """Make sure ReliefF instantiates correctly"""
    fs = ReliefF(n_neighbors=50, n_features_to_keep=100)
    assert fs.n_neighbors == 50
    assert fs.n_features_to_keep == 100

def test_fit():
    """Make sure ReliefF fits correctly"""
    data = pd.read_csv('data/GAMETES-test.csv.gz')
    X_train, X_test, y_train, y_test = train_test_split(data.drop('class', axis=1).values,
                                                        data['class'].values,
                                                        random_state=34895)

    fs = ReliefF(n_neighbors=100, n_features_to_keep=5)
    fs.fit(X_train, y_train)

    correct_top_features = np.array([94, 98, 96, 92, 99, 93, 97, 95, 45, 49, 33, 79, 57, 58, 28, 18, 75,
                                      3, 56, 84, 62, 86,  7, 15, 82, 41, 48, 64, 14, 25, 66, 36, 29, 42,
                                     35, 52, 37, 27, 21, 77, 46, 68, 80, 16, 61, 87, 17,  6, 72, 81, 31,
                                     32, 40,  0, 91,  4, 85, 54, 67,  1, 53, 51, 13, 11, 30, 63,  9, 55,
                                     44, 22, 19, 23, 74, 60, 59, 83, 12, 47, 73, 65, 70, 26, 43, 20, 38,
                                      8, 89, 88, 34,  2, 78, 10, 24, 39,  5, 90, 71, 69, 50, 76])

    correct_feature_scores = np.array([  -88.,  -142.,  -530.,   402.,  -128.,  -662.,    22.,   290.,
                                        -444.,  -168.,  -554.,  -162.,  -346.,  -152.,   228.,   288.,
                                          58.,    30.,   434.,  -268.,  -418.,    98.,  -218.,  -286.,
                                        -580.,   208.,  -402.,   112.,   542.,   154.,  -162.,   -30.,
                                         -58.,   698.,  -458.,   140.,   182.,   116.,  -430.,  -598.,
                                         -78.,   284.,   142.,  -404.,  -194.,   796.,    78.,  -350.,
                                         282.,   708., -1060.,  -150.,   130.,  -148.,  -138.,  -180.,
                                         382.,   590.,   558.,  -312.,  -298.,    54.,   376.,  -164.,
                                         252.,  -380.,   184.,  -140.,    78., -1040.,  -386.,  -782.,
                                          -8.,  -354.,  -292.,   428., -1312.,    90.,  -544.,   678.,
                                          72.,   -24.,   288.,  -334.,   378.,  -132.,   320.,    34.,
                                        -444.,  -444.,  -664.,  -118.,  2896.,  1850.,  3746.,  1100.,
                                        3130.,  1158.,  3624.,  2080.])

    assert np.all(np.equal(fs.top_features, correct_top_features))
    assert np.all(np.equal(fs.feature_scores, correct_feature_scores))

def test_transform():
    """Make sure ReliefF transforms correctly"""
    data = pd.read_csv('data/GAMETES-test.csv.gz')
    X_train, X_test, y_train, y_test = train_test_split(data.drop('class', axis=1).values,
                                                        data['class'].values,
                                                        random_state=34895)

    fs = ReliefF(n_neighbors=100, n_features_to_keep=5)
    fs.fit(X_train, y_train)
    X_test = fs.transform(X_test)

    assert np.all(np.equal(X_test[0], np.array([0, 1, 1, 1, 1])))
    assert np.all(np.equal(X_test[1], np.array([2, 1, 0, 1, 1])))
    assert np.all(np.equal(X_test[-2], np.array([1, 1, 0, 1, 0])))
    assert np.all(np.equal(X_test[-1], np.array([1, 0, 1, 0, 0])))

def test_fit_transform():
    """Make sure ReliefF fit_transforms correctly"""
    data = pd.read_csv('data/GAMETES-test.csv.gz')
    X_train, X_test, y_train, y_test = train_test_split(data.drop('class', axis=1).values,
                                                        data['class'].values,
                                                        random_state=34895)

    fs = ReliefF(n_neighbors=100, n_features_to_keep=5)
    X_train = fs.fit_transform(X_train, y_train)

    assert np.all(np.equal(X_train[0], np.array([1, 1, 0, 2, 1])))
    assert np.all(np.equal(X_train[1], np.array([0, 0, 0, 2, 0])))
    assert np.all(np.equal(X_train[-2], np.array([1, 1, 0, 1, 0])))
    assert np.all(np.equal(X_train[-1], np.array([0, 0, 0, 0, 0])))
