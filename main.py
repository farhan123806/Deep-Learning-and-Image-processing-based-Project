import boto3
import boto3.session
import io
from PIL import ImageDraw, ExifTags, ImageColor
import PIL.Image as Image
from IPython.display import display, Image
from collections import defaultdict

import logging
import boto3
from botocore.exceptions import ClientError

import boto3
rekognition = boto3.client('rekognition')

def detect_labels(photo, bucket):
    client = boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10)

    print('Detected labels for ' + photo)
    print()

    label_counts = {}

    for label in response['Labels']:
        name = label['Name']
        count = len(label['Instances'])
        label_counts[name] = count

    print(label_counts)
    peopleCount=int(label_counts['Person'])
    chairCount=int(label_counts['Chair'])
    print('I found ' + str(label_counts['Person']) + ' people.')
    print('I found ' + str(label_counts['Chair']) + ' chairs.')

    if (chairCount - peopleCount <= 0):
        print("All chairs taken.")
    else:
        print((chairCount - peopleCount), "chairs available.")



    for label in response['Labels']:
        print("Label: " + label['Name'])
        print("Confidence: " + str(label['Confidence']))
        print("Instances:")
        for instance in label['Instances']:
            print("  Bounding box")
            print("    Top: " + str(instance['BoundingBox']['Top']))
            print("    Left: " + str(instance['BoundingBox']['Left']))
            print("    Width: " + str(instance['BoundingBox']['Width']))
            print("    Height: " + str(instance['BoundingBox']['Height']))
            print("  Confidence: " + str(instance['Confidence']))
            print()

        print("Parents:")
        for parent in label['Parents']:
            print("   " + parent['Name'])
        print("----------")
        print()
    return len(response['Labels'])


def mainTrain():
    photo = 'FinalTestCase6.jpeg'
    bucket = 'worchesterbucket'
    label_count =detect_labels(photo, bucket)


mainTrain()
