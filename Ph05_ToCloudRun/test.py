import tensorflow as tf
import base64
import os
from google.cloud import aiplatform
from fastapi import FastAPI, File, UploadFile

# FastAPI アプリケーションの作成
app = FastAPI()

ENDPOINT_ID = '1706270522494418944'
GOOGLE_CLOUD_REGION = 'asia-northeast1'
GOOGLE_CLOUD_PROJECT = 'mlpipelineportfolio'
image_path = 'mnist_156.jpg'  # コンテナ内の画像パス

# Function to convert image path into TFExample
def create_example_from_path(image_path):
    features = {
        'image_raw': tf.train.Feature(bytes_list=tf.train.BytesList(
            value=[tf.io.read_file(image_path).numpy()])),
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=features))
    examples = example_proto.SerializeToString()
    return base64.b64encode(examples).decode()

# Function to convert User-provided bytes image into TFExample
def create_example_from_bytes(image_bytes):
    features = {
        'image_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_bytes])),
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=features))
    examples = example_proto.SerializeToString()
    return base64.b64encode(examples).decode()

# Function to request Vertex AI Predictions endpoint to perform inference and save result 
def endpoint_predict_sample(project: str, location: str, instances: list, endpoint: str):
    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.Endpoint(endpoint)
    prediction = endpoint.predict(instances=instances)
    return prediction

# GETリクエストに対応するエンドポイントの作成
@app.get("/test-predict")
async def test_predict():
    try:
        instances = [
            {
                'b64': create_example_from_path(image_path),  # コンテナ内の画像を使用
            },
        ]
        result = endpoint_predict_sample(
            project=GOOGLE_CLOUD_PROJECT,
            location=GOOGLE_CLOUD_REGION,
            instances=instances,
            endpoint=ENDPOINT_ID
        )
        return {"predictions": result}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to accept inference request
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try: 
        # 画像ファイルを読み込み
        image_bytes = await file.read()
        # 推論用リクエストの作成
        instances = [{"b64": create_example_from_bytes(image_bytes)}]
        # Google Cloud AI Predictionにリクエストを送信
        prediction = endpoint_predict_sample(
                project=GOOGLE_CLOUD_PROJECT,
                location=GOOGLE_CLOUD_REGION,
                instances=instances,
                endpoint=ENDPOINT_ID)
        return {"prediction": prediction}
    except Exception as e:
        return {'error': str(e)}

# Must listen on specific port(8080) to comply with cloud build policy
if __name__ == '__main__':
    import uvicorn
    # 環境変数 PORT からポート番号を取得 (デフォルトは8080)
    port = int(os.environ.get("PORT", 8080))
    # UvicornでFastAPIアプリケーションを実行
    uvicorn.run(app, host="0.0.0.0", port=port)