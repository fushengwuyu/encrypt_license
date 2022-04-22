### 为python项目添加license

1. 创建license
```shell
python license_utils.py
```
执行完毕，会生成License.dat文件

2. 启动run.py，查看服务运行情况。若License.dat有误，程序会退出

```
*Error*: License file is modified!
```

3. 将整个项目加密为so文件，防止手动修改代码

```shell
python setup.py
```
执行完毕，会生成build文件夹，该文件夹为加密后的项目。在build中执行项目启动文件run.py，可以看到成功运行服务。

