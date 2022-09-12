from flask import Blueprint, request

from key.file_path import USER_CLOTHES_DIR

clothes = Blueprint('clothes', __name__, url_prefix='/clothes')


@clothes.route('/list', methods=['GET'])
def get_clothes_list():
    from model import MyClothes

    user_id = request.args['user_id']

    user_clothes = MyClothes.query.filter(MyClothes.user_id == user_id and MyClothes.is_user_img == 1)
    recommend_clothes = MyClothes.query.filter(MyClothes.user_id == user_id and MyClothes.is_user_img == 0)

    return {'user_id': user_id,
            'user_clothes': [i.as_dict() for i in user_clothes],
            'recommend_clothes': [i.as_dict() for i in recommend_clothes]}


@clothes.route('/upload', methods=['POST'])
def upload_user_clothes():
    import os

    if request.method == 'POST':
        user_id = request.values['user_id']
        file = request.files['file']
        print(file)

        if len(file.filename) == 0:
            return {'message': 'No File Uploaded!'}, 400

        os.makedirs(USER_CLOTHES_DIR, exist_ok=True)
        filename = user_id + file.filename.split('.')[0] + '.jpg'
        file.save(os.path.join(USER_CLOTHES_DIR, filename))

        ########## openpose, humanparsing ##########
        # import sys
        # sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

        from openpose import run
        # run.get_keypoints(os.path.join(USER_CLOTHES_DIR, filename))
        run.get_keypoints('/data/seeot-model/02_4_full.jpg')

        return {'message': 'Image Uploaded!',
                'user_id': user_id,
                'file_path': USER_CLOTHES_DIR + '/' + filename}
