# Elasticsearch 클라이언트 라이브러리 설치 (사전 필요)
# pip install elasticsearch==8.7.0
# 아래의 참고 페이지를 기반으로 함수와 인자를 채우세요.
# elasticsearch 8.7.0 document: https://elasticsearch-py.readthedocs.io/en/v8.7.0/
# https://www.elastic.co/guide/en/elasticsearch/client/python-api/8.7/examples.html#indexing-documents

from elasticsearch import Elasticsearch, NotFoundError

# Elasticsearch 클라이언트 생성
# - Elasticsearch 인스턴스와 연결을 설정하는 함수
def create_es_client():
    # Elasticsearch 클라이언트 객체를 생성하고 반환합니다.
    return Elasticsearch(
        "http://localhost:9200" # Elasticsearch 인스턴스의 주소를 지정합니다.
    )

# 인덱스 존재 여부 확인 및 생성
# - 존재하지 않으면 새롭게 생성
def create_index(es, index_name):
    # es.indices.exists()를 사용하여 인덱스 존재 여부를 확인합니다.
    if not es.indices.exists(index=index_name):
        # TODO: 인덱스를 생성하는 코드를 작성하세요.
        # es.indices.create() 메서드를 사용하여 새로운 인덱스를 생성합니다.
        es.indices.create(index=index_name)
        print(f"인덱스 '{index_name}'가 생성되었습니다.")
    else:
        print(f"인덱스 '{index_name}'는 이미 존재합니다.")

# 문서 삽입
# - 특정 `doc_id`를 지정하여 문서를 인덱스에 추가
def insert_document(es, index_name, doc_id, doc):
    # TODO: 문서를 삽입하는 코드를 작성하세요.
    # es.index() 메서드를 사용하여 문서를 인덱스에 추가합니다.
    # index: 인덱스 이름, id: 문서 ID, document: 삽입할 문서 데이터
    res = es.index(index=index_name, id=doc_id, document=doc)
    # 삽입 작업 결과를 출력합니다.
    print(f"문서 삽입 결과(ID {doc_id}): {res['result']}") if res else print("문서 삽입 실패")

# 문서 조회
# - 특정 ID의 문서를 검색하여 반환
def get_document(es, index_name, doc_id):
    try:
        # TODO: 문서를 조회하는 코드를 작성하세요.
        # es.get() 메서드를 사용하여 특정 ID의 문서를 조회합니다.
        # index: 인덱스 이름, id: 문서 ID
        res = es.get(index=index_name, id=doc_id)
        # 조회된 문서의 실제 데이터는 응답 객체의 '_source' 필드에 있습니다.
        print(f"문서 조회 결과(ID {doc_id}): {res['_source']}")
        # 조회된 문서 데이터를 반환합니다.
        return res['_source']
    # 조회하려는 문서가 존재하지 않으면 NotFoundError 예외가 발생합니다.
    except NotFoundError:
        print(f"문서(ID {doc_id})가 존재하지 않습니다.")
        return None

# 문서 수정 (부분 업데이트)
# - 특정 필드만 업데이트 가능 (`doc` 키워드 사용)
def update_document(es, index_name, doc_id, update_fields):
    try:
        # TODO: 문서를 수정하는 코드를 작성하세요.
        # es.update() 메서드를 사용하여 문서의 특정 필드를 업데이트합니다.
        # index: 인덱스 이름, id: 문서 ID, doc: 업데이트할 필드와 값 (딕셔너리 형태)
        res = es.update(index=index_name, id=doc_id, doc=update_fields)
        # 수정 작업 결과를 출력합니다.
        print(f"문서 수정 결과(ID {doc_id}): {res['result']}") if res else print("문서 수정 실패")
    # 수정하려는 문서가 존재하지 않으면 NotFoundError 예외가 발생합니다.
    except NotFoundError:
        print(f"문서(ID {doc_id})가 존재하지 않아 수정할 수 없습니다.")

# Upsert 기능 (문서가 없으면 삽입, 있으면 수정)
# - 기존 문서가 없으면 새롭게 생성 (`doc_as_upsert=True`)
def upsert_document(es, index_name, doc_id, update_fields):
    # TODO: Upsert를 수행하는 코드를 작성하세요.
    # es.update() 메서드를 사용하며, doc_as_upsert=True 옵션을 추가합니다.
    # index: 인덱스 이름, id: 문서 ID, doc: 삽입 또는 업데이트할 필드와 값, doc_as_upsert=True: 없으면 삽입하도록 설정
    res = es.update(index=index_name, id=doc_id, doc=update_fields, doc_as_upsert=True)
    # Upsert 작업 결과를 출력합니다. (결과는 'created' 또는 'updated'가 될 수 있습니다)
    print(f"Upsert 결과(ID {doc_id}): {res['result']}") if res else print("Upsert 실패")

# 문서 삭제
# - 특정 ID를 가진 문서를 삭제
def delete_document(es, index_name, doc_id):
    try:
        # TODO: 문서를 삭제하는 코드를 작성하세요.
        # es.delete() 메서드를 사용하여 특정 ID의 문서를 삭제합니다.
        # index: 인덱스 이름, id: 문서 ID
        res = es.delete(index=index_name, id=doc_id)
        # 삭제 작업 결과를 출력합니다.
        print(f"문서 삭제 결과(ID {doc_id}): {res['result']}") if res else print("문서 삭제 실패")
    # 삭제하려는 문서가 존재하지 않으면 NotFoundError 예외가 발생합니다.
    except NotFoundError:
        print(f"문서(ID {doc_id})가 존재하지 않아 삭제할 수 없습니다.")

# 실행 흐름 (메인 함수)
if __name__ == "__main__":
    es = create_es_client() # Elasticsearch 클라이언트 생성
    index_name = "products" # 사용할 인덱스 이름
    doc_id = 1 # 사용할 문서 ID

    # 예제 문서 데이터를 정의합니다.
    document = {
        "product_name": "Samsung Galaxy S25",
        "brand": "Samsung",
        "release_date": "2025-02-07",
        "price": 1199.99
    }

    # 1. 인덱스 생성 함수 호출
    create_index(es, index_name)

    # 2. 문서 삽입 함수 호출
    insert_document(es, index_name, doc_id, document)

    # 3. 문서 조회 함수 호출
    get_document(es, index_name, doc_id)

    # 4. 문서 수정 함수 호출 (가격 변경)
    update_document(es, index_name, doc_id, {"price": 1099.99})

    # 5. 문서 조회 함수 호출 (수정된 데이터 확인)
    get_document(es, index_name, doc_id)

    # 6. Upsert 함수 호출 (문서가 있으면 업데이트, 없으면 생성)
    # 이 시점에는 문서가 존재하므로 업데이트 됩니다.
    upsert_document(es, index_name, doc_id, {"price": 999.99})

    # 7. 문서 조회 함수 호출 (Upsert 확인)
    get_document(es, index_name, doc_id)

    # 8. 문서 삭제 함수 호출
    delete_document(es, index_name, doc_id)

    # 9. 문서 조회 함수 호출 (삭제 확인 - 문서 없음 출력 예상)
    get_document(es, index_name, doc_id)

    # 10. Upsert 함수 호출 (문서가 없으므로 생성)
    # 이 시점에는 문서가 삭제되었으므로 새로 생성됩니다.
    upsert_document(es, index_name, doc_id, {"price": 1399.99})

    # 11. 문서 조회 함수 호출 (Upsert 확인)
    get_document(es, index_name, doc_id)