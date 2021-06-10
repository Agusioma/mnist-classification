# mnist-classification
A primer on Classification using the MNIST dataset
This is a project undertaken from the book **Hands-On Machine Learning with Scikit-Learn & TensorFlow CONCEPTS, TOOLS, AND TECHNIQUES TO BUILD INTELLIGENT SYSTEMS** by **Aurélien Géron**.

![book-cover](https://github.com/Agusioma/house-price-prediction/blob/main/book-cover.png)

It uses the MNIST dataset which consists of 70,000 handwritten digits(0-9).
The dataset helps us kickstart classification of handwritten digits.

In this project, we try to predict an imag using the pixel values provide for instance we used the image 5.

### Methods and Technologies used
Python language and its libraries such as Numpy, Pandas, Matplotlib and mainly Scikit-Learn were deployed.


Two classification methods were tested at first:
- Stochastic Gradient Descent
- Random Forest
- K-Nearest Neighbours(Multioutput classification)

For multilabel classification,`OneVsRest` Classifier was based on the Stochastic Gradient Classifier was used.

Performance analysis was done by the aid of:
- The Confusion matrix
- ROC Curve
- Precision/Recall

The confusion matrix was also used in error analysis.

  > The code will be improved time to time and OOP will be used. You can also uncomment relevant lines.Please use the Google Colab environment.
