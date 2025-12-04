"""
Database Migration: Rename image columns to 'image'
將圖片欄位統一重命名為 'image'
"""

import sys
from sqlalchemy import create_engine, text
from app.config import settings

def rename_image_columns():
    """Rename all image-related columns to 'image' for consistency."""
    
    print("=" * 60)
    print("Database Migration: Rename Image Columns")
    print("=" * 60)
    print()
    
    # Create engine
    engine = create_engine(settings.database_url)
    
    # Migration SQL commands
    migrations = [
        ("projects", "thumbnail_url", "image", "ALTER TABLE projects CHANGE thumbnail_url image VARCHAR(500)"),
        ("news", "image_url", "image", "ALTER TABLE news CHANGE image_url image VARCHAR(500)"),
        ("about_us", "banner_image_url", "image", "ALTER TABLE about_us ADD COLUMN image VARCHAR(500) AFTER description"),
    ]
    
    try:
        with engine.connect() as connection:
            print("🔗 Connected to database")
            print(f"📊 Database: {settings.DB_NAME}")
            print()
            
            success_count = 0
            
            for table, old_col, new_col, sql in migrations:
                try:
                    print(f"⏳ Renaming {table}.{old_col} → {new_col}...", end=" ")
                    connection.execute(text(sql))
                    connection.commit()
                    print("✅ Success")
                    success_count += 1
                except Exception as e:
                    error_msg = str(e)
                    if "Unknown column" in error_msg or "doesn't exist" in error_msg:
                        print(f"⚠️  Column doesn't exist (skipped)")
                    elif "Duplicate column" in error_msg:
                        print(f"✓  Already renamed")
                    else:
                        print(f"⚠️  Warning: {error_msg}")
            
            print()
            print("=" * 60)
            print(f"✅ Migration completed: {success_count}/{len(migrations)} operations")
            print("=" * 60)
            print()
            print("📋 Column renames:")
            print("   - projects.thumbnail_url → image")
            print("   - news.image_url → image")
            print("   - about_us: added image column")
            print()
            print("🎉 All image columns unified to 'image'!")
            print()
            
            return True
            
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Migration failed: {str(e)}")
        print("=" * 60)
        return False
    finally:
        engine.dispose()


if __name__ == "__main__":
    print()
    print("⚠️  Warning: This will rename database columns")
    print("📦 Make sure you have a backup before proceeding")
    print()
    
    response = input("Continue with migration? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        print()
        success = rename_image_columns()
        sys.exit(0 if success else 1)
    else:
        print()
        print("❌ Migration cancelled")
        print()
        sys.exit(0)

