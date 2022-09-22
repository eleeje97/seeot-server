import os
import shutil


def human_parsing(origin_img_path, output_img_path):
    # copy and put image into inputs/
    shutil.copy(origin_img_path, '/data/seeot-server/models/human_parsing/inputs/image.jpg')

    # run image parsing
    os.system("python models/human_parsing/simple_extractor.py --dataset 'lip' --model-restore 'checkpoints/final.pth' --input-dir 'inputs' --output-dir 'outputs'")

    # copy and put output image into /data/seeot-data/
    if os.path.exists('/data/seeot-server/models/human_parsing/outputs/image.png'):
        shutil.copy('/data/seeot-server/models/human_parsing/outputs/image.png', output_img_path)

        # remove images in inputs/
        os.remove('/data/seeot-server/models/human_parsing/inputs/image.jpg')

        # remove images in outputs/
        os.remove('/data/seeot-server/models/human_parsing/outputs/image.png')
