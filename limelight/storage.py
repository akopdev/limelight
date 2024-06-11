from limelight.settings import settings
import chromadb

client = chromadb.PersistentClient(path=f"var/{settings.storage_name}")
collection = client.get_or_create_collection(name=settings.storage_name)
