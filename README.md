![PyroNear Logo](docs/source/_static/images/logo.png)

<p align="center">
    <a href="LICENSE" alt="License">
        <img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" /></a>
</p>




# Pyrodataset: Create wildfire dataset

This repository aims to gather our work on dataset creation

The main objectives are the following

- Gather the datasets we have created / collected
- Gather several annotations for these datasets, the annotation of a smoke cloud is very complex and can answer several types of strategies.
- Visualize datasets and their annotations using fiftyone
- Create new datasets by combining available ones
- Benchmark our models on these datasets.

The annotations here are annotations for object detection, so we can evaluate models in classification and object detection


This repository use [dvc](https://dvc.org/) to store data. To fully use this repository you need access to our dvc storage which is currently reserved for Pyronear members. We hope to make it public soon. However you can access all public data listed below


## Setup

First clone the repo and install requirements
```shell
git clone https://github.com/pyronear/pyro-dataset.git
cd pyro-dataset
pip install -r requirements.txt
```

Then pull the data using dvc

```shell
dvc pull
```

## Visualize datasets using fiftyone

Fiftyone is an open-source tool to build and visualize datasets, please refer here for more information.

To load datasets, run

```shell
python fiftyone/create_datasets.py
```

then go to http://localhost:5151, to use their app


Once datasets are created in fiftyone, you can re-lunch the app using

```shell
python fiftyone/run.py
```

You can add a new dataset using:

```shell
python fiftyone/add_dataset.py
```

## Create a dataset

You can create a combination of available datasets using 

```shell
python datasets/make_dataset.py
```

this combination is defined by the configuration file dataset_config.yaml

You can preview the combination with the dry option

```shell
python datasets/make_dataset.py --dry
```



## Datasets

### Sources of Data

Today we have identified 3 main data sources, two of which are publicly available (Wildfire Alert & HPWREN):

#### Alerte wildfire

[ALERTWildfire](https://www.alertwildfire.org/) is a consortium of three universities -- The University of Nevada, Reno (UNR), University of California San Diego (UCSD), and the University of Oregon (UO) -- providing access to state-of-the-art Pan-Tilt-Zoom (PTZ) fire cameras and associated tools to help firefighters and first responders


#### HPWREN:


The High Performance Wireless Research and Education Network [HPWREN](https://hpwren.ucsd.edu/cameras/) is a network research program, funded by the National Science Foundation. The program includes the creation, demonstration, and evaluation of a non-commercial, prototype, high-performance, wide-area, wireless network in its Southern California service area. 


#### PYRONEAR

Our camera network is in development which allows us to start building an image database. This database does not contain any fire images for the moment, but it does contain a large number of false positive cases, which are quite challenging for a network.

Pyronear has the ambition to become one day a public data source as important as the two presented above.

#### UNKNOWN

In addition to these 3 sources, we gather under the name UNKNOWN all other sources of images coming from the internet without a properly defined source or in too small quantity. Among these images we find those of [Center for Wildfire Research of University of Split, Croatia](http://wildfire.fesb.hr/index.php?option=com_content&view=article&id=49&Itemid=54)


### Datasets

From these data sources we have created or collected several datasets:

#### Alerte wildfire

A dataset was created from the [Nevada Seismological Laboratory YouTube channel](https://www.youtube.com/user/nvseismolab) by Rodrigue de Schaetzen, Raphael Chang Menoni, Yifu Chen, and Drijon Hasani of the University of British Columbia, Canada their research paper detailing their work is available [here](https://rdesc.dev/project_x_final.pdf?utm_source=pocket_mylist)

They have semi-automatically labeled (by video interpolation) 1.3M frames, you can download the whole dataset [here](https://archive.org/details/smokenet-projectx?utm_source=pocket_mylist). The code of their experimentation is available [here](https://github.com/Project-X-UBC/smoke-detection-net) and allows to extract a subset of 56K frames.

We added to this repository an extract of this 56K frames set, we took only 2807 frames of this subset.


| HPWREN               | Size   | Smoke Images| Non Smoke Images |
| :---:                | :--:   |:---:        |       :---:      |
| Nvseismolab_set1     | 2807   | 1375        | 1432             |



#### HPWREN

5 datasets have been created by [AiforMankind](https://github.com/aiformankind):

Two training datasets were created during two hackathons, we name here these datasets AiForManKind_v1 ([hackaton 1](https://github.com/aiformankind/wildfire-smoke-detection-camera)) and AiForManKind_v2 ([hackaton 2](https://github.com/aiformankind/wildfire-smoke-dataset)).

To test the performance of their models on challenging false positive examples, Ai for mankind also proposes 3 small datasets each containing one of the main error sources in automated forest fire detection. We called these datasets AiForManKind_sunrise, AiForManKind_fog and AiForManKind_clouds.


A dataset is also proposed by the [fuego project](https://github.com/fuego-dev/firecam)


| HPWREN               | Size   | Smoke Images| Non Smoke Images |
| :---:                | :--:   |:---:        |       :---:      |
| Fuego                | 1739   | 1739        | 0                |
| AiForManKind_v1      | 744    | 744         | 0                |
| AiForManKind_v2      | 2191   | 2191        | 0                |
| AiForManKind_cloud   | 1080   | 0           | 0                |
| AiForManKind_sunrise | 180    | 0           | 0                |
| AiForManKind_fog     | 180    | 0           | 0                |


#### PYRONEAR

Pyronear starts to deploy its network of cameras, which allows us to create new datasets. We propose here two datasets ardeche_set0 and gironde_set0 named after the french regions where the cameras are located. These datasets do not contain any smoke images but many potential false positives which are quite challenging.

| PYRONEAR     | Size   | Smoke Images| Non Smoke Images |
| :---:        | :--:   |:---:        |       :---:      |
| ardeche_set0 | 20587  | 0           | 20587            |
| gironde_set0 | 1205   | 0           | 1205             |

#### UNKOWN

We propose here two datasets from a mix of images collected on internet, fog_clouds to evaluate a model on challenging non-smoke images and smoke to test the hability of a model to detect a wildfire


| UNKOWN     | Size | Smoke Images| Non Smoke Images |
| :---:      | :--: |:---:        |       :---:      |
| fog_clouds | 453  | 0           | 453              |
| smoke      | 333  | 333         | 0                |



## What else

## Citation

If you wish to cite this project, feel free to use this [BibTeX](http://www.bibtex.org/) reference:

```bibtex
@misc{pyrodataset2019,
    title={Pyrodataset: wildfire early detection},
    author={Pyronear contributors},
    year={2019},
    month={October},
    publisher = {GitHub},
    howpublished = {\url{https://github.com/pyronear/pyro-dataset}}
}
```


## Contributing

Please refer to [`CONTRIBUTING`](CONTRIBUTING.md) to help grow this project!



## License

Distributed under the Apache 2 License. See [`LICENSE`](LICENSE) for more information.
