"""
Database Migration Script: Add views column
為 about_us、news、projects 表添加 views 欄位
"""

import sys
from sqlalchemy import create_engine, text, inspect
from app.config import settings


def migrate_add_views():
    """Add views column to about_us, news, and projects tables."""
    
    print("=" * 60)
    print("Database Migration: Add views column")
    print("為數據庫添加 views 欄位")
    print("=" * 60)
    print()
    
    # Create engine
    engine = create_engine(settings.database_url)
    
    # Migration definitions
    migrations = [
        {
            "table": "about_us",
            "column": "views",
            "sql": "ALTER TABLE about_us ADD COLUMN views INT DEFAULT 0 NOT NULL AFTER contact_email",
            "after": "contact_email"
        },
        {
            "table": "news",
            "column": "views",
            "sql": "ALTER TABLE news ADD COLUMN views INT DEFAULT 0 NOT NULL AFTER author",
            "after": "author"
        },
        {
            "table": "projects",
            "column": "views",
            "sql": "ALTER TABLE projects ADD COLUMN views INT DEFAULT 0 NOT NULL AFTER link",
            "after": "link"
        }
    ]
    
    try:
        with engine.connect() as connection:
            print("🔗 Connected to database")
            print(f"📊 Database: {settings.DB_NAME}")
            print()
            
            # Check if tables exist
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            success_count = 0
            skipped_count = 0
            
            for migration in migrations:
                table = migration["table"]
                column = migration["column"]
                
                # Skip if table doesn't exist
                if table not in existing_tables:
                    print(f"⚠️  Table '{table}' does not exist, skipping...")
                    continue
                
                try:
                    # Check if column already exists
                    result = connection.execute(text(f"""
                        SELECT COLUMN_NAME 
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = '{settings.DB_NAME}'
                        AND TABLE_NAME = '{table}'
                        AND COLUMN_NAME = '{column}'
                    """))
                    
                    if result.fetchone():
                        print(f"⏭️  Column {table}.{column} already exists, skipping...")
                        skipped_count += 1
                        continue
                    
                    # Execute migration
                    print(f"⏳ Adding {table}.{column}...", end=" ")
                    connection.execute(text(migration["sql"]))
                    connection.commit()
                    print("✅ Success")
                    success_count += 1
                    
                except Exception as e:
                    print(f"❌ Failed: {str(e)}")
                    # Continue with other migrations even if one fails
            
            print()
            print("=" * 60)
            print(f"✅ Migration completed:")
            print(f"   - Successfully added: {success_count} columns")
            print(f"   - Already exists (skipped): {skipped_count} columns")
            print("=" * 60)
            print()
            
            # Verify results
            if success_count > 0:
                print("📋 Verification:")
                result = connection.execute(text("""
                    SELECT 
                        TABLE_NAME as 'table',
                        COLUMN_NAME as 'column',
                        COLUMN_TYPE as 'type',
                        COLUMN_DEFAULT as 'default',
                        IS_NULLABLE as 'nullable'
                    FROM 
                        INFORMATION_SCHEMA.COLUMNS
                    WHERE 
                        TABLE_SCHEMA = :db_name
                        AND COLUMN_NAME = 'views'
                    ORDER BY TABLE_NAME
                """), {"db_name": settings.DB_NAME})
                
                rows = result.fetchall()
                if rows:
                    print(f"{'Table':<15} {'Column':<10} {'Type':<15} {'Default':<10} {'Nullable':<10}")
                    print("-" * 60)
                    for row in rows:
                        print(f"{row[0]:<15} {row[1]:<10} {row[2]:<15} {str(row[3]):<10} {row[4]:<10}")
                print()
            
            print("🎉 Views column migration completed!")
            print()
            
            return success_count > 0 or skipped_count > 0
            
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
    print("This migration will:")
    print("  - Add 'views' column (INT DEFAULT 0 NOT NULL) to:")
    print("    • about_us table")
    print("    • news table")
    print("    • projects table")
    print()
    
    response = input("Continue with migration? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        print()
        success = migrate_add_views()
        sys.exit(0 if success else 1)
    else:
        print()
        print("❌ Migration cancelled")
        print()
        sys.exit(0)
