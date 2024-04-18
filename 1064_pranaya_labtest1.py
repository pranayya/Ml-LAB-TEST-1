# -*- coding: utf-8 -*-
"""1064_pranaya_labtest1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S6PhRSOcvLfza5r99upFeISv_KTS1hms

LAB TEST 1: Q3
"""

import pandas as pd
import matplotlib.pyplot as plt
col=["class","cap-shape", "cap-surface", "cap-color", "bruises", "odor", "gill-attachment", "gill-spacing", "gill-size", "gill-color", "stalk-shape", "stalk-root", "stalk-surface-above-ring", "stalk-surface-below-ring", "stalk-color-above-ring", "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type", "spore-print-color", "population", "habitat"]
mushroom_df = pd.read_csv("/content/agaricus-lepiota.data",header=None, names=col)

print(mushroom_df.head)

#encoding
from sklearn.preprocessing import LabelEncoder
mushroom_df.dropna(inplace=True)

le = LabelEncoder()
for col in mushroom_df.columns:
   mushroom_df[col] = le.fit_transform(mushroom_df[col])

import seaborn as sns

corr_matrix = mushroom_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.show()

#splitting into test and training sets

from sklearn.model_selection import train_test_split

X = mushroom_df.drop('class', axis=1)
y = mushroom_df["class"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#training the models
from sklearn.metrics import accuracy_score, classification_report, roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

models = {
    'Logistic Regression': LogisticRegression(),
    'Perceptron': Perceptron(),
    'Multi-Layer Perceptron': MLPClassifier(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Support Vector Machine': SVC(),
    'Naive Bayes': GaussianNB()
}

predictions = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    predictions[name] = y_pred

#evaluating model performance

for name, y_pred in predictions.items():
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{name} accuracy: {accuracy:.2f}")

for name, y_pred in predictions.items():
    report = classification_report(y_test, y_pred)
    print(f"{name} classification report:\n{report}\n")

#plt.figure(figsize=(10, 6))
for name, model in models.items():
    if hasattr(model, "predict_proba"):
      y_pred_proba = model.predict_proba(X_test)[:,1]
      fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
      auc = roc_auc_score(y_test, y_pred_proba)
      plt.plot(fpr, tpr, label=f'{name} (AUC = {auc:.2f})')
    #print(f"ROC curve calculated for {name}.\n")

plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves')
plt.legend()
plt.show()

for name, model in models.items():
    #print(f"Evaluating {name}...")
    # Training set evaluation
    train_accuracy = accuracy_score(y_train, model.predict(X_train))
    if hasattr(model, "predict_proba"):
        y_train_pred_proba = model.predict_proba(X_train)[:,1]
        train_auc = roc_auc_score(y_train, y_train_pred_proba)
    else:
        train_auc = None

    # Testing set evaluation
    test_accuracy = accuracy_score(y_test, predictions[name])
    if hasattr(model, "predict_proba"):
        y_test_pred_proba = model.predict_proba(X_test)[:,1]
        test_auc = roc_auc_score(y_test, y_test_pred_proba)
    else:
        test_auc = None

    print(f"Model: {name}")
    print(f"Training Accuracy: {train_accuracy:.2f}")
    print(f"Training AUC: {train_auc:.2f}" if train_auc is not None else "Training AUC: Not applicable")
    print(f"Testing Accuracy: {test_accuracy:.2f}")
    print(f"Testing AUC: {test_auc:.2f}" if test_auc is not None else "Testing AUC: Not applicable")
    print()

"""Based on evaluation metrics, except for Logestic Regression and Naive Bayes where there's slight indication of overfitting, the other models show good generalization performance without significance evidence of overfitting."""

train_accuracy = {}
test_accuracy = {}

for name, model in models.items():
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    train_accuracy[name] = accuracy_score(y_train, train_pred)
    test_accuracy[name] = accuracy_score(y_test, test_pred)

for name in train_accuracy:
    if train_accuracy[name] - test_accuracy[name] > 0.05:
        print(f"{name} is potentially overfitting.")
    else:
        print(f"{name} is not overfitting.")

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Clustering
X_cluster = mushroom_df.drop('class', axis=1)


scaler=StandardScaler()
X_cluster_scaled= scaler.fit_transform(X_cluster)


kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(X_cluster_scaled)


from sklearn.metrics import silhouette_score
silhouette_avg = silhouette_score(X_cluster_scaled, clusters)
print(f"Silhouette Score: {silhouette_avg}")

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_cluster_scaled)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', s=50, alpha=0.5)
plt.title('Clustering Results')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Cluster')
plt.show()