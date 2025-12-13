"""
Database Migration Script: Create feedback table
創建 feedback 表的數據庫遷移腳本
"""

import sys
from sqlalchemy import create_engine, text, inspect
from app.config import settings


def migrate_add_feedback():
    """Create feedback table if it doesn't exist."""
    
    print("=" * 60)
    print("Database Migration: Create feedback table")
    print("數據庫遷移：創建 feedback 表")
    print("=" * 60)
    print()
    
    # Create engine
    engine = create_engine(settings.database_url)
    
    # SQL to create feedback table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL,
        subject VARCHAR(255) NULL,
        message TEXT NOT NULL,
        is_read BOOLEAN DEFAULT FALSE NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_email (email),
        INDEX idx_is_read (is_read),
        INDEX idx_created_at (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    try:
        with engine.connect() as connection:
            print("🔗 Connected to database")
            print(f"📊 Database: {settings.DB_NAME}")
            print()
            
            # Check if table already exists
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            if 'feedback' in existing_tables:
                print("⏭️  Table 'feedback' already exists, skipping creation...")
                print()
                
                # Show table structure
                print("📋 Current table structure:")
                result = connection.execute(text("DESCRIBE feedback"))
                rows = result.fetchall()
                print(f"{'Field':<20} {'Type':<30} {'Null':<10} {'Key':<10} {'Default':<15}")
                print("-" * 85)
                for row in rows:
                    print(f"{row[0]:<20} {row[1]:<30} {row[2]:<10} {row[3]:<10} {str(row[4] or ''):<15}")
                print()
                
                return True
            
            # Create table
            print("⏳ Creating feedback table...", end=" ")
            connection.execute(text(create_table_sql))
            connection.commit()
            print("✅ Success")
            print()
            
            # Verify table creation
            print("📋 Verification:")
            result = connection.execute(text("""
                SELECT 
                    TABLE_NAME as 'table',
                    TABLE_ROWS as 'rows',
                    CREATE_TIME as 'create_time'
                FROM 
                    INFORMATION_SCHEMA.TABLES
                WHERE 
                    TABLE_SCHEMA = :db_name
                    AND TABLE_NAME = 'feedback'
            """), {"db_name": settings.DB_NAME})
            
            row = result.fetchone()
            if row:
                print(f"   Table: {row[0]}")
                print(f"   Rows: {row[1]}")
                print(f"   Created: {row[2]}")
                print()
            
            # Show table structure
            print("📋 Table structure:")
            result = connection.execute(text("DESCRIBE feedback"))
            rows = result.fetchall()
            print(f"{'Field':<20} {'Type':<30} {'Null':<10} {'Key':<10} {'Default':<15}")
            print("-" * 85)
            for row in rows:
                print(f"{row[0]:<20} {row[1]:<30} {row[2]:<10} {row[3]:<10} {str(row[4] or ''):<15}")
            print()
            
            print("=" * 60)
            print("✅ Migration completed successfully!")
            print("=" * 60)
            print()
            print("📋 Feedback table created with the following fields:")
            print("   - id (INT, PRIMARY KEY, AUTO_INCREMENT)")
            print("   - name (VARCHAR(100), NOT NULL)")
            print("   - email (VARCHAR(255), NOT NULL)")
            print("   - subject (VARCHAR(255), NULLABLE)")
            print("   - message (TEXT, NOT NULL)")
            print("   - is_read (BOOLEAN, DEFAULT FALSE)")
            print("   - created_at (DATETIME, AUTO)")
            print("   - updated_at (DATETIME, AUTO)")
            print()
            print("📊 Indexes created:")
            print("   - idx_email (email)")
            print("   - idx_is_read (is_read)")
            print("   - idx_created_at (created_at)")
            print()
            
            return True
            
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Migration failed: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False
    finally:
        engine.dispose()


if __name__ == "__main__":
    print()
    print("⚠️  Warning: This will create the feedback table in your database")
    print("📦 Make sure you have a backup before proceeding")
    print()
    print("This migration will:")
    print("  - Create 'feedback' table if it doesn't exist")
    print("  - Add indexes for performance (email, is_read, created_at)")
    print()
    
    response = input("Continue with migration? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        print()
        success = migrate_add_feedback()
        sys.exit(0 if success else 1)
    else:
        print()
        print("❌ Migration cancelled")
        print()
        sys.exit(0)
