import sys
from pathlib import Path

# Add project root to path
sys.path.append("f:/self-healing-llm")

def check_file(path_str):
    p = Path(path_str)
    if p.exists():
        print(f"[OK] Found {path_str}")
        return True
    else:
        print(f"[FAIL] Missing {path_str}")
        return False

def check_import():
    try:
        from app.core.interfaces import InteractionRequest, AbstractGenerator
        print("[OK] Successfully imported app.core.interfaces")
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error during import: {e}")
        return False

def main():
    print("--- Phase 0 Verification ---")
    files = [
        "f:/self-healing-llm/docs/vision.md",
        "f:/self-healing-llm/app/core/interfaces.py",
        "f:/self-healing-llm/docs/state_machine.md"
    ]
    
    all_files = all(check_file(f) for f in files)
    all_imports = check_import()
    
    if all_files and all_imports:
        print("\nPhase 0 COMPLETE: Success")
        sys.exit(0)
    else:
        print("\nPhase 0 INCOMPLETE: Failures detected")
        sys.exit(1)

if __name__ == "__main__":
    main()
