import os
import glob
import yaml
import shutil
from datetime import datetime


def main(args):

    print(args)

    if not args.dry:
        if os.path.isdir(args.dataset):
            shutil.rmtree(args.dataset)

    datasets = glob.glob("Data/Datasets/**/**/images")
    datasets.sort()

    with open(args.config) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    ds_size = {}
    for dataset in datasets:
        _, _, source, name, _ = os.path.normpath(dataset).split(os.sep)
        ds_name = dataset.split("Datasets/")[1].split("/images")[0].replace("/", "_")
        subsets = config[source][name]["subset"]
        if subsets is None:
            imgs = glob.glob(dataset + "/*")
            imgs.sort()
            if "dt" in config[source][name].keys():
                prev_cam = ""
                prev_date = datetime.now()
                files = []
                dt = config[source][name]["dt"] * 60
                for file in imgs:
                    cam, date_str = os.path.basename(file).split("2023")
                    date = datetime.strptime("2023" + date_str.split('.jpg')[0], "%Y_%m_%dT%H_%M_%S")
                    if cam!=prev_cam or abs((date - prev_date).total_seconds()) > dt:
                        files.append(file)
                        prev_cam = cam
                        prev_date = date
                imgs = files
            else:
                ratio = config[source][name]["ratio"]
                if ratio == 0:
                    continue
                imgs = imgs[:: int(1 / ratio)]
        else:
            if not isinstance(subsets, list):
                subsets = [subsets]
                ratios = [config[source][name]["ratio"]]
            else:
                ratios = config[source][name]["ratio"]

            imgs = []
            for subset, ratio in zip(subsets, ratios):
                if ratio == 0:
                    continue
                subset_file = os.path.join(dataset.replace("images", "subset"), subset)
                with open(subset_file) as f:
                    lines = f.read()
                lines = [l for l in lines.split("\n") if len(l) > 0]
                sub_imgs = [
                    os.path.join(dataset, file.replace(".txt", ".jpg"))
                    for file in lines
                ]
                imgs += sub_imgs[:: int(1 / ratio)]

        ds_size[ds_name] = {}
        ds_size[ds_name]["images"] = len(imgs)
        nb_smoke = 0
        for i, img_file in enumerate(imgs):
            base_file = os.path.split(img_file)[1]
            train_val = "train" if i < len(imgs) * args.train_val_split else "val"
            if not args.dry:
                new_img = os.path.join(args.dataset, "images", train_val, base_file)
                os.makedirs(os.path.split(new_img)[0], exist_ok=True)
                shutil.copy(img_file, new_img)
            label_file = img_file.replace(
                "images", "labels/" + config[source][name]["label"]
            ).replace(".jpg", ".txt")
            if os.path.isfile(label_file):
                if not args.dry:
                    new_label = os.path.join(
                        args.dataset,
                        "labels",
                        train_val,
                        base_file.replace(".jpg", ".txt"),
                    )
                    os.makedirs(os.path.split(new_label)[0], exist_ok=True)
                    shutil.copy(label_file, new_label)
                with open(label_file) as f:
                    lines = f.readlines()
                if len(lines):
                    nb_smoke += 1

        ds_size[ds_name]["smoke"] = nb_smoke
        ds_size[ds_name]["no_smoke"] = len(imgs) - nb_smoke

    nb_images, nb_smoke, nb_no_smoke = 0, 0, 0
    for k in ds_size.keys():
        print(k, ds_size[k])
        nb_images += ds_size[k]["images"]
        nb_smoke += ds_size[k]["smoke"]
        nb_no_smoke += ds_size[k]["no_smoke"]

    print(
        "nb_images :",
        nb_images,
        "nb_smoke :",
        nb_smoke,
        "nb_no_smoke :",
        nb_no_smoke,
        "background ratio :",
        round(nb_no_smoke / nb_images, 2),
    )


def get_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="Pyronear Dataset Maker",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--dataset", type=str, default="Data/DS", help="path to dataset to create"
    )
    parser.add_argument(
        "--config", type=str, default="dataset_config.yaml", help="path to config file"
    )
    parser.add_argument(
        "--dry", action="store_true", help="Dray run to simulate ds split"
    )
    parser.add_argument(
        "--train-val-split", type=float, default=0.8, help="Train / Val split ratio"
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args)
