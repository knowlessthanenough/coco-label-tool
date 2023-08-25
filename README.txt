yolov7 takes yolo format data instead of coco format 

以下是一個典型的 YOLOV7 資料集的檔案架構：
dataset/
├── annotations/
│   ├── train.json
│   ├── test.json
│   └── val.json
├── images/
│   ├── train/
│   │    ├── image1.jpg
│   │    ├── image2.jpg
│   │    ├── ...
│   │    └── imageN.jpg
│   ├── test/
│   │    ├── image1.jpg
│   │    ├── image2.jpg
│   │    ├── ...
│   │    └── imageN.jpg
│   └── val/
│        ├── image1.jpg
│        ├── image2.jpg
│        ├── ...
│        └── imageN.jpg
├── labels/
│   ├── train/
│   │    ├── image1.txt
│   │    ├── image2.txt
│   │    ├── ...
│   │    └── imageN.txt
│   ├── test/
│   │    ├── image1.txt
│   │    ├── image2.txt
│   │    ├── ...
│   │    └── imageN.txt
│   └── val/
│        ├── image1.txt
│        ├── image2.txt
│        ├── ...
│        └── imageN.txt
├── train.txt
├── test.txt
└── val.txt

在這個檔案架構中，dataset 是資料集的根目錄，包含以下幾個子目錄和檔案：
annotation 目錄: jeston file 包含所有要被處理的圖片影像資料，例如 大小, Bbox 位置等等。(gen by label studio(coco))
	need to remove the path left only the image nam

images 目錄：包含所有要被處理的圖片影像檔案，例如 image1.jpg，image2.jpg 等等。

labels 目錄：包含每張圖片對應的標註檔案，檔名與圖片檔案名稱一致，但是副檔名為 .txt。標註檔案中包含了對應圖片中所有物件的類別、邊界框位置等資訊(gen by label studio(yolo))

train.txt：一個純文字檔案，列出了所有用於訓練的圖片檔案路徑，每一行一個路徑，例如：
	images/tain/image1.jpg
	images/train/image2.jpg
	(注意: 批量修改\成你的路徑,遷移後需要重新改變路徑
	cmd 使用 python3 create_image_name_txt.py the/folder/path 生成
	會保存在相同的路徑)

test.txt：一個純文字檔案，列出了所有用於訓練的圖片檔案路徑，每一行一個路徑，例如：
	images/test/image1.jpg
	(注意: 批量修改\成你的路徑,遷移後需要重新改變路徑
	cmd 使用 python3 create_image_name_txt.py the/folder/path 生成
	會保存在相同的路徑)

val.txt：一個純文字檔案，列出了所有用於訓練的圖片檔案路徑，每一行一個路徑，例如：
	images/val/image1.jpg
	images/val/image2.jpg
	(注意:批量修改\成你的路徑,遷移後需要重新改變路徑
	cmd 使用 python3 create_image_name_txt.py the/folder/path 生成
	會保存在相同的路徑)
...

除此之外，還需要在訓練data 檔案夾裏面add一個yaml檔案，裏面包含train.txt, test.txt, val.txt path, numbers of classes, class name
可以參考 /yolov7/data/coco.yaml
還需要在訓練cfg/traing 檔案夾裏面add一個yaml檔案
可以參考 /yolov7/cfg/training/yolov7.yaml

如需結合兩個Json檔案可以使用python3 combine_coco.py 1.json 2.json 
輸出merged_annotations.json會保存在第一個json相同的路徑
(注意: 這只是合併兩個coco輸出的json檔案，其他資料如img, label仍需手動搬遷)

刪除重複圖像運行 : python3 remove_duplicate.py filename.json

檢查是否有任何剩餘的重複圖像運行: python3 check_repeat.py filename.json

更改標籤運行: python3 change_coco_data_class.py path/to/dataset(e.g:F:\c1-1-relabel)
Enter the class mapping as space-separated key-value pairs, e.g. "1:2 2:0 3:1":
5:1 4:1 3:0 2:0 1:2 0:1

*remember to change the categories by hand
        {
            "id": 0,
            "name": "stand"
        },
        {
            "id": 1,
            "name": "swim"
        },
        {
            "id": 2,
            "name": "warning"
        }

python3 combine_datasets.py dataset1 dataset2 path/to/place/the/ouytput