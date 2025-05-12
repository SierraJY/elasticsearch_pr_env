from elasticsearch import Elasticsearch

# Elasticsearch 클라이언트 연결
es = Elasticsearch("http://localhost:9200")

# match_all 쿼리
response = es.search(
    index="ecommerce_ws",
    body={
        "query": {
            "match_all": {}
        }
    }
)

# 결과 출력
for hit in response["hits"]["hits"]:
    print(f"ID: {hit['_id']}, Source: {hit['_source']}")
