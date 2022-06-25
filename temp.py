import os
import glob

import face_recognition

# imagePaths = [f for f in glob.glob('images/*.jpg')]
KNOWN_FACES_DIR = 'images'
# KNOWN_FACES_DIR = 'images' + '*.jpg'
known_faces = []
known_names = []

for filename in os.listdir(KNOWN_FACES_DIR):
    image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, filename))
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(filename)

# known_image = face_recognition.load_image_file("images/ob.jpg")
#
# known_encoding = face_recognition.face_encodings(known_image)[0]

# my_face_encoding now contains a universal 'encoding' of my facial features
# that can be compared to any other picture of a face!

unknown_image = face_recognition.load_image_file("/Users/nips/Desktop/trump.jpg")
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

# Now we can see the two face encodings are of the same person with `compare_faces`!
results = face_recognition.compare_faces(known_faces, unknown_encoding)
match = None
if True in results:
    match = known_names[results.index(True)]
    print({match})
print(results)


