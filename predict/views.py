import csv
import json
from django.http import HttpResponse
from sklearn.metrics import confusion_matrix, f1_score
from book.models import Book, BookRate
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np


def write_metrics_to_csv(accuracy, TP, FP, TN, FN, f1_score, csv_filename, param):

    # Create the CSV data
    csv_data = [
        ['Metric', 'Value'],
        ['Tag Name', param],
        ['Subset Accuracy', accuracy],
        ['True Positives (TP)', TP],
        ['False Positives (FP)', FP],
        ['True Negatives (TN)', TN],
        ['False Negatives (FN)', FN],
        ['F1 Score', f1_score]
    ]

    # Define the filename for the CSV file
    csv_filename = "metrics.csv"

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
        csv_filename)

    # Write the CSV data to the response
    csv_writer = csv.writer(response)
    csv_writer.writerows(csv_data)

    return response


def subset_accuracy_with_metrics(y_true, y_pred, params):
    """
    Calculate subset accuracy along with other metrics (TP, FP, TN, FN, F1 Score).

    Parameters:
    y_true : list of lists
        True labels for each sample.
    y_pred : list of lists
        Predicted labels for each sample.

    Returns:
    float
        Subset accuracy.
    float
        True positives (TP).
    float
        False positives (FP).
    float
        True negatives (TN).
    float
        False negatives (FN).
    float
        F1 score.
    """
    # Flatten the true and predicted labels
    y_true_flat = [label for sublist in y_true for label in sublist]
    y_pred_flat = [label for sublist in y_pred for label in sublist]

    # Calculate confusion matrix
    conf_matrix = confusion_matrix(y_true_flat, y_pred_flat)

    # Extract TP, FP, TN, FN
    TP = conf_matrix[1, 1]
    FP = conf_matrix[0, 1]
    TN = conf_matrix[0, 0]
    FN = conf_matrix[1, 0]

    # Calculate F1 score
    f1 = f1_score(y_true_flat, y_pred_flat, average='weighted')

    # Calculate subset accuracy
    accuracy = (TP + TN) / (TP + TN + FP + FN)

    return write_metrics_to_csv(accuracy, TP, FP, TN, FN, f1, "f1_score.csv", params)


def generate_predictions(book):
    # Your logic to generate predictions for the given book
    # For example, you might use a machine learning model to predict ratings and tags
    book_rates = BookRate.objects.filter(
        book=book)
    tags_query = book.tags.values_list(
        'name', flat=True)  # QuerySet of tag names
    # Convert QuerySet to a comma-separated string of tag names
    tags = ','.join(tags_query)
    # Logic to generate predicted rating
    predicted_rating = book_rates.first().rate if book_rates.exists() else 0
    predicted_tags = tags   # Logic to generate predicted tags
    return predicted_rating, predicted_tags


def subset_accuracy(y_true, y_pred):
    """
    Calculate subset accuracy for multi-label classification.

    Parameters:
    y_true : list of lists
        True labels for each sample.
    y_pred : list of lists
        Predicted labels for each sample.

    Returns:
    float
        Subset accuracy score.
    """
    correct_predictions = 0
    total_samples = len(y_true)

    for true_labels, pred_labels in zip(y_true, y_pred):
        if set(true_labels) == set(pred_labels):
            correct_predictions += 1

    accuracy = correct_predictions / total_samples
    return accuracy


def prediction_view(request):
    tag_name = request.GET.get('tag-name')

    # Fetch true ratings, tags, and genres for each book
    book_data = []
    for book in Book.objects.filter(tags__name__icontains=tag_name):
        # Retrieve ratings from BookRate model related to the current book
        ratings = BookRate.objects.filter(
            book=book).values_list('rate', flat=True)
        # Calculate average rating
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        # Retrieve tags associated with the current book
        tags_query = book.tags.values_list(
            'name', flat=True)  # QuerySet of tag names
        # Convert QuerySet to a comma-separated string of tag names
        tags = ','.join(tags_query)
        # Combine the average rating and tags for the current book
        book_data.append((avg_rating, tags))

    # Separate the combined data into true ratings and true tags
    true_ratings = [data for data in book_data]
    true_tags = [data[1] for data in book_data]

    # Convert true tags to lists of lists if not already in that format
    true_tags = [[tag.strip() for tag in tags.split(',')] if tags else []
                 for tags in true_tags]

    # Similarly, obtain predicted ratings and tags from your model
    # Store them in pred_ratings and pred_tags respectively

    # Combine predicted ratings and tags for each book into a list of tuples
    # Fetch books and generate predictions for each book
    pred_data = []
    for book in Book.objects.filter(tags__name__icontains=tag_name):
        # Generate predictions for the current book
        predicted_rating, predicted_tags = generate_predictions(book)
        pred_data.append((predicted_rating, predicted_tags))

    # Separate the combined data into predicted ratings and predicted tags
    pred_ratings = [data for data in pred_data]
    pred_tags = [data[1] for data in pred_data]

    # Convert predicted tags to lists of lists if not already in that format
    pred_tags = [[tag.strip() for tag in tags.split(',')] if tags else []
                 for tags in pred_tags]

    # Calculate subset accuracy
    accuracy = subset_accuracy(
        true_ratings + true_tags, pred_ratings + pred_tags)
    print("Subset accuracy:", accuracy)

    return subset_accuracy_with_metrics(true_ratings + true_tags, pred_ratings +
                                        pred_tags, tag_name)
    # return HttpResponse({"test": "sample"}, content_type="application/json")
