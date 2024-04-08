Sagemaker install

- Install poetry via pip
- poetry add
- gdal will fail
- conda install -c conda-forge gdal
- poetry build
- pip install/dist/eis_wheelnamehere.whl

# must install
- https://medium.com/decathlondigital/making-jupyter-kernels-remanent-in-aws-sagemaker-a130bc47eab7
- python -m ipykernel install --user --name your_kernel_name --display-name your_kernel_display_name