"""
WebWaka Tier 1 Critical African Payment Platform Integration Routes
================================================================

This module provides comprehensive API routes for managing integrations
with the most critical African payment platforms: M-Pesa, MTN Mobile Money,
Paystack, Flutterwave, and Hubtel.

Features:
- Complete CRUD operations for all Tier 1 platform integrations
- Real-time transaction processing and status tracking
- Platform-specific configuration management
- Comprehensive analytics and reporting
- Health monitoring and performance metrics
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid
import json

# Import database and models
from src.models.user import db
from src.models.tier1_critical_platforms import (
    MPesaIntegration, MTNMoMoIntegration, PaystackIntegration,
    FlutterwaveIntegration, HubtelIntegration, Tier1Transaction
)

# Create blueprint
tier1_platforms_bp = Blueprint('tier1_platforms', __name__, url_prefix='/api/tier1-platforms')

# ============================================================================
# HEALTH AND STATUS ENDPOINTS
# ============================================================================

@tier1_platforms_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Tier 1 platform integrations"""
    try:
        # Count integrations by platform
        mpesa_count = MPesaIntegration.query.count()
        mtn_momo_count = MTNMoMoIntegration.query.count()
        paystack_count = PaystackIntegration.query.count()
        flutterwave_count = FlutterwaveIntegration.query.count()
        hubtel_count = HubtelIntegration.query.count()
        
        # Count transactions
        total_transactions = Tier1Transaction.query.count()
        successful_transactions = Tier1Transaction.query.filter_by(status='Success').count()
        
        return jsonify({
            'service': 'WebWaka Tier 1 Critical Platforms Integration',
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'database': {
                'connected': True,
                'mpesa_integrations': mpesa_count,
                'mtn_momo_integrations': mtn_momo_count,
                'paystack_integrations': paystack_count,
                'flutterwave_integrations': flutterwave_count,
                'hubtel_integrations': hubtel_count,
                'total_integrations': mpesa_count + mtn_momo_count + paystack_count + flutterwave_count + hubtel_count,
                'total_transactions': total_transactions,
                'successful_transactions': successful_transactions
            },
            'platforms': [
                'M-Pesa (Kenya Mobile Money Leader)',
                'MTN Mobile Money (17+ Countries, 900+ Partners)',
                'Paystack (Nigeria Payment Gateway Leader)',
                'Flutterwave (34+ Countries, 1M+ Businesses)',
                'Hubtel (Ghana Payment Aggregator Leader)'
            ],
            'features': [
                'Universal African Payment Gateway Management',
                'Tier 1 Critical Platform Integration',
                'Real-Time Transaction Processing',
                'Multi-Country Payment Support',
                'Mobile Money Integration',
                'Banking API Connectivity',
                'Cross-Border Payment Processing',
                'Real-Time Analytics',
                'African Network Optimization',
                'Cultural Intelligence Integration'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'service': 'WebWaka Tier 1 Critical Platforms Integration',
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@tier1_platforms_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get comprehensive statistics for all Tier 1 platforms"""
    try:
        # Platform integration counts
        stats = {
            'platform_integrations': {
                'mpesa': MPesaIntegration.query.count(),
                'mtn_momo': MTNMoMoIntegration.query.count(),
                'paystack': PaystackIntegration.query.count(),
                'flutterwave': FlutterwaveIntegration.query.count(),
                'hubtel': HubtelIntegration.query.count()
            },
            'transaction_statistics': {
                'total_transactions': Tier1Transaction.query.count(),
                'successful_transactions': Tier1Transaction.query.filter_by(status='Success').count(),
                'failed_transactions': Tier1Transaction.query.filter_by(status='Failed').count(),
                'pending_transactions': Tier1Transaction.query.filter_by(status='Pending').count()
            },
            'platform_transaction_breakdown': {}
        }
        
        # Transaction breakdown by platform
        platforms = ['mpesa', 'mtn_momo', 'paystack', 'flutterwave', 'hubtel']
        for platform in platforms:
            platform_transactions = Tier1Transaction.query.filter_by(platform=platform).count()
            platform_successful = Tier1Transaction.query.filter_by(platform=platform, status='Success').count()
            
            stats['platform_transaction_breakdown'][platform] = {
                'total_transactions': platform_transactions,
                'successful_transactions': platform_successful,
                'success_rate': (platform_successful / platform_transactions * 100) if platform_transactions > 0 else 0
            }
        
        # Calculate overall success rate
        total_trans = stats['transaction_statistics']['total_transactions']
        successful_trans = stats['transaction_statistics']['successful_transactions']
        stats['overall_success_rate'] = (successful_trans / total_trans * 100) if total_trans > 0 else 0
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# M-PESA INTEGRATION ENDPOINTS
# ============================================================================

@tier1_platforms_bp.route('/mpesa/integrations', methods=['GET'])
def get_mpesa_integrations():
    """Get all M-Pesa integrations for the user"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            user_id = 1  # Default test user for API testing
        
        integrations = MPesaIntegration.query.filter_by(user_id=user_id).all()
        return jsonify([integration.to_dict() for integration in integrations]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/mpesa/integrations', methods=['POST'])
def create_mpesa_integration():
    """Create a new M-Pesa integration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'business_short_code', 'consumer_key', 'consumer_secret']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new integration
        integration = MPesaIntegration(
            integration_id=f"mpesa_{uuid.uuid4().hex[:12]}",
            user_id=data['user_id'],
            business_short_code=data['business_short_code'],
            consumer_key=data['consumer_key'],  # Should be encrypted in production
            consumer_secret=data['consumer_secret'],  # Should be encrypted in production
            passkey=data.get('passkey'),
            environment=data.get('environment', 'sandbox'),
            callback_url=data.get('callback_url'),
            result_url=data.get('result_url'),
            timeout_url=data.get('timeout_url'),
            stk_push_enabled=data.get('stk_push_enabled', True),
            c2b_enabled=data.get('c2b_enabled', False),
            b2c_enabled=data.get('b2c_enabled', False),
            b2b_enabled=data.get('b2b_enabled', False)
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'M-Pesa integration created successfully',
            'integration': integration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/mpesa/integrations/<integration_id>', methods=['GET'])
def get_mpesa_integration(integration_id):
    """Get specific M-Pesa integration details"""
    try:
        integration = MPesaIntegration.query.filter_by(integration_id=integration_id).first()
        if not integration:
            return jsonify({'error': 'M-Pesa integration not found'}), 404
        
        return jsonify(integration.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/mpesa/integrations/<integration_id>', methods=['PUT'])
def update_mpesa_integration(integration_id):
    """Update M-Pesa integration configuration"""
    try:
        integration = MPesaIntegration.query.filter_by(integration_id=integration_id).first()
        if not integration:
            return jsonify({'error': 'M-Pesa integration not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        updatable_fields = [
            'passkey', 'callback_url', 'result_url', 'timeout_url',
            'stk_push_enabled', 'c2b_enabled', 'b2c_enabled', 'b2b_enabled',
            'minimum_amount', 'maximum_amount', 'daily_limit', 'monthly_limit'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(integration, field, data[field])
        
        integration.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'M-Pesa integration updated successfully',
            'integration': integration.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# MTN MOBILE MONEY INTEGRATION ENDPOINTS
# ============================================================================

@tier1_platforms_bp.route('/mtn-momo/integrations', methods=['GET'])
def get_mtn_momo_integrations():
    """Get all MTN Mobile Money integrations for the user"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter is required'}), 400
        
        integrations = MTNMoMoIntegration.query.filter_by(user_id=user_id).all()
        return jsonify([integration.to_dict() for integration in integrations]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/mtn-momo/integrations', methods=['POST'])
def create_mtn_momo_integration():
    """Create a new MTN Mobile Money integration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'subscription_key', 'api_user_id', 'api_key']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new integration
        integration = MTNMoMoIntegration(
            integration_id=f"mtn_momo_{uuid.uuid4().hex[:12]}",
            user_id=data['user_id'],
            subscription_key=data['subscription_key'],  # Should be encrypted in production
            api_user_id=data['api_user_id'],
            api_key=data['api_key'],  # Should be encrypted in production
            target_environment=data.get('target_environment', 'sandbox'),
            environment=data.get('environment', 'sandbox'),
            callback_host=data.get('callback_host'),
            collections_enabled=data.get('collections_enabled', True),
            disbursements_enabled=data.get('disbursements_enabled', False),
            remittances_enabled=data.get('remittances_enabled', False),
            country_code=data.get('country_code', 'UG'),
            currency=data.get('currency', 'UGX'),
            supported_countries=json.dumps(data.get('supported_countries', ['UG']))
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'MTN Mobile Money integration created successfully',
            'integration': integration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# PAYSTACK INTEGRATION ENDPOINTS
# ============================================================================

@tier1_platforms_bp.route('/paystack/integrations', methods=['GET'])
def get_paystack_integrations():
    """Get all Paystack integrations for the user"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter is required'}), 400
        
        integrations = PaystackIntegration.query.filter_by(user_id=user_id).all()
        return jsonify([integration.to_dict() for integration in integrations]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/paystack/integrations', methods=['POST'])
def create_paystack_integration():
    """Create a new Paystack integration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'public_key', 'secret_key']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new integration
        integration = PaystackIntegration(
            integration_id=f"paystack_{uuid.uuid4().hex[:12]}",
            user_id=data['user_id'],
            public_key=data['public_key'],
            secret_key=data['secret_key'],  # Should be encrypted in production
            webhook_secret=data.get('webhook_secret'),
            environment=data.get('environment', 'test'),
            webhook_url=data.get('webhook_url'),
            business_name=data.get('business_name'),
            business_email=data.get('business_email'),
            business_phone=data.get('business_phone'),
            primary_country=data.get('primary_country', 'NG'),
            primary_currency=data.get('primary_currency', 'NGN'),
            supported_countries=json.dumps(data.get('supported_countries', ['NG'])),
            supported_currencies=json.dumps(data.get('supported_currencies', ['NGN']))
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'Paystack integration created successfully',
            'integration': integration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# FLUTTERWAVE INTEGRATION ENDPOINTS
# ============================================================================

@tier1_platforms_bp.route('/flutterwave/integrations', methods=['GET'])
def get_flutterwave_integrations():
    """Get all Flutterwave integrations for the user"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter is required'}), 400
        
        integrations = FlutterwaveIntegration.query.filter_by(user_id=user_id).all()
        return jsonify([integration.to_dict() for integration in integrations]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/flutterwave/integrations', methods=['POST'])
def create_flutterwave_integration():
    """Create a new Flutterwave integration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'public_key', 'secret_key', 'encryption_key']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new integration
        integration = FlutterwaveIntegration(
            integration_id=f"flutterwave_{uuid.uuid4().hex[:12]}",
            user_id=data['user_id'],
            public_key=data['public_key'],
            secret_key=data['secret_key'],  # Should be encrypted in production
            encryption_key=data['encryption_key'],  # Should be encrypted in production
            webhook_secret_hash=data.get('webhook_secret_hash'),
            environment=data.get('environment', 'staging'),
            webhook_url=data.get('webhook_url'),
            redirect_url=data.get('redirect_url'),
            business_name=data.get('business_name'),
            business_email=data.get('business_email'),
            business_logo=data.get('business_logo'),
            business_description=data.get('business_description'),
            primary_country=data.get('primary_country', 'NG'),
            primary_currency=data.get('primary_currency', 'NGN'),
            supported_countries=json.dumps(data.get('supported_countries', ['NG'])),
            supported_currencies=json.dumps(data.get('supported_currencies', ['NGN']))
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'Flutterwave integration created successfully',
            'integration': integration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# HUBTEL INTEGRATION ENDPOINTS
# ============================================================================

@tier1_platforms_bp.route('/hubtel/integrations', methods=['GET'])
def get_hubtel_integrations():
    """Get all Hubtel integrations for the user"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter is required'}), 400
        
        integrations = HubtelIntegration.query.filter_by(user_id=user_id).all()
        return jsonify([integration.to_dict() for integration in integrations]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/hubtel/integrations', methods=['POST'])
def create_hubtel_integration():
    """Create a new Hubtel integration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'client_id', 'client_secret']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new integration
        integration = HubtelIntegration(
            integration_id=f"hubtel_{uuid.uuid4().hex[:12]}",
            user_id=data['user_id'],
            client_id=data['client_id'],
            client_secret=data['client_secret'],  # Should be encrypted in production
            merchant_account_number=data.get('merchant_account_number'),
            api_key=data.get('api_key'),
            environment=data.get('environment', 'sandbox'),
            callback_url=data.get('callback_url'),
            return_url=data.get('return_url'),
            cancellation_url=data.get('cancellation_url'),
            business_name=data.get('business_name'),
            business_email=data.get('business_email'),
            business_phone=data.get('business_phone'),
            business_website=data.get('business_website'),
            supported_currencies=json.dumps(data.get('supported_currencies', ['GHS']))
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'Hubtel integration created successfully',
            'integration': integration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# TRANSACTION MANAGEMENT ENDPOINTS
# ============================================================================

@tier1_platforms_bp.route('/transactions', methods=['GET'])
def get_tier1_transactions():
    """Get transactions across all Tier 1 platforms"""
    try:
        # Query parameters
        platform = request.args.get('platform')
        status = request.args.get('status')
        user_id = request.args.get('user_id', type=int)
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Build query
        query = Tier1Transaction.query
        
        if platform:
            query = query.filter_by(platform=platform)
        if status:
            query = query.filter_by(status=status)
        if user_id:
            # Filter by user_id through platform integration
            query = query.filter_by(platform_integration_id=f"{platform}_{user_id}")
        
        # Apply pagination
        transactions = query.order_by(Tier1Transaction.created_at.desc()).offset(offset).limit(limit).all()
        total_count = query.count()
        
        return jsonify({
            'transactions': [transaction.to_dict() for transaction in transactions],
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/transactions', methods=['POST'])
def create_tier1_transaction():
    """Create a new transaction for Tier 1 platforms"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['platform', 'platform_integration_id', 'amount', 'currency', 'payment_method', 'country_code']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new transaction
        transaction = Tier1Transaction(
            transaction_id=f"tier1_{uuid.uuid4().hex[:16]}",
            platform=data['platform'],
            platform_integration_id=data['platform_integration_id'],
            external_transaction_id=data.get('external_transaction_id'),
            reference=data.get('reference', f"ref_{uuid.uuid4().hex[:8]}"),
            description=data.get('description'),
            amount=data['amount'],
            currency=data['currency'],
            payment_method=data['payment_method'],
            payment_channel=data.get('payment_channel'),
            customer_id=data.get('customer_id'),
            customer_email=data.get('customer_email'),
            customer_phone=data.get('customer_phone'),
            customer_name=data.get('customer_name'),
            country_code=data['country_code'],
            mobile_network=data.get('mobile_network'),
            bank_code=data.get('bank_code'),
            platform_request_data=json.dumps(data.get('platform_request_data', {})),
            ip_address=data.get('ip_address'),
            user_agent=data.get('user_agent')
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Tier 1 transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/transactions/<transaction_id>', methods=['GET'])
def get_tier1_transaction(transaction_id):
    """Get specific Tier 1 transaction details"""
    try:
        transaction = Tier1Transaction.query.filter_by(transaction_id=transaction_id).first()
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        return jsonify(transaction.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/transactions/<transaction_id>/status', methods=['PUT'])
def update_transaction_status(transaction_id):
    """Update transaction status and related information"""
    try:
        transaction = Tier1Transaction.query.filter_by(transaction_id=transaction_id).first()
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        data = request.get_json()
        
        # Update status and related fields
        if 'status' in data:
            transaction.status = data['status']
            
            # Update timing based on status
            if data['status'] == 'Processing' and not transaction.processed_at:
                transaction.processed_at = datetime.utcnow()
            elif data['status'] in ['Success', 'Failed', 'Cancelled'] and not transaction.completed_at:
                transaction.completed_at = datetime.utcnow()
                
                # Calculate response time
                if transaction.initiated_at:
                    response_time = (transaction.completed_at - transaction.initiated_at).total_seconds() * 1000
                    transaction.response_time = int(response_time)
        
        # Update other fields
        updatable_fields = [
            'platform_status', 'external_transaction_id', 'failure_reason',
            'platform_fee', 'gateway_fee', 'total_fees', 'net_amount'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(transaction, field, data[field])
        
        # Update platform response data
        if 'platform_response_data' in data:
            transaction.platform_response_data = json.dumps(data['platform_response_data'])
        
        if 'platform_callback_data' in data:
            transaction.platform_callback_data = json.dumps(data['platform_callback_data'])
        
        transaction.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction status updated successfully',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ANALYTICS AND REPORTING ENDPOINTS
# ============================================================================

@tier1_platforms_bp.route('/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get comprehensive analytics overview for all Tier 1 platforms"""
    try:
        # Time range parameters
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Platform performance
        platforms = ['mpesa', 'mtn_momo', 'paystack', 'flutterwave', 'hubtel']
        platform_analytics = {}
        
        for platform in platforms:
            platform_transactions = Tier1Transaction.query.filter(
                Tier1Transaction.platform == platform,
                Tier1Transaction.created_at >= start_date
            ).all()
            
            total_transactions = len(platform_transactions)
            successful_transactions = len([t for t in platform_transactions if t.status == 'Success'])
            total_volume = sum([float(t.amount) for t in platform_transactions if t.amount])
            
            platform_analytics[platform] = {
                'total_transactions': total_transactions,
                'successful_transactions': successful_transactions,
                'failed_transactions': total_transactions - successful_transactions,
                'success_rate': (successful_transactions / total_transactions * 100) if total_transactions > 0 else 0,
                'total_volume': total_volume,
                'average_transaction_value': total_volume / total_transactions if total_transactions > 0 else 0
            }
        
        # Overall metrics
        all_transactions = Tier1Transaction.query.filter(Tier1Transaction.created_at >= start_date).all()
        total_all = len(all_transactions)
        successful_all = len([t for t in all_transactions if t.status == 'Success'])
        volume_all = sum([float(t.amount) for t in all_transactions if t.amount])
        
        return jsonify({
            'period': f'Last {days} days',
            'overall_metrics': {
                'total_transactions': total_all,
                'successful_transactions': successful_all,
                'failed_transactions': total_all - successful_all,
                'success_rate': (successful_all / total_all * 100) if total_all > 0 else 0,
                'total_volume': volume_all,
                'average_transaction_value': volume_all / total_all if total_all > 0 else 0
            },
            'platform_analytics': platform_analytics,
            'top_performing_platform': max(platform_analytics.keys(), 
                                         key=lambda x: platform_analytics[x]['success_rate']) if platform_analytics else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tier1_platforms_bp.route('/platforms/supported', methods=['GET'])
def get_supported_platforms():
    """Get list of all supported Tier 1 platforms with their capabilities"""
    try:
        platforms = [
            {
                'platform_id': 'mpesa',
                'name': 'M-Pesa',
                'provider': 'Safaricom',
                'country': 'Kenya',
                'description': 'Kenya\'s leading mobile money platform with 50M+ users',
                'capabilities': ['STK Push', 'C2B', 'B2C', 'B2B', 'Account Balance', 'Transaction Status', 'Reversal'],
                'payment_methods': ['Mobile Money'],
                'currencies': ['KES'],
                'api_type': 'REST',
                'documentation_url': 'https://developer.safaricom.co.ke/Documentation',
                'sandbox_available': True,
                'webhook_support': True
            },
            {
                'platform_id': 'mtn_momo',
                'name': 'MTN Mobile Money',
                'provider': 'MTN Group',
                'countries': ['UG', 'GH', 'CI', 'CM', 'BJ', 'RW', 'ZM', 'SS', 'GN', 'LR', 'AF', 'SZ', 'CG', 'BF', 'ML', 'NE', 'TD'],
                'description': 'Pan-African mobile money platform with 900+ developer partners',
                'capabilities': ['Collections', 'Disbursements', 'Remittances', 'Account Balance', 'Transaction Status'],
                'payment_methods': ['Mobile Money'],
                'currencies': ['UGX', 'GHS', 'XOF', 'XAF', 'RWF', 'ZMW', 'SSP', 'GNF', 'LRD', 'AFN', 'SZL', 'CDF'],
                'api_type': 'REST',
                'documentation_url': 'https://momodeveloper.mtn.com/api-documentation',
                'sandbox_available': True,
                'webhook_support': True
            },
            {
                'platform_id': 'paystack',
                'name': 'Paystack',
                'provider': 'Stripe (Paystack)',
                'countries': ['NG', 'GH', 'ZA', 'KE'],
                'description': 'Leading African payment gateway serving 200,000+ businesses',
                'capabilities': ['Payments', 'Transfers', 'Subscriptions', 'Invoices', 'Payment Pages', 'Disputes'],
                'payment_methods': ['Cards', 'Bank Transfer', 'USSD', 'QR Code', 'Mobile Money'],
                'currencies': ['NGN', 'GHS', 'ZAR', 'KES', 'USD'],
                'api_type': 'REST',
                'documentation_url': 'https://paystack.com/docs/api/',
                'sandbox_available': True,
                'webhook_support': True
            },
            {
                'platform_id': 'flutterwave',
                'name': 'Flutterwave',
                'provider': 'Flutterwave Inc.',
                'countries': ['NG', 'GH', 'KE', 'UG', 'ZA', 'TZ', 'RW', 'ZM', 'MW', 'SL', 'LR', 'GM', 'GN', 'BF', 'CI', 'SN', 'ML', 'NE', 'TD', 'CM', 'GA', 'CG', 'CF', 'DJ', 'ER', 'ET', 'SO', 'SS', 'SD', 'EG', 'LY', 'TN', 'DZ', 'MA'],
                'description': 'Pan-African payment platform serving 1M+ businesses across 34+ countries',
                'capabilities': ['Standard Payments', 'Inline Payments', 'Transfers', 'Bills', 'Subscriptions', 'Payment Plans'],
                'payment_methods': ['Cards', 'Bank Transfer', 'USSD', 'Mobile Money', 'QR Code', 'Vouchers'],
                'currencies': ['NGN', 'GHS', 'KES', 'UGX', 'ZAR', 'TZS', 'RWF', 'ZMW', 'MWK', 'SLL', 'LRD', 'GMD', 'GNF', 'XOF', 'XAF', 'USD', 'EUR', 'GBP'],
                'api_type': 'REST',
                'documentation_url': 'https://developer.flutterwave.com/docs',
                'sandbox_available': True,
                'webhook_support': True
            },
            {
                'platform_id': 'hubtel',
                'name': 'Hubtel',
                'provider': 'Hubtel Limited',
                'country': 'Ghana',
                'description': 'Ghana\'s leading payment aggregator and multi-channel solutions provider',
                'capabilities': ['Receive Money', 'Send Money', 'Checkout', 'Direct Pay', 'Recurring Payments'],
                'payment_methods': ['Mobile Money (MTN, Vodafone, AirtelTigo)', 'Cards', 'Bank Payments', 'USSD'],
                'currencies': ['GHS'],
                'api_type': 'REST',
                'documentation_url': 'https://developers.hubtel.com/',
                'sandbox_available': True,
                'webhook_support': True
            }
        ]
        
        return jsonify({
            'total_platforms': len(platforms),
            'platforms': platforms,
            'total_countries_covered': len(set([country for platform in platforms for country in (platform.get('countries', [platform.get('country', '')]) if platform.get('countries') else [platform.get('country', '')])]))
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

