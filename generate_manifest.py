import os
import json
import re
from collections import defaultdict
import argparse
from pathlib import Path
import sys

# --- 配置路径 ---
# 请确保这些路径相对于你运行脚本的位置是正确的
DATASETS_BASE_PATH = 'data/datasets'
OUTPUTS_BASE_PATH = 'data/outputs'
MANIFEST_OUTPUT_PATH = 'data/detailed_manifest.json'
# ---

# --- Helper Function (adapted from update_story_refs.py) ---
def get_story_data_and_cover(
    dataset_base_path: Path,
    dataset_name: str,
    story_id: str
) -> tuple[dict | None, str | None]:
    """
    Loads story data, finds reference images for each character,
    and determines the cover image path.

    Args:
        dataset_base_path: Base path containing dataset folders.
        dataset_name: Name of the dataset (e.g., 'WildStory').
        story_id: ID of the story (e.g., '01').

    Returns:
        A tuple containing:
        - The loaded story_data dictionary (with 'ref_images' potentially added/updated in memory).
        - The relative path to the cover image (e.g., 'data/datasets/WildStory/01/image/CharKey/00.jpg') or None.
    """
    story_dir = dataset_base_path / dataset_name / story_id
    story_json_path = story_dir / "story.json"
    image_base_dir = story_dir / "image"
    cover_image_path = None

    # Load story.json
    if not story_json_path.is_file():
        print(f"  Warning: story.json not found for {dataset_name}/{story_id}. Skipping story.", file=sys.stderr)
        return None, None
    try:
        with open(story_json_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
    except Exception as e:
        print(f"  Error reading {story_json_path}: {e}", file=sys.stderr)
        return None, None

    if "Characters" not in story_data or not isinstance(story_data["Characters"], dict) or not story_data["Characters"]:
        print(f"  Warning: No valid 'Characters' found in {story_json_path}. Cannot determine cover image.", file=sys.stderr)
        return story_data, None # Return data even if no cover found

    first_char_key = next(iter(story_data["Characters"]), None)
    if not first_char_key:
         print(f"  Warning: Characters dictionary is empty in {story_json_path}.", file=sys.stderr)
         return story_data, None
         
    first_char_info = story_data["Characters"][first_char_key]
    
    # Ensure character info is a dict
    if not isinstance(first_char_info, dict):
        print(f"  Warning: Character info for '{first_char_key}' is not a dictionary in {story_json_path}. Cannot determine cover image.", file=sys.stderr)
        return story_data, None

    # Find ref_images for the first character
    char_image_dir = image_base_dir / first_char_key
    ref_images_list = []
    if char_image_dir.is_dir():
        found_files = []
        img_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        for ext in img_extensions:
            found_files.extend(p.name for p in char_image_dir.glob(f'*{ext}'))
        ref_images_list = sorted(list(set(found_files)))

    # Store the found images back into the character data (in memory for cover path)
    first_char_info["ref_images"] = ref_images_list # Store for potential use, though not saved by this func

    # Determine cover image path
    if ref_images_list:
        # Construct relative path from the project root (assuming script runs from root or similar)
        # Path needs to match what HTML uses
        relative_image_path = Path("data") / "datasets" / dataset_name / story_id / "image" / first_char_key / ref_images_list[0]
        # Convert to forward slashes for web paths
        cover_image_path = relative_image_path.as_posix() 
        # print(f"    Cover image for {dataset_name}/{story_id}: {cover_image_path}")
    else:
        print(f"  Warning: No reference images found for first character '{first_char_key}' in {dataset_name}/{story_id}. No cover image set.", file=sys.stderr)

    # Note: This function doesn't update all characters' ref_images in the file,
    # only the first one in memory to find the cover. Run update_story_refs.py separately
    # if you need all story.json files fully updated with all ref_images lists.
    
    return story_data, cover_image_path

# --- Main Manifest Generation Logic ---
def generate_manifest(datasets_path: Path, outputs_path: Path, output_manifest_path: Path):
    """
    Generates the detailed_manifest.json by scanning datasets and outputs directories.
    """
    print("Starting manifest generation...")
    manifest = {
        "stories": [],
        "outputs": defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))))
        # outputs[method][mode][dataset][language][story_id] = {ts1: [shots], ts2: [shots], ...}
    }

    # --- 1. Scan Datasets ---
    print(f"\nScanning Datasets path: {datasets_path}")
    if not datasets_path.is_dir():
        print(f"Error: Datasets path '{datasets_path}' not found.", file=sys.stderr)
        sys.exit(1)

    for dataset_dir in datasets_path.iterdir():
        if not dataset_dir.is_dir():
            continue
        dataset_name = dataset_dir.name
        print(f"- Found Dataset: {dataset_name}")
        for story_dir in dataset_dir.iterdir():
            if not story_dir.is_dir():
                continue
            story_id = story_dir.name
            
            # Get story data (in memory) and cover image path
            story_data, cover_path = get_story_data_and_cover(datasets_path, dataset_name, story_id)

            if story_data: # Even if cover_path is None, add the story
                 # Try to get a more descriptive name if available in story.json
                 story_name_en = story_data.get("Story_name", {}).get("en") # Example key, adjust if needed
                 story_name_ch = story_data.get("Story_name", {}).get("ch") # Example key, adjust if needed
                 display_name = story_name_en or story_name_ch or f"{dataset_name} {story_id}" # Fallback name

                 manifest["stories"].append({
                     "id": story_id,
                     "dataset_base": dataset_name, # Keep base name here
                     "name": display_name,
                     "story_type_en": story_data.get("Story_type", {}).get("en"),
                     "story_type_ch": story_data.get("Story_type", {}).get("ch"),
                     "cover_image_path": cover_path # Will be null if not found
                 })

    # Sort stories for consistency
    manifest["stories"].sort(key=lambda x: (x["dataset_base"], x["id"]))
    print(f"Found {len(manifest['stories'])} stories.")


    # --- 2. Scan Outputs ---
    print(f"\nScanning Outputs path: {outputs_path}")
    if not outputs_path.is_dir():
        print(f"Warning: Outputs path '{outputs_path}' not found. Manifest will not contain output info.", file=sys.stderr)
    else:
        # 新的扫描结构:
        # outputs/{method}/{mode}/{dataset}/{language}/{story}/{timestamp}/{shot}
        for method_dir in outputs_path.iterdir():
            if not method_dir.is_dir(): continue
            method = method_dir.name
            print(f"- Found Method: {method}")
            
            # 检查方法目录下是否有多个模式
            has_multiple_modes = False
            mode_dirs = [d for d in method_dir.iterdir() if d.is_dir()]
            
            for mode_dir in mode_dirs:
                if not mode_dir.is_dir(): continue
                
                # 确定模式名称（如果没有多个模式，则默认为base）
                if len(mode_dirs) > 1:
                    has_multiple_modes = True
                    mode = mode_dir.name
                else:
                    mode = "base"  # 默认模式
                
                print(f"  - Mode: {mode}")
                
                # 后续目录路径
                dataset_path = mode_dir if has_multiple_modes else method_dir
                
                for dataset_dir in dataset_path.iterdir():
                    if not dataset_dir.is_dir(): continue
                    dataset_name = dataset_dir.name
                    print(f"    - Found Dataset: {dataset_name}")

                    for language_dir in dataset_dir.iterdir():
                        if not language_dir.is_dir(): continue
                        language = language_dir.name
                        print(f"      - Found Language: {language}")

                        for story_dir in language_dir.iterdir():
                            if not story_dir.is_dir(): continue
                            story_id = story_dir.name
                            # print(f"        - Found Story ID: {story_id}")  # 可能会很冗长

                            # 检查故事ID是否存在于我们扫描的数据集中
                            if not any(s['id'] == story_id and s['dataset_base'] == dataset_name for s in manifest['stories']):
                                print(f"        Warning: Output found for story '{dataset_name}/{story_id}' but this story wasn't found in datasets.", file=sys.stderr)
                                # 继续处理，不跳过

                            for timestamp_dir in story_dir.iterdir():
                                if not timestamp_dir.is_dir(): continue
                                timestamp = timestamp_dir.name
                                
                                # 获取该时间戳目录下的所有图像
                                shots = []
                                for shot_file in timestamp_dir.glob('shot_*.png'):
                                    shots.append(shot_file.name)
                                
                                if shots:  # 如果找到了图像
                                    shots.sort()  # 排序以保持一致性
                                    # print(f"          - Found Timestamp: {timestamp} with {len(shots)} shots")
                                    
                                    # 将shots列表存储到manifest中
                                    if manifest["outputs"][method][mode][dataset_name][language].get(story_id) is None:
                                        manifest["outputs"][method][mode][dataset_name][language][story_id] = {}
                                    
                                    manifest["outputs"][method][mode][dataset_name][language][story_id][timestamp] = shots
                            
                            # 按时间戳排序（例如，最新的在前）
                            if story_id in manifest["outputs"][method][mode][dataset_name][language]:
                                # 将字典转换为排序后的字典
                                sorted_timestamps = sorted(manifest["outputs"][method][mode][dataset_name][language][story_id].keys(), reverse=True)
                                sorted_dict = {}
                                for ts in sorted_timestamps:
                                    sorted_dict[ts] = manifest["outputs"][method][mode][dataset_name][language][story_id][ts]
                                manifest["outputs"][method][mode][dataset_name][language][story_id] = sorted_dict


    # --- 3. Save Manifest ---
    print(f"\nSaving manifest to: {output_manifest_path}")
    try:
        output_manifest_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        
        # 将defaultdict转换为普通dict
        manifest_json = {
            "stories": manifest["stories"],
            "outputs": {}
        }
        
        for method, modes in manifest["outputs"].items():
            manifest_json["outputs"][method] = {}
            for mode, datasets in modes.items():
                manifest_json["outputs"][method][mode] = {}
                for dataset, languages in datasets.items():
                    manifest_json["outputs"][method][mode][dataset] = {}
                    for language, stories in languages.items():
                        manifest_json["outputs"][method][mode][dataset][language] = {}
                        for story_id, timestamps in stories.items():
                            manifest_json["outputs"][method][mode][dataset][language][story_id] = timestamps
        
        with open(output_manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_json, f, indent=4, ensure_ascii=False)
        print("Manifest generation successful.")
    except Exception as e:
        print(f"Error: Could not write manifest file to {output_manifest_path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate detailed_manifest.json for the Storytelling Benchmark.")
    # Use defaults relative to CWD assuming standard project structure
    default_data_path = Path.cwd() / "data" 
    parser.add_argument("--datasets_path", default=str(default_data_path / "datasets"),
                        help="Path to the base directory containing dataset folders.")
    parser.add_argument("--outputs_path", default=str(default_data_path / "outputs"),
                        help="Path to the base directory containing output folders.")
    parser.add_argument("--output_manifest", default=str(default_data_path / "detailed_manifest.json"),
                        help="Path to save the generated manifest file.")

    args = parser.parse_args()

    datasets_p = Path(args.datasets_path)
    outputs_p = Path(args.outputs_path)
    output_manifest_p = Path(args.output_manifest)

    generate_manifest(datasets_p, outputs_p, output_manifest_p)

    print("\nScript finished.")