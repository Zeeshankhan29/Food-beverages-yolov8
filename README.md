# Food-beverages-checkout
####  Problem statement
The objective of this project is to create or provide an application that facilitates the complete automatic self-checkout system to identify different varities of fruit and Vegetables


### Language and Libraries

<p>
<a><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen" alt="python"/></a>
<a><img src="https://img.shields.io/badge/yolo-181818?style=for-the-badge&logo=openai&logoColor=white" alt="numpy"/></a>
<a><img src="https://img.shields.io/badge/pytorch-%23EE4C2C.svg?style=for-the-badge&logo=Django&logoColor=white" alt="YOLO"/></a>

</p>




Create virtual Environment by bash command

```
bash init_setup.sh

```


Activate virtual Environment

```
conda activate checkout

```


Run the pipeline by adding the data into directories artifacts\temp\mask (mask data or annotation) and 
artifacts\temp\original (original image)

```
python main.py

```

or Run the dvc pipeline by following commands

```
dvc init
dvc repro

```