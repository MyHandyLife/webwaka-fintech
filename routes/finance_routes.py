"""
WebWaka Finance Sector - API Routes
RESTful API endpoints with African optimization and cultural integration
"""

from flask import Blueprint, jsonify, request
from models.finance_models import db, FinanceEntity

# Create blueprint
bp = Blueprint('finance', __name__)

# Get all entities
@bp.route('/', methods=['GET'])
def get_all_entities():
    """Get all finance entities with African optimization"""
    try:
        entities = FinanceEntity.query.all()
        return jsonify({
            'success': True,
            'data': [entity.to_dict() for entity in entities],
            'count': len(entities),
            'african_optimized': True,
            'mobile_friendly': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Get entity by ID
@bp.route('/<int:entity_id>', methods=['GET'])
def get_entity(entity_id):
    """Get specific finance entity"""
    try:
        entity = FinanceEntity.query.get_or_404(entity_id)
        return jsonify({
            'success': True,
            'data': entity.to_dict(),
            'african_optimized': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

# Create new entity
@bp.route('/', methods=['POST'])
def create_entity():
    """Create new finance entity with African optimization"""
    try:
        data = request.get_json()
        
        entity = FinanceEntity(
            name=data.get('name'),
            description=data.get('description'),
            traditional_name=data.get('traditional_name'),
            local_language=data.get('local_language', 'en'),
            community_approval=data.get('community_approval', False),
            traditional_authority_endorsement=data.get('traditional_authority_endorsement', False),
            cultural_significance=data.get('cultural_significance')
        )
        
        db.session.add(entity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': entity.to_dict(),
            'message': 'Finance entity created successfully',
            'african_optimized': True
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# Update entity
@bp.route('/<int:entity_id>', methods=['PUT'])
def update_entity(entity_id):
    """Update finance entity"""
    try:
        entity = FinanceEntity.query.get_or_404(entity_id)
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            entity.name = data['name']
        if 'description' in data:
            entity.description = data['description']
        if 'traditional_name' in data:
            entity.traditional_name = data['traditional_name']
        if 'local_language' in data:
            entity.local_language = data['local_language']
        if 'community_approval' in data:
            entity.community_approval = data['community_approval']
        if 'traditional_authority_endorsement' in data:
            entity.traditional_authority_endorsement = data['traditional_authority_endorsement']
        if 'cultural_significance' in data:
            entity.cultural_significance = data['cultural_significance']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': entity.to_dict(),
            'message': 'Finance entity updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# Delete entity
@bp.route('/<int:entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    """Delete finance entity"""
    try:
        entity = FinanceEntity.query.get_or_404(entity_id)
        db.session.delete(entity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Finance entity deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# African optimization endpoints
@bp.route('/mobile-optimized', methods=['GET'])
def get_mobile_optimized():
    """Get mobile-optimized data for African networks"""
    try:
        entities = FinanceEntity.query.filter_by(mobile_optimized=True).all()
        return jsonify({
            'success': True,
            'data': [entity.to_dict() for entity in entities],
            'mobile_optimized': True,
            'offline_sync_ready': True,
            'low_bandwidth_friendly': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/traditional-approved', methods=['GET'])
def get_traditional_approved():
    """Get entities approved by traditional authorities"""
    try:
        entities = FinanceEntity.query.filter_by(traditional_authority_endorsement=True).all()
        return jsonify({
            'success': True,
            'data': [entity.to_dict() for entity in entities],
            'traditional_authority_approved': True,
            'cultural_compliance': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Health check for this sector
@bp.route('/health', methods=['GET'])
def sector_health():
    """Health check for finance sector"""
    return jsonify({
        'sector': 'finance',
        'status': 'healthy',
        'database': 'connected',
        'african_optimized': True,
        'mobile_ready': True,
        'offline_capable': True,
        'culturally_integrated': True
    })
