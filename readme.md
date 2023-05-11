# 静态个人主页生成
## 快速搭建
### Step1: 准备页面描述材料
参考示例： [Input.md](tools/Input.md)
> 注意：请务必按照示例填写材料，文档结构的变化会导致页面生成错误
- md文件可以直接使用记事本打开，不过推荐用Vscode预览文档
- Markdown 语法（不懂也无关，只要按层次填写内容即可，注意：不同数量的`#`表示不同层次的标题，不可改变结构只能填写内容，`-`表示列表，可增加或减少）
- 支持HTML标签嵌入，可增强文本效果，如：`<b>加粗字体</b>`

### Step2: 准备图片材料
存放至`styles/img`文件夹下，注意文件名与`Step1`中图片名称保持一致

### Step3: 生成文档
安装依赖：
`pip install -r .\requirements.txt`

运行页面生成器：
`python tools/Generate.py tools/Input.md ZH`

其中：
- `tools/Input.md`为页面描述文件的位置
- `ZH`为中文页面，`EN`为英文页面

### Step4: 部署到github.io
- 参考：https://zhuanlan.zhihu.com/p/91652100 建立`用户名.github.io`的仓库
- 将生成的页面文件夹`page`的全部文件上传至该仓库
- 预览效果：`https://用户名.github.io`