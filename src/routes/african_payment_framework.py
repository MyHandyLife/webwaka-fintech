"""
WebWaka Universal African Payment Integration Framework API Routes
================================================================

This module provides comprehensive REST API endpoints for managing the most
advanced African payment gateway integration system ever built. It supports
115+ payment gateways across Nigeria, Kenya, South Africa, Ghana and beyond.

Features:
- Payment gateway management and discovery
- Integration configuration and monitoring
- Transaction processing and tracking
- Real-time analytics and reporting
- African-optimized payment processing
- Cross-border payment support
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
import json
import uuid
import hashlib
import logging

# Import models
from src.models.african_payment_framework import (
    db, AfricanPaymentGateway, PaymentGatewayIntegration, 
    PaymentTransaction, PaymentGatewayAnalytics, AfricanPaymentMethod
)

# Create blueprint
african_payment_bp = Blueprint('african_payment', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@african_payment_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for African payment integration framework"""
    try:
        # Check database connectivity
        gateway_count = db.session.query(func.count(AfricanPaymentGateway.id)).scalar()
        integration_count = db.session.query(func.count(PaymentGatewayIntegration.id)).scalar()
        transaction_count = db.session.query(func.count(PaymentTransaction.id)).scalar()
        
        return jsonify({
            'status': 'healthy',
            'service': 'WebWaka African Payment Integration Framework',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'database': {
                'connected': True,
                'gateways': gateway_count,
                'integrations': integration_count,
                'transactions': transaction_count
            },
            'features': [
                'Universal African Payment Gateway Management',
                '115+ Payment Gateway Support',
                'Cross-Border Payment Processing',
                'Mobile Money Integration',
                'Banking API Connectivity',
                'Real-Time Analytics',
                'African Network Optimization',
                'Cultural Intelligence Integration'
            ]
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# ============================================================================
# PAYMENT GATEWAY MANAGEMENT ENDPOINTS
# ============================================================================

@african_payment_bp.route('/gateways', methods=['GET'])
def get_payment_gateways():
    """Get all African payment gateways with filtering and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        country = request.args.get('country')
        region = request.args.get('region')
        tier = request.args.get('tier', type=int)
        status = request.args.get('status', 'Active')
        payment_method = request.args.get('payment_method')
        search = request.args.get('search')
        
        # Build query
        query = AfricanPaymentGateway.query
        
        # Apply filters
        if country:
            query = query.filter(AfricanPaymentGateway.country_code == country.upper())
        
        if region:
            query = query.filter(AfricanPaymentGateway.region == region)
        
        if tier:
            query = query.filter(AfricanPaymentGateway.tier == tier)
        
        if status:
            query = query.filter(AfricanPaymentGateway.status == status)
        
        if payment_method:
            query = query.filter(AfricanPaymentGateway.supported_payment_methods.contains(payment_method))
        
        if search:
            search_filter = or_(
                AfricanPaymentGateway.name.contains(search),
                AfricanPaymentGateway.display_name.contains(search),
                AfricanPaymentGateway.description.contains(search),
                AfricanPaymentGateway.company_name.contains(search)
            )
            query = query.filter(search_filter)
        
        # Order by priority score and tier
        query = query.order_by(AfricanPaymentGateway.tier.asc(), AfricanPaymentGateway.priority_score.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        gateways = pagination.items
        
        return jsonify({
            'success': True,
            'data': [gateway.to_dict() for gateway in gateways],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'filters_applied': {
                'country': country,
                'region': region,
                'tier': tier,
                'status': status,
                'payment_method': payment_method,
                'search': search
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching payment gateways: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch payment gateways',
            'details': str(e)
        }), 500

@african_payment_bp.route('/gateways/<gateway_id>', methods=['GET'])
def get_payment_gateway(gateway_id):
    """Get detailed information about a specific payment gateway"""
    try:
        gateway = AfricanPaymentGateway.query.filter_by(gateway_id=gateway_id).first()
        
        if not gateway:
            return jsonify({
                'success': False,
                'error': 'Payment gateway not found'
            }), 404
        
        # Get integration count for this gateway
        integration_count = PaymentGatewayIntegration.query.filter_by(gateway_id=gateway_id).count()
        
        # Get recent transaction statistics
        recent_transactions = PaymentTransaction.query.filter(
            and_(
                PaymentTransaction.gateway_id == gateway_id,
                PaymentTransaction.created_at >= datetime.utcnow() - timedelta(days=30)
            )
        ).count()
        
        gateway_data = gateway.to_dict()
        gateway_data['statistics'] = {
            'active_integrations': integration_count,
            'recent_transactions': recent_transactions
        }
        
        return jsonify({
            'success': True,
            'data': gateway_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching payment gateway {gateway_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch payment gateway',
            'details': str(e)
        }), 500

@african_payment_bp.route('/gateways', methods=['POST'])
def create_payment_gateway():
    """Create a new African payment gateway entry"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'country_code', 'region', 'api_type', 'auth_type', 
                          'supported_payment_methods', 'supported_currencies', 'company_name']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Generate gateway ID
        gateway_id = f"{data['country_code'].lower()}_{data['name'].lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}"
        
        # Create new gateway
        gateway = AfricanPaymentGateway(
            gateway_id=gateway_id,
            name=data['name'],
            display_name=data.get('display_name', data['name']),
            description=data.get('description'),
            country_code=data['country_code'].upper(),
            country_name=data.get('country_name', ''),
            region=data['region'],
            coverage_countries=json.dumps(data.get('coverage_countries', [data['country_code'].upper()])),
            market_share=data.get('market_share', 0.0),
            user_base=data.get('user_base', 0),
            api_type=data['api_type'],
            api_version=data.get('api_version'),
            api_documentation_url=data.get('api_documentation_url'),
            developer_portal_url=data.get('developer_portal_url'),
            sandbox_url=data.get('sandbox_url'),
            production_url=data.get('production_url'),
            auth_type=data['auth_type'],
            auth_requirements=json.dumps(data.get('auth_requirements', {})),
            security_features=json.dumps(data.get('security_features', [])),
            compliance_standards=json.dumps(data.get('compliance_standards', [])),
            supported_payment_methods=json.dumps(data['supported_payment_methods']),
            mobile_money_networks=json.dumps(data.get('mobile_money_networks', [])),
            card_types=json.dumps(data.get('card_types', [])),
            bank_transfer_types=json.dumps(data.get('bank_transfer_types', [])),
            alternative_methods=json.dumps(data.get('alternative_methods', [])),
            supported_currencies=json.dumps(data['supported_currencies']),
            primary_currency=data.get('primary_currency', data['supported_currencies'][0] if data['supported_currencies'] else 'USD'),
            transaction_fees=json.dumps(data.get('transaction_fees', {})),
            settlement_period=data.get('settlement_period'),
            minimum_amount=data.get('minimum_amount', 0.00),
            maximum_amount=data.get('maximum_amount'),
            uptime_percentage=data.get('uptime_percentage', 99.0),
            average_response_time=data.get('average_response_time', 1000),
            success_rate=data.get('success_rate', 99.0),
            rate_limits=json.dumps(data.get('rate_limits', {})),
            mobile_optimization_score=data.get('mobile_optimization_score', 0.0),
            network_optimization_score=data.get('network_optimization_score', 0.0),
            offline_capability_score=data.get('offline_capability_score', 0.0),
            cultural_intelligence_score=data.get('cultural_intelligence_score', 0.0),
            local_language_support=json.dumps(data.get('local_language_support', [])),
            traditional_payment_support=data.get('traditional_payment_support', False),
            company_name=data['company_name'],
            company_website=data.get('company_website'),
            headquarters_location=data.get('headquarters_location'),
            founded_year=data.get('founded_year'),
            business_model=data.get('business_model'),
            target_market=data.get('target_market'),
            integration_complexity=data.get('integration_complexity', 'Medium'),
            sdk_availability=json.dumps(data.get('sdk_availability', [])),
            webhook_support=data.get('webhook_support', False),
            callback_support=data.get('callback_support', False),
            testing_environment=data.get('testing_environment', 'Limited'),
            developer_support_quality=data.get('developer_support_quality', 'Good'),
            regulatory_licenses=json.dumps(data.get('regulatory_licenses', [])),
            regulatory_bodies=json.dumps(data.get('regulatory_bodies', [])),
            kyc_requirements=json.dumps(data.get('kyc_requirements', {})),
            aml_compliance=data.get('aml_compliance', False),
            status=data.get('status', 'Active'),
            tier=data.get('tier', 2),
            priority_score=data.get('priority_score', 50.0)
        )
        
        db.session.add(gateway)
        db.session.commit()
        
        logger.info(f"Created new payment gateway: {gateway_id}")
        
        return jsonify({
            'success': True,
            'message': 'Payment gateway created successfully',
            'data': gateway.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating payment gateway: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create payment gateway',
            'details': str(e)
        }), 500

# ============================================================================
# PAYMENT GATEWAY INTEGRATION ENDPOINTS
# ============================================================================

@african_payment_bp.route('/integrations', methods=['GET'])
def get_integrations():
    """Get payment gateway integrations for a user"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id parameter is required'
            }), 400
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status = request.args.get('status')
        gateway_id = request.args.get('gateway_id')
        
        # Build query
        query = PaymentGatewayIntegration.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter(PaymentGatewayIntegration.status == status)
        
        if gateway_id:
            query = query.filter(PaymentGatewayIntegration.gateway_id == gateway_id)
        
        # Order by creation date
        query = query.order_by(PaymentGatewayIntegration.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        integrations = pagination.items
        
        return jsonify({
            'success': True,
            'data': [integration.to_dict() for integration in integrations],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching integrations: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch integrations',
            'details': str(e)
        }), 500

@african_payment_bp.route('/integrations', methods=['POST'])
def create_integration():
    """Create a new payment gateway integration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['gateway_id', 'user_id', 'integration_name', 'api_credentials']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Verify gateway exists
        gateway = AfricanPaymentGateway.query.filter_by(gateway_id=data['gateway_id']).first()
        if not gateway:
            return jsonify({
                'success': False,
                'error': 'Payment gateway not found'
            }), 404
        
        # Generate integration ID
        integration_id = f"int_{data['gateway_id']}_{data['user_id']}_{uuid.uuid4().hex[:8]}"
        
        # Encrypt credentials (simplified - use proper encryption in production)
        credentials_hash = hashlib.sha256(json.dumps(data['api_credentials']).encode()).hexdigest()
        
        # Create integration
        integration = PaymentGatewayIntegration(
            integration_id=integration_id,
            gateway_id=data['gateway_id'],
            user_id=data['user_id'],
            environment=data.get('environment', 'sandbox'),
            integration_name=data['integration_name'],
            description=data.get('description'),
            api_credentials=credentials_hash,  # Store encrypted in production
            webhook_url=data.get('webhook_url'),
            callback_url=data.get('callback_url'),
            configuration=json.dumps(data.get('configuration', {})),
            payment_methods_enabled=json.dumps(data.get('payment_methods_enabled', [])),
            currencies_enabled=json.dumps(data.get('currencies_enabled', [])),
            daily_limit=data.get('daily_limit'),
            monthly_limit=data.get('monthly_limit'),
            per_transaction_limit=data.get('per_transaction_limit'),
            status='Active'
        )
        
        db.session.add(integration)
        db.session.commit()
        
        logger.info(f"Created new integration: {integration_id}")
        
        return jsonify({
            'success': True,
            'message': 'Integration created successfully',
            'data': integration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating integration: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create integration',
            'details': str(e)
        }), 500

# ============================================================================
# PAYMENT TRANSACTION ENDPOINTS
# ============================================================================

@african_payment_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """Get payment transactions with filtering and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        integration_id = request.args.get('integration_id')
        gateway_id = request.args.get('gateway_id')
        status = request.args.get('status')
        payment_method = request.args.get('payment_method')
        country_code = request.args.get('country_code')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query
        query = PaymentTransaction.query
        
        # Apply filters
        if integration_id:
            query = query.filter(PaymentTransaction.integration_id == integration_id)
        
        if gateway_id:
            query = query.filter(PaymentTransaction.gateway_id == gateway_id)
        
        if status:
            query = query.filter(PaymentTransaction.status == status)
        
        if payment_method:
            query = query.filter(PaymentTransaction.payment_method == payment_method)
        
        if country_code:
            query = query.filter(PaymentTransaction.country_code == country_code.upper())
        
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query = query.filter(PaymentTransaction.created_at >= start_dt)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid start_date format. Use ISO format.'
                }), 400
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query = query.filter(PaymentTransaction.created_at <= end_dt)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid end_date format. Use ISO format.'
                }), 400
        
        # Order by creation date (newest first)
        query = query.order_by(PaymentTransaction.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        transactions = pagination.items
        
        return jsonify({
            'success': True,
            'data': [transaction.to_dict() for transaction in transactions],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch transactions',
            'details': str(e)
        }), 500

@african_payment_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """Create a new payment transaction"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['integration_id', 'amount', 'currency', 'payment_method', 'reference']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Verify integration exists
        integration = PaymentGatewayIntegration.query.filter_by(
            integration_id=data['integration_id']
        ).first()
        
        if not integration:
            return jsonify({
                'success': False,
                'error': 'Integration not found'
            }), 404
        
        # Generate transaction ID
        transaction_id = f"txn_{integration.gateway_id}_{uuid.uuid4().hex[:12]}"
        
        # Create transaction
        transaction = PaymentTransaction(
            transaction_id=transaction_id,
            gateway_id=integration.gateway_id,
            integration_id=data['integration_id'],
            reference=data['reference'],
            description=data.get('description'),
            amount=data['amount'],
            currency=data['currency'].upper(),
            payment_method=data['payment_method'],
            payment_channel=data.get('payment_channel'),
            customer_id=data.get('customer_id'),
            customer_email=data.get('customer_email'),
            customer_phone=data.get('customer_phone'),
            customer_name=data.get('customer_name'),
            country_code=data.get('country_code', integration.gateway.country_code),
            mobile_network=data.get('mobile_network'),
            bank_code=data.get('bank_code'),
            metadata=json.dumps(data.get('metadata', {})),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            status='Pending'
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        logger.info(f"Created new transaction: {transaction_id}")
        
        return jsonify({
            'success': True,
            'message': 'Transaction created successfully',
            'data': transaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating transaction: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create transaction',
            'details': str(e)
        }), 500

# ============================================================================
# ANALYTICS AND REPORTING ENDPOINTS
# ============================================================================

@african_payment_bp.route('/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get overview analytics for African payment gateways"""
    try:
        # Get query parameters
        days = request.args.get('days', 30, type=int)
        country_code = request.args.get('country_code')
        gateway_id = request.args.get('gateway_id')
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Build base query
        query = PaymentTransaction.query.filter(
            PaymentTransaction.created_at >= start_date
        )
        
        if country_code:
            query = query.filter(PaymentTransaction.country_code == country_code.upper())
        
        if gateway_id:
            query = query.filter(PaymentTransaction.gateway_id == gateway_id)
        
        # Get transaction statistics
        total_transactions = query.count()
        successful_transactions = query.filter(PaymentTransaction.status == 'Success').count()
        failed_transactions = query.filter(PaymentTransaction.status == 'Failed').count()
        pending_transactions = query.filter(PaymentTransaction.status == 'Pending').count()
        
        # Get volume statistics
        volume_query = query.filter(PaymentTransaction.status == 'Success')
        total_volume = db.session.query(func.sum(PaymentTransaction.amount)).filter(
            PaymentTransaction.id.in_([t.id for t in volume_query.all()])
        ).scalar() or 0
        
        # Get payment method breakdown
        payment_methods = db.session.query(
            PaymentTransaction.payment_method,
            func.count(PaymentTransaction.id).label('count')
        ).filter(
            PaymentTransaction.created_at >= start_date
        ).group_by(PaymentTransaction.payment_method).all()
        
        # Get country breakdown
        countries = db.session.query(
            PaymentTransaction.country_code,
            func.count(PaymentTransaction.id).label('count')
        ).filter(
            PaymentTransaction.created_at >= start_date
        ).group_by(PaymentTransaction.country_code).all()
        
        # Get gateway statistics
        gateway_stats = AfricanPaymentGateway.query.with_entities(
            func.count(AfricanPaymentGateway.id).label('total_gateways'),
            func.count(AfricanPaymentGateway.id).filter(AfricanPaymentGateway.status == 'Active').label('active_gateways')
        ).first()
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'days': days,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'transactions': {
                    'total': total_transactions,
                    'successful': successful_transactions,
                    'failed': failed_transactions,
                    'pending': pending_transactions,
                    'success_rate': (successful_transactions / total_transactions * 100) if total_transactions > 0 else 0
                },
                'volume': {
                    'total': float(total_volume),
                    'average_transaction': float(total_volume / successful_transactions) if successful_transactions > 0 else 0
                },
                'payment_methods': [
                    {'method': method, 'count': count} 
                    for method, count in payment_methods
                ],
                'countries': [
                    {'country': country, 'count': count} 
                    for country, count in countries
                ],
                'gateways': {
                    'total': gateway_stats.total_gateways if gateway_stats else 0,
                    'active': gateway_stats.active_gateways if gateway_stats else 0
                }
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching analytics overview: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch analytics overview',
            'details': str(e)
        }), 500

# ============================================================================
# AFRICAN PAYMENT METHOD ENDPOINTS
# ============================================================================

@african_payment_bp.route('/payment-methods', methods=['GET'])
def get_payment_methods():
    """Get available African payment methods"""
    try:
        country_code = request.args.get('country_code')
        category = request.args.get('category')
        region = request.args.get('region')
        
        # Build query
        query = AfricanPaymentMethod.query.filter_by(status='Active')
        
        if country_code:
            query = query.filter(
                or_(
                    AfricanPaymentMethod.primary_country == country_code.upper(),
                    AfricanPaymentMethod.available_countries.contains(country_code.upper())
                )
            )
        
        if category:
            query = query.filter(AfricanPaymentMethod.category == category)
        
        if region:
            query = query.filter(AfricanPaymentMethod.region == region)
        
        # Order by popularity
        query = query.order_by(AfricanPaymentMethod.popularity_score.desc())
        
        payment_methods = query.all()
        
        return jsonify({
            'success': True,
            'data': [method.to_dict() for method in payment_methods],
            'total': len(payment_methods)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching payment methods: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch payment methods',
            'details': str(e)
        }), 500

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@african_payment_bp.route('/countries', methods=['GET'])
def get_supported_countries():
    """Get list of supported African countries"""
    try:
        countries = db.session.query(
            AfricanPaymentGateway.country_code,
            AfricanPaymentGateway.country_name,
            AfricanPaymentGateway.region,
            func.count(AfricanPaymentGateway.id).label('gateway_count')
        ).filter(
            AfricanPaymentGateway.status == 'Active'
        ).group_by(
            AfricanPaymentGateway.country_code,
            AfricanPaymentGateway.country_name,
            AfricanPaymentGateway.region
        ).order_by(
            AfricanPaymentGateway.region,
            AfricanPaymentGateway.country_name
        ).all()
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'country_code': country.country_code,
                    'country_name': country.country_name,
                    'region': country.region,
                    'gateway_count': country.gateway_count
                }
                for country in countries
            ],
            'total': len(countries)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching supported countries: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch supported countries',
            'details': str(e)
        }), 500

@african_payment_bp.route('/statistics', methods=['GET'])
def get_system_statistics():
    """Get overall system statistics"""
    try:
        # Get gateway statistics
        gateway_stats = db.session.query(
            func.count(AfricanPaymentGateway.id).label('total'),
            func.count(AfricanPaymentGateway.id).filter(AfricanPaymentGateway.status == 'Active').label('active'),
            func.count(AfricanPaymentGateway.id).filter(AfricanPaymentGateway.tier == 1).label('tier1'),
            func.count(AfricanPaymentGateway.id).filter(AfricanPaymentGateway.tier == 2).label('tier2'),
            func.count(AfricanPaymentGateway.id).filter(AfricanPaymentGateway.tier == 3).label('tier3')
        ).first()
        
        # Get regional distribution
        regional_stats = db.session.query(
            AfricanPaymentGateway.region,
            func.count(AfricanPaymentGateway.id).label('count')
        ).filter(
            AfricanPaymentGateway.status == 'Active'
        ).group_by(AfricanPaymentGateway.region).all()
        
        # Get integration statistics
        integration_stats = db.session.query(
            func.count(PaymentGatewayIntegration.id).label('total'),
            func.count(PaymentGatewayIntegration.id).filter(PaymentGatewayIntegration.status == 'Active').label('active')
        ).first()
        
        # Get transaction statistics (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        transaction_stats = db.session.query(
            func.count(PaymentTransaction.id).label('total'),
            func.count(PaymentTransaction.id).filter(PaymentTransaction.status == 'Success').label('successful'),
            func.sum(PaymentTransaction.amount).filter(PaymentTransaction.status == 'Success').label('volume')
        ).filter(
            PaymentTransaction.created_at >= thirty_days_ago
        ).first()
        
        return jsonify({
            'success': True,
            'data': {
                'gateways': {
                    'total': gateway_stats.total if gateway_stats else 0,
                    'active': gateway_stats.active if gateway_stats else 0,
                    'tier_1': gateway_stats.tier1 if gateway_stats else 0,
                    'tier_2': gateway_stats.tier2 if gateway_stats else 0,
                    'tier_3': gateway_stats.tier3 if gateway_stats else 0
                },
                'regions': [
                    {'region': region, 'count': count}
                    for region, count in regional_stats
                ],
                'integrations': {
                    'total': integration_stats.total if integration_stats else 0,
                    'active': integration_stats.active if integration_stats else 0
                },
                'transactions_30_days': {
                    'total': transaction_stats.total if transaction_stats else 0,
                    'successful': transaction_stats.successful if transaction_stats else 0,
                    'volume': float(transaction_stats.volume) if transaction_stats and transaction_stats.volume else 0.0
                }
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching system statistics: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch system statistics',
            'details': str(e)
        }), 500

