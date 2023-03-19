import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, f1_score, precision_score, \
    recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree


# the constants we are using and tuning in this project
MODE = 2
LOWER = 5
UPPER = 101
STEP = 4


def load_data(n):
    """
    Load the data according to the mode <n>, split the data randomly into
    training 60%, validation 20%, and testing 20%. The data is the one stored in
    "out.csv" file. It prints the sizes of the training data and the counts of
    the response variable in the whole dataset

    :param
    n: the mode of target class, with:
    1 being nothate (0) vs racism (1);
    2 being nothate (0) vs hate (1)
    3 being hate (0) vs racism (1)
    4 being nothate (0) vs hate|racism (1)
    where nothate indicates a normal speech, hate indicates a normal hate speech
    that is not a racism speech and racism indicates a hate speech that is
    racist.

    :return:
    X_train: training predictors, a sparse matrix with columns as indicator of
    each word and each row as a training example.
    X_val: validation predictors, same as above
    X_test: testing predictors, same as above
    y_train: training targets, a vector storing the target of each corresponding
    row
    y_val: validation targets, same as above
    v_test: testing targets, same as above
    v: vectorizer for the sparse matrix
    response: the binary response according to the mode n, with response[0]
    being indicator of (0) and response[1] being indicator of (1)
    """
    df = pd.read_csv("out.csv")
    if n == 1:
        df = df[(df['hate'] == 'nothate') | (df['hate'] == 'racism')]
        label = df['hate'].values[:-1].tolist()
        y = np.array([1 if i == 'racism' else 0 for i in label])
        response = 'nothate', 'racism'
    elif n == 2:
        df = df[(df['hate'] == 'nothate') | (df['hate'] == 'hate')]
        label = df['hate'].values[:-1].tolist()
        y = np.array([0 if i == 'nothate' else 1 for i in label])
        response = 'nothate', 'hate'
    elif n == 3:
        df = df[(df['hate'] == 'hate') | (df['hate'] == 'racism')]
        label = df['hate'].values[:-1].tolist()
        y = np.array([0 if i == 'hate' else 1 for i in label])
        response = 'hate', 'racism'
    else:
        label = df['hate'].values[:-1].tolist()
        y = np.array([0 if i == 'nothate' else 1 for i in label])
        response = 'nothate', 'hate or racism'
    corpus = df['dalits are lowlives'].values[:-1].tolist()
    v = CountVectorizer()
    X = v.fit_transform(corpus)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=5213)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,
                                                      test_size=0.25,
                                                      random_state=5213)
    print(X_train.shape)
    print(df['hate'].value_counts())
    print('\n')
    return X_train, X_val, X_test, y_train, y_val, y_test, v, response


# the datasets
X_train, X_val, X_test, y_train, y_val, y_test, vectorizer, response = \
    load_data(MODE)


def classify(max_depth, criterion):
    """
    trains a DecisionTreeClassifier on the dataset and evaluates the classifier
    using the validation data.

    :param max_depth: the max_depth hyperparameter of the classifier
    :param criterion: the criterion hyperparameter of the classifier

    :return:
    accuracy: accuracy of the classifier
    precision: the precision of the classifier
    recall: the recall of the classifier
    f1: the f1 score of the classifier
    """
    clf = DecisionTreeClassifier(max_depth=max_depth, criterion=criterion)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred)
    recall = recall_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred)
    return accuracy, precision, recall, f1


def select_model():
    """
    This function is the most important on in our data project, it is also a
    powerful one. This function first trains the data on the max_depths pre-
    specified by LOWER, UPPER, and STEP, for each criterion: "log_loss", "gini",
    "entropy". It then evaluates the classifier on the validation data and plots
    the four evaluation metrics of the classifiers of each criterion against max
    depth of the classifier in four different plots. And it also reports the
    four metrics in the terminal.
    """

    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    for s in ["log_loss", "gini", "entropy"]:
        markers = ['s', 'o', '^']
        accuracy = []
        precision = []
        recall = []
        f1 = []
        indices = np.arange(LOWER, UPPER, STEP)
        for i, k in enumerate(indices):
            results = classify(k, s)
            accuracy.append(results[0])
            precision.append(results[1])
            recall.append(results[2])
            f1.append(results[3])
            print("criterion " + s + " with max depth " + str(k) + ":")
            print("accuracy: " + str(round(results[0], 3)))
            print("precision: " + str(round(results[1], 3)))
            print("recall: " + str(round(results[2], 3)))
            print("f1 score: " + str(round(results[3], 3)) + '\n')

        accuracy = np.array(accuracy)
        ax[0, 0].scatter(indices, accuracy,
                         marker=markers[["log_loss", "gini",
                                         "entropy"].index(s)],
                         label=s, alpha=0.7)
        ax[0, 0].set_xlabel("Max depth")
        ax[0, 0].set_ylabel("Accuracy")
        ax[0, 0].set_title("Accuracy")
        legend = ax[0, 0].legend(loc='lower right')
        ax[0, 0].add_artist(legend)

        precision = np.array(precision)
        ax[0, 1].scatter(indices, precision,
                         marker=markers[["log_loss", "gini",
                                         "entropy"].index(s)],
                         label=s, alpha=0.7)
        ax[0, 1].set_xlabel("Max depth")
        ax[0, 1].set_ylabel("Precision")
        ax[0, 1].set_title("Precision")
        legend = ax[0, 1].legend(loc='lower right')
        ax[0, 1].add_artist(legend)

        recall = np.array(recall)
        ax[1, 0].scatter(indices, recall,
                         marker=markers[["log_loss", "gini",
                                         "entropy"].index(s)],
                         label=s, alpha=0.7)
        ax[1, 0].set_xlabel("Max depth")
        ax[1, 0].set_ylabel("recall")
        ax[1, 0].set_title("Recall")
        legend = ax[1, 0].legend(loc='lower right')
        ax[1, 0].add_artist(legend)

        f1 = np.array(f1)
        ax[1, 1].scatter(indices, f1,
                         marker=markers[["log_loss", "gini",
                                         "entropy"].index(s)],
                         label=s, alpha=0.7)
        ax[1, 1].set_xlabel("Max depth")
        ax[1, 1].set_ylabel("f1 score")
        ax[1, 1].set_title("f1 score")
        legend = ax[1, 1].legend(loc='lower right')
        ax[1, 1].add_artist(legend)

    # annotations of the max that is not necessary in this place
    # max_index = indices[np.argmax(ac)]
        # plt.annotate(f'Max: ({str(max_index)}, {round(max(ac),5)})',
        #              xy=(indices[max_index], ac[max_index]),
        #              xytext=(-10, coord_helper(["log_loss", "gini",
        #                                         "entropy"].index(s))),
        #              textcoords='offset points', ha='center', va='top')
    # max_value = 0
    # row_index = 0
    # col_index = 0
    # for k, row in enumerate(acs):
    #     for j, value in enumerate(row):
    #         if value > max_value:
    #             max_value = value
    #             row_index = k
    #             col_index = j
    # print("Highest accuracy: ", max_value)
    # print("Hyperparameters for the highest accuracy:",
    #       ["log_loss", "gini", "entropy"][row_index],
    #       "max depth", col_index + LOWER)

    plt.suptitle("Four evaluation metrics of validation set prediction against "
                 "max depth for three criteria", fontsize=15)
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.show()


def visualization(depth, cri, layer):
    """
    Visualization visualizes the binary tree classifier trained on X-train and
    y-train with <depth>, <cri> as hyperparameters, and <layer> as the number of
    layers to display.

    :param depth: the depth of the classifier
    :param cri: criterion of the classifier
    :param layer: layers we want to display
    """
    my_tree = DecisionTreeClassifier(max_depth=depth, criterion=cri)
    my_tree.fit(X_train, y_train)
    x_path = my_tree.decision_path(X_train)
    first_two_nodes = np.zeros((X_train.shape[0], layer+1), dtype=bool)
    for i, row in enumerate(x_path):
        indices = np.where(row.indices < layer+1)[0]
        first_two_nodes[i, indices] = True
    plot_tree(my_tree, max_depth=layer,
              feature_names=vectorizer.get_feature_names_out(),
              class_names=[response[0], response[1]], filled=True, label="root",
              impurity=True, fontsize=12)
    plt.show()


def entropy(array):
    """
    calculates the shannon entropy of a binary sample, helper for compute_
    information_gain()

    :param array: the sample of a binary variable, usually a column vector
    :return: the entropy of this variable
    """

    y_1s = np.count_nonzero(array == 1)
    y_0s = np.count_nonzero(array == 0)
    y_length = array.shape[0]
    if y_1s == 0 or y_0s == 0:
        raise ValueError("The word exist in full data. But no such word exist "
                         "in training data.")
    else:
        ent = (y_1s / y_length) * math.log2(y_1s / y_length) + \
              (y_0s / y_length) * math.log2(y_0s / y_length)
        return -ent


def compute_information_gain(word):
    """
    compute the information gain on the response if given <word>.

    :param word: the word, a str
    :return: the information gain if we know the value of <word>
    """
    if not (word in vectorizer.get_feature_names_out()):
        return "No such word exist in the data."
    else:
        i = np.where(vectorizer.get_feature_names_out() == word)[0][0]
        try:
            ent_y = entropy(y_train)
        except ValueError as error:
            return str(error)
        x = X_train[:, i]
        indices_x1 = np.where(X_train[:, i].reshape(1, -1).toarray() >= 1)[1]
        indices_x0 = np.where(X_train[:, i].reshape(1, -1).toarray() == 0)[1]
        try:
            ent_y_given_x1 = entropy(y_train[indices_x1])
            ent_y_given_x0 = entropy(y_train[indices_x0])
        except ValueError as error:
            return str(error)
        p_x1 = indices_x1.shape[0] / x.shape[0]
        p_x0 = indices_x0.shape[0] / x.shape[0]
        conditional_entropy = p_x1 * ent_y_given_x1 + p_x0 * ent_y_given_x0
        return ent_y - conditional_entropy


def high_information_words():
    """
    Prints the words in the over 20,000 word datasets that have high information
    gain. The threshold is set to only 0.005 since this is already a high
    information gain in the context of nlp and this dataset.
    """
    for word in vectorizer.get_feature_names_out():
        # print(word, compute_information_gain(word))
        w = compute_information_gain(word)
        if isinstance(w, float) and w > 0.001:
            print(word)


if __name__ == "__main__":
    select_model()
    visualization(40, 'gini', 3)
    high_information_words()
