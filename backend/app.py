from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import cv2 as cv
import os
import time
from datetime import timedelta
from flask_cors import CORS
# from controller.img_process import do_sobel
import controller.img_process as img_process

# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}


# 注：这个函数一定要放在app = Flask(__name__)前面，不然就会被当做入口！！！！
def check_if_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/upload', methods=['POST', 'GET'])
def upload_img():
    if request.method == 'POST':
        # r = request.get_json()
        print('request')
        print(request)
        f = request.files['file']

        if not (f and check_if_allowed(f.filename)):
            return jsonify({'error': 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/imgs_plain',
                                   secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)  # 储存的路径
        upload_path_2 = os.path.join(basepath, 'static/imgs_sobel',
                                     secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f_sobel = do_sobel(upload_path, 1)
        f_sobel.save(upload_path_2)

        # 使用Opencv转换一下图片格式和名称
        img = cv.imread(upload_path)
        cv.imwrite(os.path.join(basepath, 'static/imgs_plain', 'test.jpg'), img)

        return render_template('uploadImg_ok.html', userinput=user_input, val1=time.time())

    return render_template('uploadImg.html')


test_imgs = [
    {
        'name': 'test-img',
        'url': '../static/imgs_plain/test.jpg'
    }
]


@app.route('/get-imgs', methods=['GET'])
def get_imgs():
    return jsonify({
        'status': 'success',
        'imgs': test_imgs
    })


@app.route('/post-imgs', methods=['POST', 'GET'])
def post_imgs():
    response_object = {'status': 'success'}
    imgUrl = test_imgs[len(test_imgs) - 1]['url']
    upload_path = ''
    if request.method == 'POST':
        # post_data = request.get_json()
        # test_imgs.append({
        #     # 'name': post_data.get('name'),
        #     # 'url': post_data.get('url'),
        #     'formData': post_data.get('formData'),
        #  })
        # # imgUrl = post_data.get('url')
        f = request.files['file']
        # test_imgs.append(file)
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/imgs_plain',
                                   secure_filename(f.filename))  # 注:没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)  # 储存的路径

        upload_path_2 = os.path.join(basepath, 'static/imgs_sobel', secure_filename(f.filename))
        f_sobel = img_process.do_sobel(upload_path, False)
        cv.imwrite(upload_path_2, f_sobel)  # 不能用.save()!

        upload_path_3 = os.path.join(basepath, 'static/imgs_contours', secure_filename(f.filename))
        f_contours = img_process.do_find_contours(upload_path)
        cv.imwrite(upload_path_3, f_contours)

        imgUrl = upload_path
        response_object['message'] = 'imgs added!'
    else:
        response_object['test_imgs'] = test_imgs
    # return jsonify(response_object, test_imgs)
    return render_template('uploadImg_ok.html', imgUrl=imgUrl, upload_path=upload_path)


# @app.route('/upload', methods=['POST', 'GET'])
# def


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000, debug=True)
