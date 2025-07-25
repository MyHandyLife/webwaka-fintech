"""
WebWaka Finance Sector - Data Models
Comprehensive data models with African optimization and cultural integration
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
import json

db = SQLAlchemy()

class FinanceEntity(db.Model):
    """Main entity for finance sector with African optimization"""
    __tablename__ = 'finance_entities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # African optimization fields
    traditional_name = db.Column(db.String(200))
    local_language = db.Column(db.String(50))
    community_approval = db.Column(db.Boolean, default=False)
    traditional_authority_endorsement = db.Column(db.Boolean, default=False)
    cultural_significance = db.Column(db.Text)
    
    # Mobile optimization
    mobile_optimized = db.Column(db.Boolean, default=True)
    offline_sync_enabled = db.Column(db.Boolean, default=True)
    mobile_money_supported = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'traditional_name': self.traditional_name,
            'local_language': self.local_language,
            'community_approval': self.community_approval,
            'traditional_authority_endorsement': self.traditional_authority_endorsement,
            'cultural_significance': self.cultural_significance,
            'mobile_optimized': self.mobile_optimized,
            'offline_sync_enabled': self.offline_sync_enabled,
            'mobile_money_supported': self.mobile_money_supported,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Utility functions for African optimization
def format_for_mobile(data, language='en'):
    """Format data for mobile display with African optimization"""
    if language == 'ig':  # Igbo
        return {'sector': 'Finance', 'language': 'Igbo'}
    elif language == 'yo':  # Yoruba
        return {'sector': 'Finance', 'language': 'Yoruba'}
    elif language == 'ha':  # Hausa
        return {'sector': 'Finance', 'language': 'Hausa'}
    else:  # English default
        return {'sector': 'Finance', 'language': 'English'}
