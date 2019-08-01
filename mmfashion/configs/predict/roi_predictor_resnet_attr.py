import os

# model settings
arch = 'resnet'
class_num = 1000
img_size = (224, 224)
model = dict(
    type='RoIPredictor',
    backbone=dict(type='ResNet'),
    global_pool=dict(
        type='GlobalPooling',
        inplanes=(7, 7),
        pool_plane=(2, 2),
        inter_plane=512 * 7 * 7,
        outplanes=4096),
    roi_pool=dict(
        type='RoIPooling',
        pool_plane=(2, 2),
        inter_plane=512,
        outplanes=4096,
        crop_size=7,
        img_size=img_size,
        num_lms=8),
    concat=dict(
        type='Concat',
        inplanes=2 * 4096,
        inter_plane=4096,
        num_classes=class_num),
    loss=dict(
        type='BCEWithLogitsLoss',
        weight=None,
        size_average=None,
        reduce=None,
        reduction='mean'),
    pretrained='checkpoint/resnet50.pth')

pooling = 'RoI'

# dataset settings
dataset_type = 'Attr_Pred'
data_root = '../data/Attr_Predict'
img_norm = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
data = dict(
    imgs_per_gpu=32,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        img_path=os.path.join(data_root, 'Img'),
        img_file=os.path.join(data_root, 'train.txt'),
        label_file=os.path.join(data_root, 'train_attr.txt'),
        bbox_file=os.path.join(data_root, 'train_bbox.txt'),
        landmark_file=os.path.join(data_root, 'train_landmarks.txt'),
        img_size=img_size),
    test=dict(
        type=dataset_type,
        img_path=os.path.join(data_root, 'Img'),
        img_file=os.path.join(data_root, 'test.txt'),
        label_file=os.path.join(data_root, 'test_attr.txt'),
        bbox_file=os.path.join(data_root, 'test_bbox.txt'),
        landmark_file=os.path.join(data_root, 'test_landmarks.txt'),
        img_size=img_size),
    val=dict(
        type=dataset_type,
        img_path=os.path.join(data_root, 'Img'),
        img_file=os.path.join(data_root, 'val.txt'),
        label_file=os.path.join(data_root, 'val_attr.txt'),
        bbox_file=os.path.join(data_root, 'val_bbox.txt'),
        landmark_file=os.path.join(data_root, 'val_landmarks.txt'),
        img_size=img_size))

# optimizer
optimizer = dict(type='SGD', lr=1e-3, momentum=0.9)
optimizer_config = dict()

# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.1,
    step=[10, 20])

checkpoint_config = dict(interval=1)
log_config = dict(
    interval=10, hooks=[
        dict(type='TextLoggerHook'),
    ])

start_epoch = 0
total_epochs = 40
gpus = dict(train=[0, 1, 2, 3], test=[0, 1, 2, 3])
work_dir = 'checkpoint/Predict/resnet/attr_pred'
print_interval = 20  # interval to print information
save_interval = 5
init_weights_from = 'checkpoint/resnet50.pth'
resume_from = None
checkpoint = 'checkpoint/Predict/resnet/attr_pred/latest.pth'
workflow = [('train', 40)]
dist_params = dict(backend='nccl')
log_level = 'INFO'
