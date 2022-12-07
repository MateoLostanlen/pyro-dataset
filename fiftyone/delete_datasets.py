import glob
import fiftyone as fo

print(fo.list_datasets())

ds_list = fo.list_datasets()
for ds in ds_list:
    print(ds)
    dataset = fo.load_dataset(ds)
    dataset.delete()
print(fo.list_datasets())
