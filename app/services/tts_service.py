import edge_tts


async def text_to_speech(
    text: str,
    output_path: str,
):
    communicate = edge_tts.Communicate(
        text,
        "en-US-AriaNeural",
    )

    await communicate.save(output_path)