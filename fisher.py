from app import create_app

app = create_app()

if __name__ == '__main__':
    # 如果要使用vscode调试，需要将debug设置为False，否则无法命中请求断点
    app.run(host='0.0.0.0', debug=True)


