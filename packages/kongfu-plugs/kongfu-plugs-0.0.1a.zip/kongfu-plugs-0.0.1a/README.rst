kongfu-plugs
------------
Plugs is a collection project for kongfu project

kongfu项目中使用的第三方产品的代码仓库

plugs列表
=======

* top: 阿里大鱼短信验证接口

kongfu-plugs发布流程
=================
* 如果有非Python编写的文件要打包发布，则应对 `minifest.in` 文件进行修改，将这类文件包含进来。典型代码如下
```
include readme.rst
include *.html
recursive-include any-plug-package-such-as-top *.txt, *.css, *.html, *.png
```
* 新的版本应对 `setup.py` 中的 `version` 值进行设置成正确的版本号

* `python setup.py sdist` ：打包成生成easy_install支持格式的可发布包

* `python setup.py register` ：在你的主机上做第一次发布时需要执行，根据提示选择 `1. use your existing login`
    用户名:uniyes  密码:uniyes1234567890


* `python setup.py sdist upload` ：向pypi上传打包好的文件
