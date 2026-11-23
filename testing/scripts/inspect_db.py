import sqlite3
from importlib.resources import files

def inspect_db():
    print("=== OSDAG_CORE DATABASE INSPECTION ===")
    try:
        db_path = files('osdag_core.data.ResourceFiles.Database').joinpath('Intg_osdag.sqlite')
        print(f"Path: {db_path}")
        print(f"Exists: {db_path.exists()}, Size: {db_path.stat().st_size} bytes")
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"Total Tables in osdag_core DB: {len(tables)}")
        for t in sorted(tables):
            try:
                cnt = cur.execute(f"SELECT count(*) FROM [{t}]").fetchone()[0]
                print(f"  - {t:<28}: {cnt:>6} rows")
            except Exception as e:
                print(f"  - {t:<28}: ERROR {e}")
        conn.close()
    except Exception as e:
        print(f"Error inspecting osdag_core DB: {e}")

    print("\n=== OSDAGBRIDGE LOCAL DATABASE INSPECTION ===")
    try:
        db_path2 = files('osdagbridge.core.data.ResourceFiles').joinpath('Intg_osdag.sqlite')
        print(f"Path: {db_path2}")
        print(f"Exists: {db_path2.exists()}, Size: {db_path2.stat().st_size} bytes")
        conn = sqlite3.connect(str(db_path2))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables2 = [r[0] for r in cur.fetchall()]
        print(f"Total Tables in osdagbridge local DB: {len(tables2)}")
        for t in sorted(tables2):
            try:
                cnt = cur.execute(f"SELECT count(*) FROM [{t}]").fetchone()[0]
                print(f"  - {t:<28}: {cnt:>6} rows")
            except Exception as e:
                print(f"  - {t:<28}: ERROR {e}")
        conn.close()
    except Exception as e:
        print(f"Error inspecting osdagbridge local DB: {e}")

if __name__ == "__main__":
    inspect_db()
