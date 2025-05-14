from elasticsearch import Elasticsearch, NotFoundError, helpers
import json

# Elasticsearch 클라이언트 생성
es = Elasticsearch("http://localhost:9200")

# 1. 기존 'nested_test' 인덱스 삭제
try:
    es.indices.delete(index="nested_test")
    print("1. 'nested_test' 인덱스 삭제 완료")
except NotFoundError:
    print("1. 삭제할 인덱스가 없음 (이미 삭제된 상태)")

# 2. 'nested_test' 인덱스 생성
es.indices.create(
    index="nested_test",
    settings={
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    mappings={
        "properties": {
            "title": {"type": "text"},
            "reviews": {
                "type": "nested",
                "properties": {
                    "author": {"type": "text"},
                    "rating": {"type": "integer"},
                    "comment": {"type": "text"}
                }
            }
        }
    }
)
print("2. 'nested_test' 인덱스 생성 완료")

# 3. Bulk Insert 실행
bulk_insert_data = [
    {
        "_index": "nested_test", 
        "_id": "1", 
        "_source": {
            "title": "Elasticsearch Advanced Guide",
            "reviews": [
                {"author": "Alice", "rating": 5, "comment": "Excellent book!"},
                {"author": "Bob", "rating": 3, "comment": "Decent but could be improved."}
            ]
        }
    },
    {
        "_index": "nested_test", 
        "_id": "2", 
        "_source": {
            "title": "Mastering Elasticsearch",
            "reviews": [
                {"author": "Charlie", "rating": 4, "comment": "Great for advanced users."},
                {"author": "David", "rating": 2, "comment": "Too complex for beginners."}
            ]
        }
    },
    {
        "_index": "nested_test", 
        "_id": "3", 
        "_source": {
            "title": "Introduction to Elasticsearch",
            "reviews": [
                {"author": "Eve", "rating": 5, "comment": "A great starting point!"},
                {"author": "Frank", "rating": 3, "comment": "Covers the basics well."}
            ]
        }
    },
    {
        "_index": "nested_test", 
        "_id": "4", 
        "_source": {
            "title": "Elasticsearch Deep Dive",
            "reviews": [
                {"author": "Grace", "rating": 4, "comment": "Very in-depth and useful."},
                {"author": "Hank", "rating": 5, "comment": "Best resource for Elasticsearch!"}
            ]
        }
    },
    {
        "_index": "nested_test", 
        "_id": "5", 
        "_source": {
            "title": "Practical Elasticsearch",
            "reviews": [
                {"author": "Ivy", "rating": 3, "comment": "Good but lacks examples."},
                {"author": "Jack", "rating": 4, "comment": "Practical and insightful."}
            ]
        }
    }
]

# helpers.bulk를 사용하여 bulk 문서 삽입
success, failed = helpers.bulk(es, bulk_insert_data, stats_only=True)
print(f"3. Bulk 문서 삽입 완료 - 성공: {success}, 실패: {failed}")

# 강제로 색인 refresh
es.indices.refresh(index="nested_test")

# 4. 삽입된 문서 조회
print("\n4. 삽입된 문서:")
res = es.search(index="nested_test", query={"match_all": {}}, size=10)
for hit in res["hits"]["hits"]:
    print(f"ID: {hit['_id']}, Title: {hit['_source']['title']}")
    for review in hit["_source"]["reviews"]:
        print(f"  - {review['author']}: {review['rating']}/5 - {review['comment']}")
    print()

# 5. Nested 쿼리 예시 - 평점이 4 이상인 리뷰가 있는 책 찾기
print("5. 평점이 4 이상인 리뷰가 있는 책들:")
nested_query = {
    "query": {
        "nested": {
            "path": "reviews",
            "query": {
                "range": {
                    "reviews.rating": {
                        "gte": 4
                    }
                }
            }
        }
    }
}
res = es.search(index="nested_test", body=nested_query)
for hit in res["hits"]["hits"]:
    print(f"- {hit['_source']['title']}")

# 6. 특정 저자의 리뷰가 있는 책 찾기
print("\n6. 'Alice'의 리뷰가 있는 책:")
author_query = {
    "query": {
        "nested": {
            "path": "reviews",
            "query": {
                "match": {
                    "reviews.author": "Alice"
                }
            }
        }
    }
}
res = es.search(index="nested_test", body=author_query)
for hit in res["hits"]["hits"]:
    print(f"- {hit['_source']['title']}")