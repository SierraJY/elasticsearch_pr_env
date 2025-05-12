from elasticsearch import Elasticsearch, NotFoundError # Elasticsearch 클래스와 NotFoundError 예외 클래스를 임포트합니다.

# Elasticsearch 클라이언트 생성
es = Elasticsearch("http://localhost:9200") # 로컬 Elasticsearch에 연결합니다.

index_name = "products" # 사용할 인덱스 이름을 정의합니다.
doc_id = 1 # 작업할 문서의 ID를 정의합니다.

# 1. 기존 문서 삭제 (Upsert 테스트 준비)
# Upsert 테스트를 위해 해당 ID의 문서가 있으면 삭제합니다.
try:
    # TODO: 문서를 삭제하는 코드를 작성하세요.
    # es.delete() 메서드를 사용하여 특정 인덱스의 특정 ID 문서를 삭제합니다.
    es.delete(index=index_name, id=doc_id)
    print("1. 기존 문서 삭제 완료 (업서트 테스트 준비)")
# 문서를 삭제하려 했으나 해당 ID의 문서가 없는 경우 NotFoundError가 발생합니다.
except NotFoundError:
    print("1. 삭제할 문서가 없음 (이미 삭제된 상태)")

# 2. Upsert 실행 - 문서가 없으면 삽입
# Upsert는 문서를 업데이트하되, 문서가 존재하지 않으면 새로 생성하는 기능입니다.
# 업데이트 또는 삽입될 문서의 내용을 정의합니다.
upsert_body_1 = {
    "doc": { # 업데이트할 필드와 값
        "price": 999.99
    },
    # doc_as_upsert: True로 설정하면 doc 내용을 사용하여 문서를 생성(upsert)합니다.
    "doc_as_upsert": True
}
# TODO: upsert 기능을 호출하는 코드를 작성하세요.
# es.update() 메서드를 사용하며, index, id와 함께 body에 upsert_body_1을 전달합니다.
response_1 = es.update(index=index_name, id=doc_id, body=upsert_body_1)
# upsert 작업의 결과 (예: "created" 또는 "updated")를 출력합니다.
print("2. 업서트 (없으면 삽입):", response_1["result"])

# 3. 문서 조회
# upsert된 문서를 조회합니다.
# TODO: 문서를 조회하는 코드를 작성하세요.
# 이 부분에 es.get() 호출 코드가 들어갑니다.
# es.get() 메서드를 사용하여 특정 인덱스의 특정 ID 문서를 조회하고 결과를 'doc' 변수에 할당합니다.
doc = es.get(index=index_name, id=doc_id)
# 조회된 문서의 실제 데이터는 'doc' 객체의 "_source" 필드에 있습니다.
print("3. 문서 내용:", doc["_source"])