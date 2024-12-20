# ベースイメージとしてPython 3.10を使用
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストールするrequirements.txtをコピー
COPY Mdl06_HandleRequest/requirements.txt /app/

# パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# srcディレクトリとtestdataディレクトリをコピー
COPY Mdl06_HandleRequest/src/ /app/src/
COPY Mdl06_HandleRequest/testdata/ /app/testdata/

EXPOSE 8080

# Cloud Buildによるデプロイで実行するためのエントリーポイント
ENTRYPOINT ["python", "/app/src/main.py"]