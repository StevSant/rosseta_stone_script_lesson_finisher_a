import sys


def main():
    # Create .env interactively if missing, BEFORE importing anything that
    # reads settings, so pydantic finds the file on first load.
    from rosseta_stone_script_a.infrastructure.core import ensure_env_exists

    ensure_env_exists()

    from rosseta_stone_script_a.presentation.cli import main_cli

    main_cli()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"\nError: {exc}")
    finally:
        if getattr(sys, "frozen", False):
            input("\nPresiona Enter para cerrar...")
