from __future__ import annotations
import json
from pathlib import Path

def build_manifest(dataset_root: Path, output_path: Path) -> None:
    stories = []
    if dataset_root.is_dir():
        for story_dir in sorted(dataset_root.iterdir()):
            if not story_dir.is_dir():
                continue
            story_id = story_dir.name
            story_json_path = story_dir / 'story.json'
            if not story_json_path.is_file():
                continue
            try:
                with open(story_json_path, 'r', encoding='utf-8-sig') as f:
                    story_json = json.load(f)
            except Exception:
                continue
            story_name = story_json.get('Story_name', {})
            display_name = story_name.get('en') or story_name.get('ch') or f'Story {story_id}'
            story_type = story_json.get('Story_type', {})
            image_dir = story_dir / 'image'
            characters = story_json.get('Characters', {})
            en_chars = []
            zh_chars = []
            cover_path = None
            if image_dir.is_dir():
                for char_folder in sorted(image_dir.iterdir()):
                    if not char_folder.is_dir():
                        continue
                    files = sorted([
                        p.name for p in char_folder.iterdir()
                        if p.is_file() and p.suffix.lower() in {'.avif', '.jpg', '.jpeg', '.png', '.webp'}
                    ])
                    if files and not cover_path:
                        cover_path = f'dataset_lite_avif/{story_id}/image/{char_folder.name}/{files[0]}'
                    char_info = characters.get(char_folder.name, {})
                    en_name = char_info.get('name_en') or char_folder.name
                    zh_name = (
                        char_info.get('name_ch')
                        or char_info.get('name_cn')
                        or char_info.get('name_zh')
                        or char_info.get('name_en')
                        or char_folder.name
                    )
                    en_chars.append({'name': en_name, 'ref_image_count': len(files)})
                    zh_chars.append({'name': zh_name, 'ref_image_count': len(files)})
            stories.append({
                'id': story_id,
                'dataset_base': 'lite',
                'name': display_name,
                'story_type_en': story_type.get('en'),
                'story_type_ch': story_type.get('ch'),
                'cover_image_path': cover_path,
                'characters_en': en_chars,
                'characters_ch': zh_chars,
            })
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as f:
        json.dump({'stories': stories}, f, ensure_ascii=False, indent=2)

def build_outputs_index(outputs_root: Path, output_path: Path) -> None:
    structure_map: dict[str, str] = {}
    index: dict[str, dict] = {}
    if outputs_root.is_dir():
        for model_dir in sorted(outputs_root.iterdir()):
            if not model_dir.is_dir():
                continue
            model_name = model_dir.name
            model_entry = {}
            model_structure: str | None = None
            for mode_dir in sorted(model_dir.iterdir()):
                if not mode_dir.is_dir():
                    continue
                mode_name = mode_dir.name
                mode_entry = {}
                for lang_dir in sorted(mode_dir.iterdir()):
                    if not lang_dir.is_dir():
                        continue
                    lang_name = lang_dir.name
                    timestamps = []
                    for ts_dir in sorted(lang_dir.iterdir()):
                        if not ts_dir.is_dir():
                            continue
                        timestamps.append(ts_dir.name)
                        if model_structure is None:
                            if (ts_dir / 'shots').is_dir():
                                model_structure = 'shots-first'
                            else:
                                has_story_dirs = any(child.is_dir() for child in ts_dir.iterdir())
                                model_structure = 'stories-first' if has_story_dirs else 'shots-first'
                    if timestamps:
                        mode_entry[lang_name] = timestamps
                if mode_entry:
                    model_entry[mode_name] = mode_entry
            if model_entry:
                index[model_name] = model_entry
                structure_map[model_name] = model_structure or 'stories-first'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as f:
        json.dump({'root': 'outputs_lite_avif', 'structure': structure_map, 'index': index}, f, ensure_ascii=False, indent=2)

def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    build_manifest(project_root / 'public' / 'dataset_lite_avif', project_root / 'src' / 'data' / 'detailed_manifest.json')
    build_outputs_index(project_root / 'public' / 'outputs_lite_avif', project_root / 'src' / 'data' / 'outputs_index.json')

if __name__ == '__main__':
    main()
