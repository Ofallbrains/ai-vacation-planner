from app.rag.chunker import chunk_text


text = """
Paris is the capital of France. It is famous for museums,
architecture, food, cafes, and historic neighborhoods.

Montmartre is known for its artistic history and Sacré-Cœur.

Canal Saint-Martin is a quieter area where visitors can walk
along the canal and explore local cafes.

The Paris Metro is one of the most convenient ways to travel
around the city.
"""


chunks = chunk_text(
    text,
    chunk_size=100,
    overlap=20,
)


for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {index} ---")
    print(chunk)