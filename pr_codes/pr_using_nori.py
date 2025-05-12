from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import time
import json

# ----------------------------------------------
# 1. Elasticsearch 클라이언트 연결
# ----------------------------------------------
# TODO: 클러스터에 연결
es = Elasticsearch("http://localhost:9200")
index_name = "korean_nori"

# ----------------------------------------------
# 2. Nori 플러그인 설치 여부 확인
# ----------------------------------------------
print("Nori 플러그인 설치 여부 확인")
node_info = es.nodes.info()
nori_installed = any(
    "analysis-nori" in plugin["name"]
    for node in node_info["nodes"].values()
    for plugin in node.get("plugins", [])
)

if not nori_installed:
    print("Nori 플러그인이 설치되지 않음. 설치 후 다시 실행하세요.")
    exit(1)
else:
    print("Nori 플러그인이 설치됨.\n")

time.sleep(2)

# ----------------------------------------------
# 3. 기존 인덱스 삭제
# ----------------------------------------------
print("기존 인덱스 확인 및 삭제")
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"기존 인덱스 [{index_name}] 삭제 완료!\n")
else:
    print(f"기존 인덱스 [{index_name}] 없음, 새로 생성 진행.\n")

time.sleep(2)

# ----------------------------------------------
# 4. Nori 분석기 적용 인덱스 생성
# ----------------------------------------------
print(f"Nori 분석기를 적용한 인덱스 [{index_name}] 생성")
es.indices.create(index=index_name, body={
    # 1. settings (책장 전체에 대한 규칙, '책 정리 도구'를 만드는 곳)
    "settings": {
        "analysis": { # 텍스트 분석에 대한 규칙을 정의하는 곳
            "tokenizer": { # '단어 쪼개는 도구' (Tokenizer)를 만드는 곳
                "nori_user_dict": { # 'nori_user_dict'라는 이름의 단어 쪼개는 도구를 만들 거야
                    "type": "nori_tokenizer", # 이 도구는 한국어 Nori 토크나이저를 사용해
                    "decompound_mode": "mixed" # 복합 명사를 어떻게 처리할지 정하는 설정 (예: '아이폰케이스'를 '아이폰'과 '케이스'로 분리)
                }
            },
            "analyzer": { # '종합 분석기' (Analyzer)를 만드는 곳
                "korean_nori_analyzer": { # 'korean_nori_analyzer'라는 이름의 종합 분석기를 만들 거야
                    "type": "custom", # 이건 우리가 직접 조합해서 만드는 커스텀 분석기야
                    "tokenizer": "nori_tokenizer", # 이 분석기는 Nori 토크나이저를 써서 단어를 쪼갤 거야
                                                 # (참고: 위에 정의한 'nori_user_dict'가 아닌, Nori 플러그인의 기본 'nori_tokenizer'를 사용하고 있습니다.)
                    "filter": ["nori_part_of_speech"] # 단어를 쪼갠 후, 불필요한 품사(예: 조사, 어미 등)를 제거하는 필터도 적용할 거야
                }
            }
        }
    },

    # 2. mappings (책장 안의 '책'을 어떤 방식으로 보관할지, '책의 속성'을 정하는 곳)
    "mappings": {
        "properties": { # 책의 속성(필드)들을 정의하는 곳
            "text": { # 'text'라는 이름의 속성(필드)을 정의할 거야
                "type": "text", # 이 속성에는 텍스트 데이터가 들어갈 거야
                "analyzer": "korean_nori_analyzer" # 그리고 이 'text' 속성에 들어오는 텍스트는 위에서 만든 'korean_nori_analyzer'로 분석할 거야
            }
        }
    }
})
print("인덱스 생성 완료\n")
time.sleep(2)

# ----------------------------------------------
# 5. 문서 색인 (한국어 문장)
# ----------------------------------------------
print("한국어 문장 색인")
docs = [
    {"text": "엘라스틱서치는 검색 기능을 제공합니다."},
    {"text": "한국어 형태소 분석을 위해 Nori를 활용할 수 있습니다."}
]

# TODO: 두 개 문서 색인
for i, doc in enumerate(docs, start=1):
    es.index(index=index_name, body=doc)
print("문서 색인 완료\n")
time.sleep(2)

# ----------------------------------------------
# 6. 검색 테스트 (match_phrase)
# ----------------------------------------------
print("Nori를 활용한 검색 테스트")
query = {
    "query": {
        "match_phrase": {
            "text": "검색 기능"
        }
    }
}

# TODO: 검색 실행
result = es.search(index=index_name, body=query)
for hit in result["hits"]["hits"]:
    print(f"ID: {hit['_id']}, Score: {hit['_score']}, Text: {hit['_source']['text']}")

print("\nNori 기반 한국어 분석 작업 완료!")
