import glob
import fiftyone as fo
import os

# Remove existing
ds_list = fo.list_datasets()
for ds in ds_list:
    dataset = fo.load_dataset(ds)
    dataset.delete()

datasets = glob.glob("Data/Datasets/**/**/images")
datasets.sort()
for dataset in datasets:
    ds_name = dataset.split("Datasets/")[1].split("/images")[0].replace("/", "_")
    imgs = glob.glob(dataset + "/*")
    imgs.sort()
    label_folders = glob.glob(dataset.replace("images", "labels/*"))
    samples = []
    for img_file in imgs:
        _, file = os.path.split(img_file)
        sample = fo.Sample(filepath=img_file)
        for label_folder in label_folders:
            label_name = os.path.normpath(label_folder).split(os.sep)[-1]
            label_file = os.path.join(label_folder, file.replace(".jpg", ".txt"))

            if os.path.isfile(label_file):
                with open(label_file) as f:
                    lines = f.readlines()

                # Convert detections to FiftyOne format
                detections = []

                for line in lines:
                    # Bounding box coordinates should be relative values
                    # in [0, 1] in the following format:
                    # [top-left-x, top-left-y, width, height]
                    if len(line) > 0:
                        bounding_box = [float(li) for li in line.split(" ")[1:5]]
                        bounding_box[0] -= bounding_box[2] / 2
                        bounding_box[1] -= bounding_box[3] / 2

                        detections.append(
                            fo.Detection(label="smoke", bounding_box=bounding_box)
                        )

                # Store detections in a field name of your choice
                sample[label_name] = fo.Detections(detections=detections)

        samples.append(sample)

    dataset = fo.Dataset(ds_name)
    dataset.add_samples(samples)
    dataset.persistent = True

if __name__ == "__main__":
    # Ensures that the App processes are safely launched on Windows
    session = fo.launch_app(dataset)
    session.wait()
