def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """
    Split text into chunks while trying to preserve paragraphs.
    """

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # If adding the paragraph keeps us within the limit
        if len(current_chunk) + len(paragraph) + 1 <= chunk_size:
            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:
            # Save the current chunk
            if current_chunk:
                chunks.append(current_chunk)

            # Start a new chunk
            current_chunk = paragraph

    # Add the final chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks