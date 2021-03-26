# simple-AI-captcha-analyze
基于机器学习识别验证码，仅在`macos`下运行通过，理论上`Linux`也可用。但由于使用了`bash`建立软链接，因此无法在`windows`下运行，原项目详见顶部forked from。

# 用法

`macos`使用时，请**务必**在区分大小写的宗卷下克隆本仓库，并且在运行结束前都不要通过访达打开`data/`目录，以免自动生成的`.DS_Store`文件干扰运行。

首先克隆存储库
```bash
git clone https://github.com/fumiama/simple-AI-captcha-analyze.git
cd simple-AI-captcha-analyze
```
接下来可以选择预测或重新进行机器学习
1. 预测
该命令会分析`data/test_captcha`下的所有验证码
```bash
python3 ./image_predict.py
```
2. 重新学习
首先删除原数据集
```bash
rm -rf data/*
```
然后重新生成验证码+训练
```bash
python3 ./main.py
```