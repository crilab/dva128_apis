import requests

with open('bananas.jpg', 'rb') as f:
    image = {'image': f}
    r = requests.post('http://localhost:5000/classify?filter=false', files=image)

print(r.text)

