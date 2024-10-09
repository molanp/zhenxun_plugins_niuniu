# zhenxun_plugin_niuniu
真寻群内小游戏插件-牛牛大作战(误

# 目前暂不适配0.2版本zhenxun，如果需要使用，请使用nonebot分支内的文件或release内的nonebot版本
# 本插件无需数据库！(因为我不会bushi)

# [nonebot版本](https://github.com/molanp/zhenxun_plugin_niuniu/tree/nonebot)

## 使用方法
下载压缩包，解压并放入`extensive_plugin`文件夹或其他自定义文件夹中

## 指令
|指令|功能描述|
|---|---|
|注册牛牛|注册你的牛牛|
|注销牛牛|删除你的牛牛|
|jj [@user](或"击剑)|与注册牛牛的人进行击剑，对战结果影响牛牛长度|
|我的牛牛|查看自己牛牛长度|
|牛牛长度排行|查看本群正数牛牛长度排行|
|牛牛深度排行|查看本群负数牛牛深度排行|
|打胶|对自己的牛牛进行操作，结果随机|

## 依赖

正常情况真寻的虚拟环境里附带此模块
```powershell
pip install ujson
```

## 说明
群友长度数据位于插件文件夹中的`data/long.json`中
