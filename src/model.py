from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


def train_model(data):

    X = data[['Hour', 'Voltage', 'Global_intensity', 'Random_noise']]
    y = data['Global_active_power']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    lr = Ridge(alpha=20)

    dt = DecisionTreeRegressor(
        max_depth=4,
        min_samples_leaf=10,
        random_state=42
    )

    rf = RandomForestRegressor(
        n_estimators=40,
        max_depth=5,
        min_samples_leaf=8,
        random_state=42
    )

    lr.fit(X_train, y_train)
    dt.fit(X_train, y_train)
    rf.fit(X_train, y_train)

    return lr, dt, rf, X_test, y_test