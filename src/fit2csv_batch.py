#!/usr/bin/env python3
import argparse, csv, sys
from pathlib import Path
try:
    import fitdecode
except ImportError:
    print("Mangler fitdecode. Installer: pip install fitdecode", file=sys.stderr)
    sys.exit(1)

def normalize(name: str) -> str:
    return str(name).replace(" ", "_").replace("-", "_").lower()

def flat(val):
    if isinstance(val, (bytes, bytearray)):
        return val.hex()
    if isinstance(val, (list, tuple)):
        return ";".join(map(str, val))
    return val

def gather_rows(fit_path: Path, kinds: set):
    out = {k: [] for k in kinds}
    with fitdecode.FitReader(str(fit_path), check_crc=False) as fr:
        for frame in fr:
            if isinstance(frame, getattr(fitdecode, "FitDataMessage", object)):
                kind = getattr(frame, "name", "")
                if kind in kinds:
                    row = {}
                    for f in getattr(frame, "fields", []):
                        n = getattr(f, "name", None)
                        if not n:
                            continue
                        row[normalize(n)] = flat(getattr(f, "value", None))
                    if row:
                        out[kind].append(row)
    return out

def write_csv(rows, path: Path):
    if not rows:
        return False
    headers, seen = [], set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k); headers.append(k)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader(); w.writerows(rows)
    return True

def main():
    p = argparse.ArgumentParser(description="Konverter mange .fit til .csv")
    p.add_argument("input_dir", type=str, help="Mappe med .fit filer")
    p.add_argument("--include", type=str, default="record",
                   help="Komma separert liste: record,laps,session")
    p.add_argument("--out", type=str, default=None,
                   help="Output mappe, standard <input_dir>/csv_out")
    p.add_argument("--quiet", action="store_true", help="Mindre utskrift")
    args = p.parse_args()

    in_dir = Path(args.input_dir).expanduser().resolve()
    if not in_dir.is_dir():
        print(f"Fant ikke mappe: {in_dir}", file=sys.stderr); sys.exit(2)

    types = {"record": "record", "lap": "lap", "laps": "lap", "session": "session"}
    req = []
    for t in [s.strip().lower() for s in args.include.split(",") if s.strip()]:
        if t in types: req.append(types[t])
        else: print(f"Advarsel, ukjent type: {t}", file=sys.stderr)
    if not req: req = ["record"]
    kinds = set(req)

    out_dir = Path(args.out).expanduser().resolve() if args.out else in_dir / "csv_out"
    out_dir.mkdir(parents=True, exist_ok=True)

    fits = sorted(in_dir.glob("*.fit"))
    if not fits:
        print(f"Ingen .fit i {in_dir}"); sys.exit(0)

    total_written = 0
    for i, fp in enumerate(fits, 1):
        if not args.quiet: print(f"[{i}/{len(fits)}] Leser {fp.name} ...")
        try:
            by_kind = gather_rows(fp, kinds)
        except Exception as e:
            print(f"Feil ved lesing av {fp.name}: {e}", file=sys.stderr)
            continue
        wrote = False
        stem = fp.stem
        for k, rows in by_kind.items():
            target = out_dir / f"{stem}_{k}.csv"
            if write_csv(rows, target):
                wrote = True; total_written += 1
                if not args.quiet: print(f"  Skrev {target.name} med {len(rows)} rader")
            elif not args.quiet:
                print(f"  Ingen {k} data i {fp.name}")
        if not wrote and not args.quiet:
            print(f"  Ingen data skrevet for {fp.name}")
    print(f"Ferdig. Skrev {total_written} CSV filer til {out_dir}")

if __name__ == "__main__":
    main()
