* 构建版本2024-0925 
* 原生支持linux mac win
```
magnet:?xt=urn:btih:920c1a578e815e9d0e4b843179306cdcb5e8e00d&dn=idapro90rc1
```
mac使用方法：
```
cd kg_patch
cp -f keygen2.py /Applications/IDA\ Professional\ 9.0.app/Contents/MacOS
cd /Applications/IDA\ Professional\ 9.0.app/Contents/MacOS
python keygen2.py
mv -f libida.dylib.patched libida.dylib
mv -f libida32.dylib.patched libida32.dylib
sudo codesign -f -s - /Applications/IDA\ Professional\ 9.0.app/Contents/MacOS/libida.dylib
sudo codesign -f -s - /Applications/IDA\ Professional\ 9.0.app/Contents/MacOS/libida32.dylib
sudo xattr -cr /Applications/IDA\ Professional\ 9.0.app
```

开启idapython
```
cd /Applications/IDA\ Professional\ 9.0.app/Contents/MacOS
./idapyswitch

# 选择你的venv使用的python
```

设置idapython venv
```
# 修改idapythonrc.py文件中mypath为你venv的路径
cp idapythonrc.py /User/name/.idapro
```

完整ida feeds支持#目前会导致PyQt5无法被引用，从而加载失败
```
cd /Applications/IDA\ Professional\ 9.0.app/Contents/MacOS/plugins/ida_feeds
pip install -r requirements.txt
`mkdir $HOME/.idapro/plugins`
`ln -s "$(pwd)" $HOME/.idapro/plugins/`
```
