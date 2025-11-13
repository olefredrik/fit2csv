#!/usr/bin/env python3
import argparse
import csv
import sys
from pathlib import Path

try:
    import fitdecode
except ImportError:
    print(
        "Missing dependency: fitdecode.\n"
        "Install it with: pip install fitdecode",
        file=sys.stderr,
    )
    sys.exit(1)


def normalize(name: str) -> str:
    """Normalize field names to lowercase snake_case-ish."""
    return str(name).replace(" ", "_").replace("-", "_").lower()


def flat(val):
    """Flatten values so they can be written safely to CSV."""
    if isinstance(val, (bytes, bytearray)):
        return val.hex()
    if isinstance(val, (list, tuple)):
        return ";".join(map(str, val))
    return val


def gather_rows(fit_path: Path, kinds: set[str]) -> dict[str, list[dict]]:
    """Read a FIT file and collect rows per message kind."""
    out: dict[str, list[dict]] = {k: [] for k in kinds}

    with fitdecode.FitReader(str(fit_path), check_crc=False) as fr:
        for frame in fr:
            if isinstance(frame, getattr(fitdecode, "FitDataMessage", object)):
                kind = getattr(frame, "name", "")
                if kind in kinds:
                    row: dict[str, object] = {}
                    for f in getattr(frame, "fields", []):
                        n = getattr(f, "name", None)
                        if not n:
                            continue
                        row[normalize(n)] = flat(getattr(f, "value", None))
                    if row:
                        out[kind].append(row)

    return out


def write_csv(rows: list[dict], path: Path) -> bool:
    """Write a list of dict rows to CSV at the given path."""
    if not rows:
        return False

    headers: list[str] = []
    seen: set[str] = set()

    # Preserve first-seen order of headers
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                headers.append(k)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert multiple .fit files to .csv"
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Folder containing .fit files",
    )
    parser.add_argument(
        "--include",
        type=str,
        default="record",
        help="Comma-separated list of message types to export, e.g. record,lap,session",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output folder, defaults to ./csv_out inside the input folder",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce console output",
    )

    args = parser.parse_args()

    in_dir = Path(args.input_dir).expanduser().resolve()
    if not in_dir.is_dir():
        print(f"Input directory not found: {in_dir}", file=sys.stderr)
        sys.exit(2)

    # Map aliases to canonical message types
    types = {
        "record": "record",
        "lap": "lap",
        "laps": "lap",
        "session": "session",
    }

    requested: list[str] = []
    for t in [s.strip().lower() for s in args.include.split(",") if s.strip()]:
        if t in types:
            requested.append(types[t])
        else:
            print(f"Warning, unknown type: {t}", file=sys.stderr)

    if not requested:
        requested = ["record"]

    kinds = set(requested)

    out_dir = (
        Path(args.out).expanduser().resolve()
        if args.out
        else in_dir / "csv_out"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    fits = sorted(in_dir.glob("*.fit"))
    if not fits:
        print(f"No .fit files found in {in_dir}")
        sys.exit(0)

    total_written = 0

    for i, fp in enumerate(fits, start=1):
        if not args.quiet:
            print(f"[{i}/{len(fits)}] Reading {fp.name} ...")

        try:
            by_kind = gather_rows(fp, kinds)
        except Exception as e:  # noqa: BLE001 – we want to log any error
            print(f"Error while reading {fp.name}: {e}", file=sys.stderr)
            continue

        wrote_any = False
        stem = fp.stem

        for kind, rows in by_kind.items():
            target = out_dir / f"{stem}_{kind}.csv"
            if write_csv(rows, target):
                wrote_any = True
                total_written += 1
                if not args.quiet:
                    print(f" Wrote {target.name} with {len(rows)} rows")
            elif not args.quiet:
                print(f" No {kind} data in {fp.name}")

        if not wrote_any and not args.quiet:
            print(f" No data written for {fp.name}")

    print(f"Done.\nWrote {total_written} CSV files to {out_dir}")


if __name__ == "__main__":
    main()
