
from app import app, db
from models import ImageAnalysis

def migrate_database():
    """Add missing columns to image_analysis table"""
    with app.app_context():
        # Check if columns exist and add them if they don't
        engine = db.engine
        inspector = db.inspect(engine)
        columns = inspector.get_columns('image_analysis')
        existing_columns = [col['name'] for col in columns]
        
        # Create a list of columns to add
        columns_to_add = {
            'image_width': 'INTEGER',
            'image_height': 'INTEGER',
            'image_format': 'VARCHAR(16)',
            'image_size_bytes': 'INTEGER',
            'image_type': 'VARCHAR(32)',
            'character_traits': 'JSONB',
            'character_role': 'VARCHAR(32)',
            'plot_lines': 'JSONB',
            'scene_type': 'VARCHAR(64)',
            'setting': 'VARCHAR(255)',
            'setting_description': 'TEXT',
            'story_fit': 'VARCHAR(255)',
            'dramatic_moments': 'JSONB'
        }
        
        # Check if we need to fix any inconsistent column names
        inconsistent_columns = {
            'sceneType': 'scene_type',
            'storyFit': 'story_fit',
            'dramaticMoments': 'dramatic_moments'
        }
        
        # Add logic to rename columns if they exist with the old camelCase names
        with engine.connect() as conn:
            for old_name, new_name in inconsistent_columns.items():
                if old_name in existing_columns and new_name not in existing_columns:
                    print(f"Renaming column {old_name} to {new_name}")
                    conn.execute(db.text(f"ALTER TABLE image_analysis RENAME COLUMN {old_name} TO {new_name}"))
            conn.commit()
        
        # Add each missing column
        with engine.connect() as conn:
            for col_name, col_type in columns_to_add.items():
                if col_name not in existing_columns:
                    print(f"Adding column {col_name} to image_analysis table")
                    conn.execute(db.text(f"ALTER TABLE image_analysis ADD COLUMN {col_name} {col_type}"))
            conn.commit()
        
        print("Database migration completed successfully")

if __name__ == "__main__":
    migrate_database()
