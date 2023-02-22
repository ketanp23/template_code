from flask import Flask, request, Response 
from flask_uploads import UploadSet, IMAGES, configure_uploads
import jsonpickle
import pickle
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Load the pickled data and store it in a global variable
with open('finalized_model.sav', 'rb') as f:
    model = pickle.load(f)


# Configure the app to store uploaded files in the 'uploads' folder
app.config['UPLOADS_DEFAULT_DEST'] = 'vol1'

# Create an UploadSet for handling image uploads
images = UploadSet('images', IMAGES)

# Configure the Flask-Uploads extension
configure_uploads(app, (images,))

filename = ''






@app.route('/api/test', methods=['GET'])
def test():
    # Model code
    response = {'message': 'API hit iimv'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")





@app.route('/api/testmodel', methods=['POST'])
def process_form():
    data = request.form
    data = model.predict([[float(data['testdata'])]])  
    data_str = ", ".join(str(x) for x in data)
    return data_str


@app.route('/api/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'image' not in request.files:
        return 'No file uploaded', 400

    # Save the uploaded file
    filename = images.save(request.files['image'])
    

    # Return the filename of the saved file
    return filename, 200





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)