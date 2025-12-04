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
    Also rename image columns to 'image' for consistency.
    在應用啟動時自動將 TEXT 欄位升級為 LONGTEXT，並統一圖片欄位名稱。
    """
    
    # LONGTEXT migrations
    migrations = [
        ("projects", "description"),
        ("news", "excerpt"),
        ("news", "content"),
        ("about_us", "subtitle"),
        ("about_us", "description"),
    ]
    
    # Image column renames
    image_migrations = [
        ("projects", "thumbnail_url", "image"),
        ("news", "image_url", "image"),
    ]
    
    try:
        engine = create_engine(settings.database_url)
        
        with engine.connect() as connection:
            # Check if tables exist first
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            migrated = []
            skipped = []
            renamed = []
            
            # First, migrate TEXT to LONGTEXT
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
            
            # Then, rename image columns
            for table, old_col, new_col in image_migrations:
                if table not in existing_tables:
                    continue
                
                try:
                    # Check if old column exists and new column doesn't
                    result = connection.execute(text(f"""
                        SELECT COLUMN_NAME 
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = '{settings.DB_NAME}'
                        AND TABLE_NAME = '{table}'
                        AND COLUMN_NAME IN ('{old_col}', '{new_col}')
                    """))
                    
                    existing_cols = [row[0] for row in result.fetchall()]
                    
                    if old_col in existing_cols and new_col not in existing_cols:
                        connection.execute(text(
                            f"ALTER TABLE {table} CHANGE {old_col} {new_col} VARCHAR(500)"
                        ))
                        connection.commit()
                        renamed.append(f"{table}.{old_col} → {new_col}")
                        logger.info(f"✅ Renamed {table}.{old_col} to {new_col}")
                    
                except Exception as e:
                    logger.warning(f"⚠️  Could not rename {table}.{old_col}: {e}")
            
            if migrated:
                logger.info(f"🎉 LONGTEXT migration: {len(migrated)} columns upgraded")
                for col in migrated:
                    logger.info(f"   - {col}")
            
            if renamed:
                logger.info(f"🎉 Column rename: {len(renamed)} columns renamed")
                for col in renamed:
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

