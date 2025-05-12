from elasticsearch import Elasticsearch
import time

# ----------------------------------------------
# 1. Elasticsearch 클라이언트 연결
# ----------------------------------------------
es = Elasticsearch("http://localhost:9200")
index_name = "analyzer_comparison"

# ----------------------------------------------
# 2. 기존 인덱스 삭제
# ----------------------------------------------
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"기존 인덱스 [{index_name}] 삭제 완료")
else:
    print(f"기존 인덱스 [{index_name}] 없음, 새로 생성 진행")
time.sleep(2)

# ----------------------------------------------
# 3. 다양한 Analyzer 설정 포함한 인덱스 생성
# ----------------------------------------------
print(f"인덱스 [{index_name}] 생성 및 analyzer 설정 적용")
# Elasticsearch의 분석기(Analyzer) 설정은 두 가지 레벨에서 가능합니다:
# 1. 인덱스 레벨: settings.analysis.analyzer에서 정의하여 인덱스 전체에 적용
# 2. 필드 레벨: mappings.properties.{field_name}.analyzer에서 정의하여 특정 필드에만 적용
#
# 현재 설정:
# - text 필드에 여러 분석기를 멀티필드로 정의:
#   - standard: 기본 분석기 (소문자 변환, 특수문자 제거, 공백 기준 토큰화)
#   - whitespace: 공백만으로 토큰화 (대소문자, 특수문자 유지)
#   - simple: 소문자 변환, 특수문자 제거, 공백 기준 토큰화
#   - stop: 불용어(stop words) 제거
#   - keyword: 분석 없이 전체 문자열을 하나의 토큰으로 처리
es.indices.create(index=index_name, body={
    "mappings": {
        "properties": {
            "text": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "whitespace": { "type": "text", "analyzer": "whitespace" },
                    "simple": { "type": "text", "analyzer": "simple" },
                    "stop": { "type": "text", "analyzer": "stop" },
                    "keyword": { "type": "keyword" }
                }
            }
        }
    }
})
time.sleep(2)

# ----------------------------------------------
# 4. 테스트 문장 정의
# ----------------------------------------------
test_text = "The QUICK brown-fox 123 jumps!!! over & lazy-dogs?"

# ----------------------------------------------
# 5. analyzer 테스트 함수 정의
# ----------------------------------------------
# es.indices.analyze() 메서드는 Elasticsearch의 분석기(Analyzer)가 텍스트를 어떻게 처리하는지 테스트해볼 수 있는 API
def analyze_with(analyzer_name):
    print(f"\n[{analyzer_name.capitalize()} Analyzer 결과]")
    # TODO: analyze API 실행
    response = es.indices.analyze(index=index_name, analyzer=analyzer_name, text=test_text)
    for token in response["tokens"]:
        print(f"- {token['token']}")

# ----------------------------------------------
# 6. 각 Analyzer 비교 실행
# ----------------------------------------------
# TODO: standard, whitespace, simple, stop 순서대로 테스트
analyze_with("standard")
time.sleep(1)

analyze_with("whitespace")
time.sleep(1)

analyze_with("simple")
time.sleep(1)

analyze_with("stop")
time.sleep(1)

print("\nElasticsearch 기본 Analyzer 비교 테스트 완료!")
