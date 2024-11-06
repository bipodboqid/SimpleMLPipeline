# TensorFlow/TFXとGoogle Cloud Platformを用いた、ディープラーニングによる画像診断システムおよびMLOps基盤の構築
このリポジトリは、上記見出しの個人開発プロジェクトのソースリポジトリです。
プロジェクト内容の詳細説明および開発ドキュメントは
[Qiita記事(簡易版)](https://qiita.com/bipodboqid/private/10b9ad6173f7a16b9998)
[Qiita記事(詳細版)(エンジニア/データサイエンティストの方向け)](https://qiita.com/bipodboqid/private/195aff28a4ded12ccf51)
に掲載しておりますので、そちらをご確認いただけますと幸いです。

参考までに、上記記事の要約を以下に掲載いたします。

## 記事要約
1. **機械学習・ディープラーニングのビジネス利用は「データサイエンティストが学習させた高性能の機械学習モデル」だけでは成立せず、モデルの改修・デプロイ・運用監視に大量の人手と時間が求められる**<br>
機械学習・ディープラーニングのモデルをビジネスに利用する場合、「モデルを学習させるコード」以外にも多くの要素が求められ、結果として開発・運用のプロセスは複雑で時間のかかるものになります。<br>また、コンペティションや個人利用のための開発の場合とは異なり、ビジネス利用では、本番リリース済みモデルを継続的に監視し、高頻度に改修（再学習）しなければモデルのビジネス価値が保たれません。<br>そのため、機械学習プロジェクトには、「コストの高い改修プロセスを高頻度に繰り返さなければならない」困難が付きまといます。
![hiddentechnicaldebt.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2960191/3349cc82-8395-8094-dc49-8a2f47868cf6.png "hiddentechnicaldebt")
*コード（画像中央）はビジネス利用される機械学習システムのごく一部に過ぎない<br>（[Sculley et al., 2015](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf "a")[^1]より画像を引用）*<br><br><br>

2. **1の課題を解決するため、モデル開発・システム開発・本番運用/監視を統合するMLOps（エムエルオプス）の手法が有効である**<br>
MLOpsは、機械学習モデルの開発/改修・デプロイ・本番運用/監視のサイクルの安定・高速化のために用いられる手法です。
MLOpsの実践では、モデルの開発・改修プロセスおよび本番運用時のモデルの性能監視の大部分を自動化し、モニタリングします。
これらプロセスを高速・高頻度に実施することは、機械学習プロジェクトのビジネス上のインパクトの最大化に大きく寄与します。
![MLOpsimage.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2960191/00dccd0c-2a92-55a8-5740-6cd3f8bb3a8d.png)
*MLOpsによって機械学習モデルの開発と運用監視のサイクルは統合・高速化される<br>（画像出典：[Neal Analytics](https://www.linkedin.com/pulse/what-mlops-edwin-webster/)）* 
<br><br>

3. **今回のプロジェクトでは、ディープラーニングのモデルを開発するとともに、MLOps基盤の実装手法を実践・検証した**<br>
本プロジェクトは、ディープラーニングモデルおよびMLOps基盤の実装技術（事前に学習済み）の実践・検証を目的として実施しました。
具体的には、TensorFlow/TFX・Google Cloud Platform（GCP）などの関連技術・サービスを適切に用いて開発・運用の効率化を図った場合、限られた人月でどの程度までMLOps基盤を実現できるかを実践によって検証しました。<br><br><br>
4. **サービス例として、ディープラーニングを用いた画像診断モデルを開発した**<br>
本プロジェクトでは、ディープラーニングを用いたモデル例として、「植物の葉の画像から健康/不健康を判別するモデル」（以下、植物画像診断モデル）を開発しました。
![AppImage.drawio.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2960191/27b07f95-21cd-c741-e44d-49ec0c43fc23.png)
*筆者の所有する観葉植物の葉の健康状態をモデルに診断させた例。<br>「94.75%の確率で不健康だ」と診断されている*
<br><br>
5. **植物画像診断モデルの本番運用を想定し、モデルの改修・デプロイ・運用監視のサイクルを高速化するMLOps基盤を構築した**<br>
上記「4」の植物画像診断サービスを本番運用する際のビジネス価値の最大化のため、モデル改修・デプロイ・運用監視プロセスの大部分を自動化し、改修のサイクルを迅速に実行するシステム（MLOps基盤）を構築しました。
![BF_diagram_tobe.drawio.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2960191/095c534a-aa5e-25b5-7e4e-9bce5d30fbef.png)
*パイプライン化、パイプライン自動化等の取り組みにより、改修サイクルが安定化・高速化する*
<br><br>
6. **実践による検証の結果、GCPとTensorFlow/TFXのMLOps基盤構築におけるインパクトと現時点での限界が明らかになった**<br><br>上記「3」の検証のため、稼働時間の上限をおよそ1人月(160時間)、プロジェクト実施期間を2024/10/1(火)~11/2(土)としてプロジェクトを実施しました。<br>検証により、「GCPの各種サービスおよびTensorFlow/TFXを用いることで、個別モジュールのスクラッチ開発を極力押さえながら[MLOps成熟度](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)レベル1~2相当の要件を満たせる」ことが分かりました。
一方、画像データの処理に未対応のサービスがあるなど、現時点でのこれら技術・サービスの適用範囲の限界も一部確認されました。
<br><br>
7. **加えて、個人開発という条件と本来MLOpsを適用すべき状況とのギャップも浮き彫りになり、異なる専門性を持つ複数のチームが関わるプロジェクトでMLOpsの有効な実現方法を模索する必要性が明確になった**<br><br>本来のMLOpsは、チームビルディング・プロジェクト規約・システム化計画など、多様な取り組みによって実践される手法です。<br>一方、今回のプロジェクトでは、個人開発という制約から、機械学習ワークフローのパイプライン化やデプロイ・運用監視の自動化にスコープを絞ってMLOpsを実践する事になりました。<br>また、今回開発した機械学習モデルはビジネスに利用していないため、ユーザ行動指標の監視が行われないなど、「機械学習モデルのビジネス価値の最大化」を目指すMLOpsの実践としては条件が適切でない部分もありました。<br>これを踏まえ、実際のビジネス環境での機械学習プロジェクトで開発・運用プロセスの合理化を模索する必要性が改めて実感されました。