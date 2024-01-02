def getBestModel(X_train, X_test, y_train, y_test, column_transformer):
    from tqdm import tqdm
    from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor, AdaBoostRegressor
    from xgboost import XGBRegressor
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
    from sklearn.svm import LinearSVR, SVR, NuSVR
    from sklearn.pipeline import make_pipeline
    import pandas as pd
    from sklearn.metrics import r2_score
    train_score = []
    r2_scores = []
    models_new = []

    models = [
        RandomForestRegressor(),
        ExtraTreesRegressor(), 
        GradientBoostingRegressor(), 
        AdaBoostRegressor(), 
        XGBRegressor(),
        LinearRegression(),
        LinearSVR(),
        SVR(),
        NuSVR(),
        Ridge(),
        Lasso(),
        ElasticNet()
    ]

    # Use tqdm to create a progress bar for the loop
    for model in tqdm(models, desc="Fitting Models", unit="model"):
        pipe = make_pipeline(column_transformer, model)
        pipe.fit(X_train, y_train)
        train_score.append(pipe.score(X_train, y_train))
        y_pred = pipe.predict(X_test)
        r2_scores.append(r2_score(y_test, y_pred))
        models_new.append(model.__class__.__name__)

    df = pd.DataFrame({
        'model': models_new,
        'train score': train_score,
        'r2 score': r2_scores
    })

    return df.sort_values('r2 score', ascending=False)



def getBestState(X, y, test_size, column_transformer):
    from sklearn.model_selection import train_test_split
    from modelprocessing.functions import getBestModel
    import numpy as np
    from tqdm import tqdm
    beststate = []

    for i in tqdm(range(10), desc='getting best state', unit='state'):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=i)
        beststate.append(getBestModel(X_train, X_test, y_train, y_test, column_transformer).at[0, 'r2 score'])
    
    return np.argmax(beststate)


