# Elasticsearch 클라이언트 라이브러리 설치 (사전 필요)
# pip install elasticsearch==8.7.0
# 아래의 참고 페이지를 기반으로 함수와 인자를 채우세요.
# elasticsearch 8.7.0 document: https://elasticsearch-py.readthedocs.io/en/v8.7.0/
# https://www.elastic.co/guide/en/elasticsearch/client/python-api/8.7/examples.html#indexing-documents

from elasticsearch import Elasticsearch

# Elasticsearch 클라이언트 생성
# - `verify_certs=False`: 인증서 검증을 비활성화 (HTTPS 환경에서 필요)
es = Elasticsearch("http://localhost:9200")

# 사용할 인덱스 이름 지정
index_name = 'products'

# 1. 인덱스 생성
# - 인덱스가 존재하는지 확인 후, 없으면 생성
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)
    print(f"인덱스 '{index_name}'가 생성되었습니다.")
else:
    print(f"인덱스 '{index_name}'는 이미 존재합니다.")

# 2. 문서 삽입
# - Elasticsearch에 새로운 문서를 추가하는 작업
# - `id=1`을 지정하여 문서를 삽입 (ID를 지정하지 않으면 자동 생성)
# - ID 생성 방식:
#   1. 자동 생성 ID: ID를 지정하지 않으면 Elasticsearch가 자동으로 생성 (예: VhUTQpUBT_-Ind6MuiLS)
#   2. 사용자 지정 ID: id 파라미터로 직접 지정 (숫자나 문자열 모두 가능)
doc = {
    'product_name': 'Samsung Galaxy S25',
    'brand': 'Samsung',
    'release_date': '2025-02-07',  # 출시일 (ISO 8601 날짜 형식)
    'price': 799  # 가격 (float 형식)
}

# 문서 삽입 실행
# - 지정된 ID로 문서 저장
res = es.index(index=index_name, id=1, body=doc)
print(f"문서 삽입 결과: {res['result']} (ID: {res['_id']})")

# 3. 문서 조회
# - 특정 문서를 ID(id가 1인 문서) 기반으로 조회하는 API
res = es.get(index=index_name, id=1)
print(f"문서 조회 결과: {res['_source']}")

# 4. 문서 수정 (부분 업데이트)
# - 가격을 수정하는 업데이트 수행
doc = {
    'price': 1099.99
}

# TODO: 문서를 업데이트하는 코드를 작성하세요.
res = es.update(index=index_name, id=1, body={"doc": doc})  
print(f"문서 수정 결과: {res['result']}")

# 수정된 문서 확인을 위해 다시 조회
updated_doc = es.get(index=index_name, id=1)
print(f"수정된 문서 내용: {updated_doc['_source']}")

# 5. 문서 삭제
# - `delete` API를 사용하여 특정 ID의 문서를 삭제
res = es.delete(index=index_name, id=1)
print(f"문서 삭제 결과: {res['result']} (ID: {res['_id']})")
