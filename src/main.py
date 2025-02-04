"""Main runner for UVSIM."""

from src.boot import Bootstrapper


def main():
    """Initialize CPU and run Test1.txt."""
    boot = Bootstrapper()
    boot.load_program("Test1.txt")
    boot.run()


if __name__ == "__main__":
    main()
