from __future__ import annotations
import argparse
import asyncio
import json
from pathlib import Path

from .vi_client import VideoIndexer
from .llm import summarize_from_transcript

parser = argparse.ArgumentParser(prog="video-agent", description="Azure Video Agent CLI")
sub = parser.add_subparsers(dest="cmd", required=True)

# index: يبدأ فهرسة فيديو من رابط URL
p_index = sub.add_parser("index", help="Index a remote video URL via Azure AI Video Indexer")
p_index.add_argument("--name", required=True, help="Friendly name for the video")
p_index.add_argument("--url", required=True, help="Public or SAS video URL")

# insights: يجلب الـ insights/transcript لفيديو عبر المعرّف
p_ins = sub.add_parser("insights", help="Fetch insights JSON for a video id")
p_ins.add_argument("--id", required=True, help="Video ID returned from index step")

# summarize: يقرأ ملف JSON كـ نص (أو أي نص) ويلخّصه إلى Markdown
p_sum = sub.add_parser("summarize", help="Summarize transcript/JSON text into Markdown")
p_sum.add_argument("--transcript", required=True, help="Path to a JSON/text file")


def _save_json(obj: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

async def cmd_index(args) -> None:
    vi = VideoIndexer()
    resp = await vi.upload_video(name=args.name, video_url=args.url)
    _save_json(resp, Path("outputs/index_response.json"))
    print("✔ uploaded & indexing started. videoId:", resp.get("id"))

async def cmd_insights(args) -> None:
    vi = VideoIndexer()
    data = await vi.get_insights(video_id=args.id)
    out = Path(f"outputs/insights_{args.id}.json")
    _save_json(data, out)
    print("✔ insights saved:", out.as_posix())

def cmd_summarize(args) -> None:
    text = Path(args.transcript).read_text(encoding="utf-8")
    md = summarize_from_transcript(text)
    out = Path("outputs/summary.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print("✔ summary saved:", out.as_posix())

async def _amain() -> None:
    args = parser.parse_args()
    if args.cmd == "index":
        await cmd_index(args)
    elif args.cmd == "insights":
        await cmd_insights(args)
    elif args.cmd == "summarize":
        # ملخص لا يحتاج async
        cmd_summarize(args)

if __name__ == "__main__":
    asyncio.run(_amain())
