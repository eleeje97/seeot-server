####################################
# MODULE INIT
####################################
from dior import DIOR
dior_model = DIOR()


####################################
# POSE TRANSFER
####################################

### Pose Tranfer 에서는 사람을 지정할 때, garment값을 None값으로 지정한다. ###

# # 베이스 모델
# pid = ("plaid", 0, None)
#
# # 포즈: 지정한 사람의 포즈 데이터를 가져옴
# pose_id = ("plain", 0, None)
#
# # Pose Tranfer
# pimg, gimgs, oimgs, gen_img, pose = dior_model.dress_in_order(dior_model.model, pid, pose_id=pose_id)
# dior_model.plot_img(pimg, gimgs, oimgs, gen_img, pose)


####################################
# TRY ON
####################################
def try_on(base, top, bottom, outer):
    # 베이스 모델: garment를 None으로 지정
    pid = ("plain", base, None)

    # Garment: 지정한 사람에게서 지정한 번호의 garment를 뽑아옴 (ex. ("print", 1, 5)인 경우, print 그룹에서 1번 사람의 top(5)을 뽑아옴)
    # gids에 try-on해볼 garments를 여러개 추가할 수 있음
    gids = []
    if top != -1:
        gids.append(("plain", top, 5))
    if bottom != -1:
        gids.append(("plain", bottom, 5))
    if outer != -1:
        gids.append(("plain", outer, 5))

    # Try-On: order 리스트에 착용할 순서를 garment 번호로 지정함
    # tuck in -> [2,5,1]: hair, top, bottom 순서
    # not tuck in -> [2,1,5]: hair, bottom, top 순서
    pimg, gimgs, oimgs, gen_img, pose = dior_model.dress_in_order(dior_model.model, pid, gids=gids, order=[1, 5, 3])
    dior_model.plot_img(pimg, gimgs, gen_img=gen_img, pose=pose)
