# Hand Segmentation in Third-Person Point of View
## Pretrained Model
Download the pretrained model from [Google Drive](https://drive.google.com/drive/u/1/folders/1q--u3g9XgQ0qH1I6JJfCs3EfTMc3t1IT) and place the model in ```ckpt/egohands-resnet50dilated-ppm_deepsup```
## Quick Start: Running Inference
1. Simple Demo
```bash
python3 run_inference.py --cfg config/egohands-resnet50dilated-ppm_deepsup.yaml --visualise
```
2. To change resolution
```bash
python3 run_inference.py --cfg config/egohands-resnet50dilated-ppm_deepsup.yaml --resolution 720p --visualise
```
