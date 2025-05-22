import json
import argparse
from pathlib import Path
import sys

def update_single_story_with_ref_images(
    dataset_base_path: Path,
    dataset_name: str,
    story_id: str,
    write_to_file: bool = True  # New parameter to control writing
) -> dict | None: # Returns updated story_data or None on failure
    """
    Scans character image directories for a specific story, finds reference images,
    updates the corresponding story.json file with a 'ref_images' list.

    Args:
        dataset_base_path: The base path containing all dataset folders.
        dataset_name: The name of the dataset (e.g., 'WildStory').
        story_id: The ID of the story (e.g., '01').
        write_to_file: If True, writes changes back to story.json.

    Returns:
        The updated story_data dictionary if successful, otherwise None.
    """
    story_dir = dataset_base_path / dataset_name / story_id
    story_json_path = story_dir / "story.json"
    image_base_dir = story_dir / "image" # HTML uses 'image', not 'images'

    print(f"Processing story: {dataset_name}/{story_id}")

    # --- Load story.json ---
    if not story_json_path.is_file():
        print(f"Error: story.json not found at {story_json_path}", file=sys.stderr)
        return None

    try:
        with open(story_json_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from {story_json_path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: Could not read {story_json_path}: {e}", file=sys.stderr)
        return None

    if "Characters" not in story_data or not isinstance(story_data["Characters"], dict):
        print(f"Error: 'Characters' key missing or not a dictionary in {story_json_path}", file=sys.stderr)
        return None

    initial_story_data_str = json.dumps(story_data) # For checking if updated

    # --- Iterate through characters ---
    for char_key, char_info in story_data["Characters"].items():
        # Ensure char_info is a dictionary, sometimes it might be just a string if JSON is malformed
        if not isinstance(char_info, dict):
            print(f"  Warning: Character info for '{char_key}' is not a dictionary. Skipping.", file=sys.stderr)
            continue

        char_image_dir = image_base_dir / char_key
        # print(f"  Checking character '{char_key}' in dir: {char_image_dir}")

        ref_images_list = []
        if char_image_dir.is_dir():
            found_files = []
            img_extensions = ['.jpg', '.jpeg', '.png', '.webp'] # Common image extensions
            for ext in img_extensions:
                # Using glob for direct children, rglob for recursive (less likely needed here)
                found_files.extend(p.name for p in char_image_dir.glob(f'*{ext}'))
            
            # Sort filenames. If they are like '00.jpg', '01.jpg', '10.jpg', default sort works.
            # For more complex numeric sort:
            # ref_images_list = sorted(list(set(found_files)), key=lambda x: int(Path(x).stem) if Path(x).stem.isdigit() else float('inf'))
            ref_images_list = sorted(list(set(found_files))) 
            # print(f"    Found reference images: {ref_images_list}")
        # else:
            # print(f"    Warning: Image directory not found for character '{char_key}' at {char_image_dir}")

        # Update the character info in the dictionary
        char_info["ref_images"] = ref_images_list # Always assign, even if empty

    # --- Save updated story.json (only if changes were made and write_to_file is True) ---
    updated_story_data_str = json.dumps(story_data)
    if updated_story_data_str != initial_story_data_str:
        if write_to_file:
            try:
                with open(story_json_path, 'w', encoding='utf-8') as f:
                    json.dump(story_data, f, indent=4, ensure_ascii=False)
                print(f"  Successfully updated {story_json_path} with ref_images.")
            except Exception as e:
                print(f"  Error: Could not write updated data to {story_json_path}: {e}", file=sys.stderr)
                # Even if write fails, we might still want to return the data if it was modified in memory
        else:
            print(f"  Story data for {story_json_path} was modified in memory (ref_images updated).")
    else:
        print(f"  No updates needed for ref_images in {story_json_path}.")
    
    return story_data # Return the (potentially) modified story_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update a single story.json file with character reference image lists. "
                    "This script is primarily for updating one story.json. "
                    "Use generate_detailed_manifest.py for batch processing and manifest generation."
    )
    parser.add_argument("--dataset", default="WildStory", help="Name of the dataset folder (e.g., WildStory)")
    parser.add_argument("--story_id", default="01", help="ID of the story folder (e.g., 01)")
    parser.add_argument("--base_path", default=str(Path.cwd() / "data" / "datasets"),
                        help="Base path to the datasets directory (default: ./data/datasets relative to CWD)")
    parser.add_argument("--no_write", action="store_true",
                        help="If set, performs a dry run and does not write changes to story.json.")

    args = parser.parse_args()
    base_path = Path(args.base_path)
    for id in range(1, 81):
        args.story_id = str(id).zfill(2)
        base_path = Path(args.base_path)
        if not base_path.is_dir():
            print(f"Error: Base path '{base_path}' does not exist or is not a directory.", file=sys.stderr)
            sys.exit(1)

        updated_data = update_single_story_with_ref_images(
            base_path,
            args.dataset,
            args.story_id,
            write_to_file=not args.no_write
        )

        if updated_data:
            # If you want to see the output even if not writing to file:
            # print("\nFinal story_data (in memory):")
            # print(json.dumps(updated_data, indent=4, ensure_ascii=False))
            print("\nScript finished successfully.")
        else:
            print("\nScript finished with errors.")
            sys.exit(1)