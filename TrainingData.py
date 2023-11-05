# Importing Required Packages
import projectmodules as pm


directory=r'.\Dataset'
train_file=r'.\Recognizer\Trained_data.yml'
faces,faceid=pm.training_data(directory)  # Training Images and getting faces co-ordinates along with id
recognizer=pm.train_classifier(faces,faceid)  # Training classifier
recognizer.save(train_file)  # saving the trained file