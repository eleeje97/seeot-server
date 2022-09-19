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
        import sys
        sys.path.append('/data/seeot-model')

        from openpose import run
        # run.get_keypoints(os.path.join(USER_CLOTHES_DIR, filename))
        run.get_keypoints('/data/seeot-model/02_4_full.jpg')

        return {'message': 'Image Uploaded!',
                'user_id': user_id,
                'file_path': USER_CLOTHES_DIR + '/' + filename}


@clothes.route('openpose', methods=['GET'])
def openpose():
    from models.openpose import run
    run.get_keypoints('/data/seeot-model/02_4_full.jpg')
    return {'message': 'OPENPOSE SUCCESS!'}

@clothes.route('human_parsing', methods=['GET'])
def human_parsing():
    from models.human_parsing import run
    origin_img_path = '/data/seeot-model/02_4_full.jpg'
    output_img_path = '/data/seeot-model/temp/02_4_full.png'
    run.human_parsing(origin_img_path, output_img_path)
    return {'message': 'HUMAN_PARSING SUCCESS!'}

@clothes.route('/cc', methods=['GET'])
def Classification():
    ### 필요한 모듈 임포트 ###
    from models.efficientnet.run import efficientnet

    # 밖으로 빼고싶은거 (app.py에 적재시 코드 제거 또는 주석)
    from models.efficientnet.load_model import Load_Model
    lm = Load_Model()
    male_model, female_model = lm.set_model()

    ## 받아오는거 : 성별 / 사진이 저장되어있는 경로

    ## 나갈꺼 사진의 계절
#     clothes_path = request.args['clothes_url']
#     gender = request.args["gender"]
    gender = "female"

    ### 옷 분류 모델 실행 ###
    cla = ""
    if gender == "male":
        # male model
        clm = efficientnet(male_model)
#         cla = clm.run(clothes_path)
        cla = clm.run()
    else:
        # female model
        clm = efficientnet(female_model)
#         cla = clm.run(clothes_path)
        cla = clm.run()

    return cla
