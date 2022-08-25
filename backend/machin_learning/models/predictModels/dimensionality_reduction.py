# 三种数据降维(Dimensionality Reduction)的方法：
# Principal Component Analysis (PCA)
# Kernel PCA
# Linear Discriminant Analysis (LDA)

# Importing the libraries
from matplotlib.colors import ListedColormap
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import explained_variance_score

# Importing the dataset
dataset = pd.read_csv('Absenteeism_at_work_new.csv')
X = dataset.iloc[:, :-2].values#记得去掉[-2]的缺勤时间！！！！
y = dataset.iloc[:, -1].values

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# 三种数据降维方法的对比
def do_dimensionality_reduction(mode, X_train, X_test, y_train):
    # Applying PCA
    if mode == 'PCA':
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        #pca = PCA()
        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)
        ratio = pca.explained_variance_ratio_
        print("explained_variance_ratio: ", ratio)
    # Applying Kernel PCA
    if mode == 'Kernel_PCA':
        from sklearn.decomposition import KernelPCA
        kpca = KernelPCA(n_components=2, kernel='rbf')
        X_train = kpca.fit_transform(X_train)
        X_test = kpca.transform(X_test)
# Applying LDA
    if mode == 'LDA':
        from sklearn.discriminant_analysis \
            import LinearDiscriminantAnalysis as LDA
        #n_components for LDA cannot be larger than min(n_features, n_classes - 1).
        lda = LDA(n_components=2)
        X_train = lda.fit_transform(X_train, y_train)
        X_test = lda.transform(X_test)
        ratio = lda.explained_variance_ratio_
        print("explained_variance_ratio: ", ratio)
    return (X_train, X_test, y_train)

print('X_train:\n',X_train[0],len(X_train[0]))
X_train, X_test, y_train = do_dimensionality_reduction('PCA', X_train, X_test, y_train)
print('X_train(after):\n',X_train[0],len(X_train[0]))

# Training the Logistic Regression model on the Training set
classifier = LogisticRegression(random_state=1)
classifier.fit(X_train, y_train)

# Making the Confusion Matrix
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(accuracy_score(y_test, y_pred))




#隐藏掉画图设定颜色时的warning
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')
#画图
plt.figure()
# Visualising the Training set results
plt.subplot(1,2,1)
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start=X_set[:, 0].min() - 1,
                               stop=X_set[:, 0].max() + 1, step=0.01),
                     np.arange(start=X_set[:, 1].min() - 1,
                               stop=X_set[:, 1].max() + 1, step=0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T)
             .reshape(X1.shape), alpha=0.75,
             cmap=ListedColormap(('red', 'green', 'blue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c=ListedColormap(('red', 'green', 'blue'))(i), label=j)
plt.title('Dimensionality Reduction (Training set)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()

# Visualising the Test set results
plt.subplot(1,2,2)
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start=X_set[:, 0].min() - 1,
                               stop=X_set[:, 0].max() + 1, step=0.01),
                     np.arange(start=X_set[:, 1].min() - 1,
                               stop=X_set[:, 1].max() + 1, step=0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T)
             .reshape(X1.shape), alpha=0.75,
             cmap=ListedColormap(('red', 'green', 'blue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c=ListedColormap(('red', 'green', 'blue'))(i), label=j)
plt.title('Dimensionality Reduction (Test set)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()
