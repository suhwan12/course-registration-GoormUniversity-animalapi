import io
from torchvision import models
import json
from flask import Flask, request
from flask import make_response
import torchvision.transforms as transforms
from PIL import Image

app = Flask(__name__)

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)
    
model = models.densenet121(pretrained=True)

model.eval()

imagenet_class_index = json.load(open('imagenet_class_index.json'))

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    
    return imagenet_class_index[predicted_idx]

@app.route('/', methods=['GET'])
def hell():
    if request.method == 'GET':
        print("GET request received")
        return "Hell World!"

@app.route('/mlapp/app', methods=['GET'])
def hello():
    if request.method == 'GET':
        print("GET request received")
        return "Hello World!"

@app.route('/mlapp/mlapp', methods=['POST'])
def predict():
    if request.method == 'POST':
        print("POST request received")
        file = request.files['image']
        img_bytes = file.read()
        
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        
        res = {
            'class_id' : class_id,
            'class_name' : class_name
        }
        res = make_response(json.dumps(res, ensure_ascii=False))
        res.headers['Content-Type'] = 'application/json'
        
        return res
    
if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)