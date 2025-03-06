from datetime import datetime
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

# Association table for many-to-many relationship between stories and images
story_images = db.Table('story_images',
    db.Column('story_id', db.Integer, db.ForeignKey('story_generation.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image_analysis.id'), primary_key=True)
)

class StoryGeneration(db.Model):
    """Model for storing generated story segments and their choices"""
    id = db.Column(db.Integer, primary_key=True)
    primary_conflict = db.Column(db.String(255))
    setting = db.Column(db.String(255))
    narrative_style = db.Column(db.String(255))
    mood = db.Column(db.String(255))
    generated_story = db.Column(JSONB)  # Stores the story text and choices
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with ImageAnalysis
    images = db.relationship('ImageAnalysis', secondary=story_images,
                           backref=db.backref('stories', lazy='dynamic'))

class ImageAnalysis(db.Model):
    """Model for storing analyzed character images"""
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(1024), nullable=False)
    analysis_result = db.Column(JSONB)  # Stores name, style, story
    character_traits = db.Column(JSONB)  # Array of character traits
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AIInstruction(db.Model):
    """Model for storing AI generation parameters and instructions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    prompt_template = db.Column(db.Text, nullable=False)
    parameters = db.Column(JSONB)  # Stores additional parameters
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HashtagCollection(db.Model):
    """Model for storing hashtag collections (for debugging/Instagram features)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    hashtags = db.Column(JSONB)  # Array of hashtags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
