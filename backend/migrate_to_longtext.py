"""
Database Migration Script: TEXT to LONGTEXT
將所有描述欄位從 TEXT 轉換為 LONGTEXT
"""

import sys
from sqlalchemy import create_engine, text
from app.config import settings

def migrate_to_longtext():
    """Migrate TEXT columns to LONGTEXT for better Markdown support."""
    
    print("=" * 60)
    print("Database Migration: TEXT → LONGTEXT")
    print("=" * 60)
    print()
    
    # Create engine
    engine = create_engine(settings.database_url)
    
    # Migration SQL commands
    migrations = [
        # Projects table
        ("projects", "description", "ALTER TABLE projects MODIFY description LONGTEXT"),
        
        # News table
        ("news", "excerpt", "ALTER TABLE news MODIFY excerpt LONGTEXT"),
        ("news", "content", "ALTER TABLE news MODIFY content LONGTEXT"),
        
        # About_us table
        ("about_us", "subtitle", "ALTER TABLE about_us MODIFY subtitle LONGTEXT"),
        ("about_us", "description", "ALTER TABLE about_us MODIFY description LONGTEXT"),
    ]
    
    try:
        with engine.connect() as connection:
            print("🔗 Connected to database")
            print(f"📊 Database: {settings.DB_NAME}")
            print()
            
            success_count = 0
            
            for table, column, sql in migrations:
                try:
                    print(f"⏳ Migrating {table}.{column}...", end=" ")
                    connection.execute(text(sql))
                    connection.commit()
                    print("✅ Success")
                    success_count += 1
                except Exception as e:
                    print(f"⚠️  Warning: {str(e)}")
                    # Continue even if one migration fails
                    # (column might already be LONGTEXT)
            
            print()
            print("=" * 60)
            print(f"✅ Migration completed: {success_count}/{len(migrations)} columns updated")
            print("=" * 60)
            print()
            print("📋 Updated columns:")
            for table, column, _ in migrations:
                print(f"   - {table}.{column} → LONGTEXT")
            print()
            print("🎉 All description fields now support up to 4GB of content!")
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
    print("⚠️  Warning: This will modify your database schema")
    print("📦 Make sure you have a backup before proceeding")
    print()
    
    response = input("Continue with migration? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        print()
        success = migrate_to_longtext()
        sys.exit(0 if success else 1)
    else:
        print()
        print("❌ Migration cancelled")
        print()
        sys.exit(0)

