"""
Automatic database migration utility.
自動資料庫遷移工具
"""

from sqlalchemy import create_engine, text, inspect
from app.config import settings
import logging

logger = logging.getLogger(__name__)


def auto_migrate_to_longtext():
    """
    Automatically migrate TEXT columns to LONGTEXT on startup.
    在應用啟動時自動將 TEXT 欄位升級為 LONGTEXT。
    """
    
    # Migration definitions
    migrations = [
        ("projects", "description"),
        ("news", "excerpt"),
        ("news", "content"),
        ("about_us", "subtitle"),
        ("about_us", "description"),
    ]
    
    try:
        engine = create_engine(settings.database_url)
        
        with engine.connect() as connection:
            # Check if tables exist first
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            migrated = []
            skipped = []
            
            for table, column in migrations:
                # Skip if table doesn't exist yet
                if table not in existing_tables:
                    continue
                
                try:
                    # Check current column type
                    result = connection.execute(text(f"""
                        SELECT COLUMN_TYPE 
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = '{settings.DB_NAME}'
                        AND TABLE_NAME = '{table}'
                        AND COLUMN_NAME = '{column}'
                    """))
                    
                    row = result.fetchone()
                    if row:
                        column_type = row[0].lower()
                        
                        # Migrate if it's TEXT (not LONGTEXT)
                        if column_type == 'text':
                            connection.execute(text(
                                f"ALTER TABLE {table} MODIFY {column} LONGTEXT"
                            ))
                            connection.commit()
                            migrated.append(f"{table}.{column}")
                            logger.info(f"✅ Migrated {table}.{column} to LONGTEXT")
                        elif 'longtext' in column_type:
                            skipped.append(f"{table}.{column}")
                        
                except Exception as e:
                    logger.warning(f"⚠️  Could not migrate {table}.{column}: {e}")
            
            if migrated:
                logger.info(f"🎉 Auto-migration completed: {len(migrated)} columns upgraded to LONGTEXT")
                for col in migrated:
                    logger.info(f"   - {col}")
            
            if skipped:
                logger.debug(f"Already LONGTEXT: {len(skipped)} columns")
                
        engine.dispose()
        return True
        
    except Exception as e:
        logger.error(f"❌ Auto-migration failed: {e}")
        return False


if __name__ == "__main__":
    # Can be run standalone for testing
    logging.basicConfig(level=logging.INFO)
    auto_migrate_to_longtext()

