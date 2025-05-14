from elasticsearch import Elasticsearch, NotFoundError, helpers
from datetime import datetime

# Elasticsearch 클라이언트 생성
es = Elasticsearch("http://localhost:9200")

# 1. 기존 'kibana_kql_test' 인덱스 삭제
try:
    es.indices.delete(index="kibana_kql_test")
    print("1. 'kibana_kql_test' 인덱스 삭제 완료")
except NotFoundError:
    print("1. 삭제할 인덱스가 없음 (이미 삭제된 상태)")

# 2. 'kibana_kql_test' 인덱스 생성 및 매핑 설정
es.indices.create(
    index="kibana_kql_test",
    mappings={
        "properties": {
            "user": {"type": "keyword"},
            "role": {"type": "keyword"},
            "message": {"type": "text"},
            "status": {"type": "keyword"},
            "age": {"type": "integer"},
            "created_at": {"type": "date"}
        }
    }
)
print("2. 'kibana_kql_test' 인덱스 생성 완료")

# 3. 샘플 데이터 Bulk 삽입
bulk_insert_data = [
    {
        "_index": "kibana_kql_test",
        "_id": "1",
        "_source": {
            "user": "Alice",
            "role": "admin",
            "message": "System updated successfully",
            "status": "success",
            "age": 32,
            "created_at": "2025-02-22T12:30:00"
        }
    },
    {
        "_index": "kibana_kql_test",
        "_id": "2",
        "_source": {
            "user": "Bob",
            "role": "user",
            "message": "Login attempt failed",
            "status": "failure",
            "age": 28,
            "created_at": "2025-02-22T13:00:00"
        }
    },
    {
        "_index": "kibana_kql_test",
        "_id": "3",
        "_source": {
            "user": "Charlie",
            "role": "admin",
            "message": "New user registered",
            "status": "success",
            "age": 45,
            "created_at": "2025-02-22T14:15:00"
        }
    },
    {
        "_index": "kibana_kql_test",
        "_id": "4",
        "_source": {
            "user": "David",
            "role": "moderator",
            "message": "Post deleted by moderator",
            "status": "success",
            "age": 35,
            "created_at": "2025-02-22T15:45:00"
        }
    },
    {
        "_index": "kibana_kql_test",
        "_id": "5",
        "_source": {
            "user": "Eve",
            "role": "user",
            "message": "Password reset requested",
            "status": "pending",
            "age": 29,
            "created_at": "2025-02-22T16:10:00"
        }
    },
    {
        "_index": "kibana_kql_test",
        "_id": "6",
        "_source": {
            "user": "Frank",
            "role": "user",
            "message": "Account locked due to multiple failures",
            "status": "failure",
            "age": 40,
            "created_at": "2025-02-22T16:30:00"
        }
    }
]

# helpers.bulk를 사용하여 bulk 문서 삽입
success, failed = helpers.bulk(es, bulk_insert_data, stats_only=True)
print(f"3. Bulk 문서 삽입 완료 - 성공: {success}, 실패: {failed}")

# 강제로 색인 refresh
es.indices.refresh(index="kibana_kql_test")

# 4. 삽입된 문서 조회
print("\n4. 삽입된 모든 문서:")
res = es.search(index="kibana_kql_test", query={"match_all": {}}, size=10)
for hit in res["hits"]["hits"]:
    doc = hit["_source"]
    print(f"ID: {hit['_id']}, User: {doc['user']}, Role: {doc['role']}, Status: {doc['status']}")

# 5. 예시 쿼리들
print("\n5. admin 역할을 가진 사용자들:")
admin_query = {
    "query": {
        "term": {
            "role": "admin"
        }
    }
}
res = es.search(index="kibana_kql_test", body=admin_query)
for hit in res["hits"]["hits"]:
    doc = hit["_source"]
    print(f"- {doc['user']}: {doc['message']}")

print("\n6. 실패(failure) 상태인 로그들:")
failure_query = {
    "query": {
        "term": {
            "status": "failure"
        }
    }
}
res = es.search(index="kibana_kql_test", body=failure_query)
for hit in res["hits"]["hits"]:
    doc = hit["_source"]
    print(f"- {doc['user']}: {doc['message']} (at {doc['created_at']})")

print("\n7. 30세 이상 사용자들:")
age_query = {
    "query": {
        "range": {
            "age": {
                "gte": 30
            }
        }
    }
}
res = es.search(index="kibana_kql_test", body=age_query)
for hit in res["hits"]["hits"]:
    doc = hit["_source"]
    print(f"- {doc['user']} (Age: {doc['age']}, Role: {doc['role']})")

# 8. 특정 시간 범위의 데이터 조회 (2025-02-22 15:00 이후)
print("\n8. 2025-02-22 15:00 이후 생성된 로그들:")
time_query = {
    "query": {
        "range": {
            "created_at": {
                "gte": "2025-02-22T15:00:00"
            }
        }
    }
}
res = es.search(index="kibana_kql_test", body=time_query)
for hit in res["hits"]["hits"]:
    doc = hit["_source"]
    print(f"- {doc['user']}: {doc['message']} (at {doc['created_at']})")