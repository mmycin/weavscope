import weaviate
from weaviate.classes.init import Auth

client = weaviate.connect_to_custom(
    http_host="100.80.4.100",
    http_port=5556,
    http_secure=False,
    grpc_host="100.80.4.100",
    grpc_port=50051,
    grpc_secure=False,
    auth_credentials=Auth.api_key("user-a-key"),
    skip_init_checks=True
)

client.connect()
print(f"Version: {client.get_meta()['version']}")
print(f"gRPC Connected: {client.is_live()}") # check live status

# Try a simple REST query
try:
    cols = client.collections.list_all()
    print(f"Collections: {list(cols.keys())}")
except Exception as e:
    print(f"REST error: {e}")

# Try a gRPC batch ping? No, just close
client.close()
