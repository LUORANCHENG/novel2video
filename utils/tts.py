import asyncio
import edge_tts

async def generate_speech(text: str, language: str, txt_name: str, order: int, voice="en-US-EmmaMultilingualNeural") -> None:
    max_retries = 10
    retry_delay = 2
    attempt = 0

    while attempt < max_retries:
        try:
            communicate = edge_tts.Communicate(text, voice, rate='+25%')
            await communicate.save(f'./output/audios/{txt_name}/{language}/{order}.mp3')
            break
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"Failed to save speech after {max_retries} attempts.")
