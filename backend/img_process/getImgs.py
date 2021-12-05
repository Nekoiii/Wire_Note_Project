from flask import Flask, jsonify
from flask_cors import CORS


test_imgs = [
    {
        'name': 'test-img----',
        'url': '../static/testImg/test_img_1.jpg'
    }
]

app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/get-imgs', methods=['GET'])
def all_books():
    return jsonify({
        'status': 'success',
        'imgs': test_imgs
    })


if __name__ == '__main__':
    # app.debug = True
    # app.run(host='127.0.0.1', port=5000, debug=True)
    app.run()
