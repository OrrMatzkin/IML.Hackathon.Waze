from sklearn.model_selection import train_test_split, GridSearchCV
import sys
import warnings

from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import plotly.graph_objects as go
from sklearn.neighbors import KNeighborsRegressor

from model_selection import model_selection
from preprocess import *



def cross_validation(estimator, X_train, y_train, k_range):
    param_grid = {'n_neighbors': k_range}
    knn_cv = GridSearchCV(estimator, param_grid,
                          cv=5, scoring='f1_micro').fit(X_train, y_train)
    cv_errors = 1 - knn_cv.cv_results_["mean_test_score"]
    # std = knn_cv.cv_results_["std_test_score"]

    min_ind = np.argmin(np.array(cv_errors))
    selected_k = np.array(k_range)[min_ind]
    selected_error = cv_errors[min_ind]

    return selected_k, selected_error



def generate_pearson_correlation_heatmap(df):
    corr_df = df.corr()
    go.Figure([go.Heatmap(x=df.columns, y=df.columns, z=corr_df, type='heatmap', colorscale='Viridis')]).show(renderer="browser")


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    try:
        geolocator_use = sys.argv[1]
    except IndexError:
        geolocator_use = ''
    np.random.seed(0)
    raw_data = pd.read_csv("waze_data.csv")
    train_data, test_data = train_test_split(raw_data, test_size=.2, random_state=42)
    preprocess_data, preprocess_y = preprocess(train_data, True if geolocator_use == "-g" else False)
    model_selection(preprocess_data, preprocess_y)
    print("done")
