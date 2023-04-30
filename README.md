# ecg_pytorch

### pytorch

[GitHub - yiyiis/ecg_pytorch](https://github.com/yiyiis/ecg_pytorch)

- 参数与原版相同不做修改
- 需要注意的是pytorch的padding和keras的padding不同，keras的padding默认是对两头进行padding，而pytorch则是向后补，所以为了解决卷积后维度不变，我向前padding了7，向后padding了8，如果不做这一步acc将会下降大约10%。



### keras

[GitHub - awni/ecg: Cardiologist-level arrhythmia detection and classification in ambulatory electrocardiograms using a deep neural network](https://github.com/awni/ecg)

