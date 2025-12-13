# Add Pronunciations Script

This script automatically fetches US IPA (International Phonetic Alphabet) pronunciations for vocabulary words and adds them to the `all-episodes-mapped.json` file.

## Features

- ✅ Fetches pronunciations from the Free Dictionary API
- ✅ Prefers US pronunciations when available
- ✅ Skips words that already have pronunciations
- ✅ Dry-run mode by default (safe to test)
- ✅ Creates automatic backup before saving
- ✅ Rate limiting to avoid API throttling
- ✅ Detailed progress reporting

## Requirements

```bash
pip install requests
```

## Usage

### 1. Dry Run (Test Mode - Recommended First)

This will show what would be added without making any changes:

```bash
python add_pronunciations.py
```

### 2. Live Mode (Actually Update the File)

Once you're happy with the dry run results:

```bash
python add_pronunciations.py --live
```

### 3. Custom Options

```bash
# Use a different JSON file
python add_pronunciations.py --file path/to/your/file.json

# Adjust delay between API calls (in seconds)
python add_pronunciations.py --delay 1.0 --live

# Full example with all options
python add_pronunciations.py --live --delay 0.3 --file src/data/all-episodes-mapped.json
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--live` | Actually save changes (without this, it's dry-run) | `false` |
| `--delay` | Delay between API calls in seconds | `0.5` |
| `--file` | Path to JSON file | `src/data/all-episodes-mapped.json` |

## How It Works

1. **Loads the JSON file** containing all episodes and vocabulary
2. **For each vocabulary word:**
   - Checks if it already has a pronunciation (skips if yes)
   - Extracts the clean word (removes category info like "(phrase)")
   - Calls the Free Dictionary API
   - Looks for US pronunciation specifically
   - Falls back to any available pronunciation if US not found
3. **Adds pronunciation** to the vocabulary item
4. **Creates a backup** (`.json.backup`) before saving
5. **Saves the updated JSON** with pronunciations

## Example Output

```
============================================================
Adding pronunciations to: src/data/all-episodes-mapped.json
Mode: DRY RUN (no changes will be saved)
============================================================

📚 Episode 1: Conversation at a Coffee Shop

  🔍 Fetching pronunciation for 'Dare to say'...
  ✓ Found US pronunciation: /deər tə seɪ/
  
  🔍 Fetching pronunciation for 'Impression'...
  ✓ Found pronunciation: /ɪmˈpreʃ.ən/
  
  ⏭️  'Erudite' already has pronunciation

============================================================
SUMMARY
============================================================
Total vocabulary words: 150
Already had pronunciation: 0
Pronunciations added: 120
Failed to fetch: 30
============================================================
```

## API Information

This script uses the **Free Dictionary API**:
- **URL:** https://dictionaryapi.dev/
- **Free:** Yes, no API key required
- **Rate Limit:** Be respectful, use delays
- **Coverage:** English words and phrases

## Troubleshooting

### "No pronunciation found"
- The API doesn't have data for that word
- Try checking the word manually at https://dictionaryapi.dev/
- Some phrases or specialized terms may not be available

### "Connection error"
- Check your internet connection
- The API might be temporarily down
- Try increasing the `--delay` value

### "File not found"
- Make sure you're running the script from the project root
- Or specify the correct path with `--file`

## Notes

- **Backup:** A `.json.backup` file is created before any changes
- **Idempotent:** Safe to run multiple times (skips existing pronunciations)
- **Rate Limiting:** Default 0.5s delay between requests (adjustable)
- **Format:** Pronunciations are stored without forward slashes (added in UI)

## Example JSON Before/After

**Before:**
```json
{
  "word": "Impression (common noun, singular)",
  "definition": "The feelings one has after a specific event"
}
```

**After:**
```json
{
  "word": "Impression (common noun, singular)",
  "definition": "The feelings one has after a specific event",
  "pronunciation": "ɪmˈpreʃ.ən"
}
```
