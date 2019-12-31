## How-to

1. Make sure you have `Docker` and `Docker-compose`.

2. Build and up the image,
```bash
docker-compose -f docker-compose.yml up --build
```

```text
dask_1  | 2019-10-23 15:42:00.453028: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
dask_1  | 2019-10-23 15:42:00.462504: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 1598810000 Hz
dask_1  | 2019-10-23 15:42:00.464081: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x527f320 executing computations on platform Host. Devices:
dask_1  | 2019-10-23 15:42:00.464154: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): <undefined>, <undefined>
```
