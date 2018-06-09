
from scipy.ndimage.filters import gaussian_filter
from datasets.ISIC2018 import *
from models import backbone
from misc_utils.visualization_utils import BatchVisualization
from misc_utils.eval_utils import compute_jaccard
from skimage.morphology import label as sk_label

if __name__ == '__main__':
    backbone_name = 'vgg16'
    k_fold = 0
    version = '0'

    model_name = 'task2_%s' % backbone_name
    run_name = 'task2_%s_k%d_v%s' % (backbone_name, k_fold, version)

    _, (x, y_true), _ = load_training_data(task_idx=2, output_size=224)

    if len(y_true.shape) == 3:
        y_true = y_true[..., None]

    if y_true[0].max() > 1:
        y_true = (y_true > 127.5).astype(np.uint8)

    model = backbone(backbone_name).segmentation_model(load_from=run_name)

    # max_num_images = 32
    max_num_images = x.shape[0]
    x = x[:max_num_images]
    y_true = y_true[:max_num_images]

    y_pred = model.predict(x, batch_size=8)

    scores = model.evaluate(x, y_true, batch_size=32, verbose=1)
    print(scores)

    bv = BatchVisualization(images=x,
                            true_masks=y_true,
                            pred_masks=y_pred)
    bv()

