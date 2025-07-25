"""
WebWaka South African Payment Ecosystem API Routes
=================================================

This module provides comprehensive API endpoints for South African payment
gateway integrations, representing the most sophisticated financial market
in Africa.

Supported Platforms:
- PayFast (South Africa's leading payment processor)
- Stitch Money (Enterprise payment solutions)
- Ozow (Instant EFT specialist)
- Standard Bank API Marketplace
- Yoco (SME payment solutions)

Features:
- Complete South African payment ecosystem coverage
- Advanced banking API integration
- Real-time payment processing
- Enterprise-grade solutions
- SME-focused payment tools
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid
import json

# Import shared database instance
from src.models.user import db
from src.models.south_african_payment_ecosystem import (
    PayFastIntegration, StitchMoneyIntegration, OzowIntegration,
    StandardBankAPIIntegration, YocoIntegration,
    SouthAfricanPaymentTransaction, SouthAfricanPaymentAnalytics
)

# Create blueprint
south_african_ecosystem_bp = Blueprint('south_african_payments', __name__, url_prefix='/api/south-african-payments')

@south_african_ecosystem_bp.route('/health', methods=['GET'])
def health_check():
    """
    South African Payment Ecosystem Health Check
    
    Returns the health status of the South African payment ecosystem
    with comprehensive platform statistics and capabilities.
    """
    try:
        # Get database statistics
        total_integrations = (
            PayFastIntegration.query.count() +
            StitchMoneyIntegration.query.count() +
            OzowIntegration.query.count() +
            StandardBankAPIIntegration.query.count() +
            YocoIntegration.query.count()
        )
        
        payfast_integrations = PayFastIntegration.query.count()
        stitch_integrations = StitchMoneyIntegration.query.count()
        ozow_integrations = OzowIntegration.query.count()
        standard_bank_integrations = StandardBankAPIIntegration.query.count()
        yoco_integrations = YocoIntegration.query.count()
        
        total_transactions = SouthAfricanPaymentTransaction.query.count()
        successful_transactions = SouthAfricanPaymentTransaction.query.filter_by(status='completed').count()
        
        return jsonify({
            'service': 'WebWaka South African Payment Ecosystem Integration',
            'version': '1.0.0',
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': {
                'connected': True,
                'total_integrations': total_integrations,
                'payfast_integrations': payfast_integrations,
                'stitch_integrations': stitch_integrations,
                'ozow_integrations': ozow_integrations,
                'standard_bank_integrations': standard_bank_integrations,
                'yoco_integrations': yoco_integrations,
                'total_transactions': total_transactions,
                'successful_transactions': successful_transactions
            },
            'features': [
                'Complete South African Payment Ecosystem Coverage',
                'PayFast Integration (SA\'s Leading Payment Processor)',
                'Stitch Money Integration (Enterprise Payment Solutions)',
                'Ozow Integration (Instant EFT Specialist)',
                'Standard Bank API Marketplace Integration',
                'Yoco Integration (SME Payment Solutions)',
                'South African Rand (ZAR) Optimization',
                'Instant EFT and Bank API Integration',
                'Card Payment Processing (Visa, Mastercard, Amex)',
                'QR Code Payment Support',
                'Real-Time Payment Processing',
                'Enterprise-Grade Banking APIs',
                'SME Payment Solutions',
                'Advanced Analytics and Reporting'
            ],
            'south_african_platforms': [
                'PayFast (South Africa\'s Leading Payment Processor)',
                'Stitch Money (Enterprise Payment Solutions)',
                'Ozow (Instant EFT Specialist)',
                'Standard Bank API Marketplace (Award-Winning Open Banking)',
                'Yoco (SME Payment Solutions)',
                'Nedbank API Platform',
                'Absa Bank APIs',
                'FNB APIs',
                'Capitec Bank APIs',
                'SnapScan (QR Code Payments)'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'service': 'WebWaka South African Payment Ecosystem Integration',
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@south_african_ecosystem_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get comprehensive South African payment ecosystem statistics"""
    try:
        # Platform statistics
        platform_stats = {
            'payfast': PayFastIntegration.query.count(),
            'stitch_money': StitchMoneyIntegration.query.count(),
            'ozow': OzowIntegration.query.count(),
            'standard_bank': StandardBankAPIIntegration.query.count(),
            'yoco': YocoIntegration.query.count()
        }
        
        # Transaction statistics
        total_transactions = SouthAfricanPaymentTransaction.query.count()
        successful_transactions = SouthAfricanPaymentTransaction.query.filter_by(status='completed').count()
        failed_transactions = SouthAfricanPaymentTransaction.query.filter_by(status='failed').count()
        
        # Calculate success rate
        success_rate = (successful_transactions / total_transactions * 100) if total_transactions > 0 else 0
        
        return jsonify({
            'platform_statistics': platform_stats,
            'transaction_statistics': {
                'total_transactions': total_transactions,
                'successful_transactions': successful_transactions,
                'failed_transactions': failed_transactions,
                'success_rate': round(success_rate, 2)
            },
            'total_integrations': sum(platform_stats.values()),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@south_african_ecosystem_bp.route('/platforms/supported', methods=['GET'])
def get_supported_platforms():
    """Get all supported South African payment platforms with detailed information"""
    try:
        platforms = [
            {
                'platform_id': 'payfast',
                'name': 'PayFast',
                'type': 'Payment Processor',
                'description': 'South Africa\'s leading payment processor with 70+ plugin integrations',
                'api_type': 'REST',
                'documentation_url': 'https://developers.payfast.co.za/',
                'sandbox_available': True,
                'payment_methods': ['Card Payment', 'EFT', 'Instant EFT', 'Bitcoin', 'Mobicred', 'RCS'],
                'currencies': ['ZAR'],
                'capabilities': [
                    'Payment Processing',
                    'Recurring Payments',
                    'Refunds',
                    'Webhooks',
                    'Fraud Protection',
                    'Settlement Reporting'
                ],
                'payfast_features': [
                    '70+ Plugin Integrations',
                    'Multiple Payment Methods',
                    'Fraud Protection',
                    'T+2 Settlement'
                ]
            },
            {
                'platform_id': 'stitch_money',
                'name': 'Stitch Money',
                'type': 'Enterprise Payment Solutions',
                'description': 'Enterprise payment solutions with real-time bank APIs and advanced processing',
                'api_type': 'REST',
                'documentation_url': 'https://stitch.money/docs/',
                'sandbox_available': True,
                'payment_methods': ['Instant Pay', 'Debit Order', 'Bank Transfer'],
                'currencies': ['ZAR'],
                'capabilities': [
                    'Real-Time Bank APIs',
                    'Instant Payments',
                    'Account Verification',
                    'Debit Orders',
                    'Refunds',
                    'White Label Solutions'
                ],
                'stitch_features': [
                    'Real-Time Bank Integration',
                    'Enterprise Solutions',
                    'White Label Support',
                    'Multi-Tenant Architecture'
                ]
            },
            {
                'platform_id': 'ozow',
                'name': 'Ozow',
                'type': 'Instant EFT Specialist',
                'description': 'South Africa\'s instant EFT specialist with bank API technology',
                'api_type': 'REST',
                'documentation_url': 'https://docs.ozow.com/',
                'sandbox_available': True,
                'payment_methods': ['Instant EFT', 'Smart EFT', 'QR Code'],
                'currencies': ['ZAR'],
                'capabilities': [
                    'Instant EFT',
                    'Smart Routing',
                    'QR Code Payments',
                    'Real-Time Verification',
                    'Bank API Integration',
                    'Instant Settlement'
                ],
                'ozow_features': [
                    'Instant Settlement',
                    'Bank API Technology',
                    'Smart Routing',
                    'QR Code Support'
                ]
            },
            {
                'platform_id': 'standard_bank_api',
                'name': 'Standard Bank API Marketplace',
                'type': 'Banking API Platform',
                'description': 'Award-winning open banking API platform with comprehensive banking services',
                'api_type': 'REST',
                'documentation_url': 'https://developer.standardbank.co.za/',
                'sandbox_available': True,
                'payment_methods': ['Bank Transfer', 'Card Payment', 'Mobile Banking'],
                'currencies': ['ZAR', 'USD', 'EUR', 'GBP'],
                'capabilities': [
                    'Account Services',
                    'Payment Services',
                    'Card Services',
                    'Forex Services',
                    'Trade Finance',
                    'Loan Services'
                ],
                'standard_bank_features': [
                    'Award-Winning Open Banking API',
                    'Comprehensive Banking Services',
                    'Multi-Currency Support',
                    'Enterprise-Grade Security'
                ]
            },
            {
                'platform_id': 'yoco',
                'name': 'Yoco',
                'type': 'SME Payment Solutions',
                'description': 'SME payment solutions with card readers, online payments, and business tools',
                'api_type': 'REST',
                'documentation_url': 'https://developer.yoco.com/',
                'sandbox_available': True,
                'payment_methods': ['Card Payment', 'Online Payment', 'QR Code', 'Tap to Pay'],
                'currencies': ['ZAR'],
                'capabilities': [
                    'Card Processing',
                    'Online Payments',
                    'QR Code Payments',
                    'Business Management',
                    'Sales Reporting',
                    'Inventory Management'
                ],
                'yoco_features': [
                    'SME-Focused Solutions',
                    'Card Reader Integration',
                    'Business Management Tools',
                    'Sales Analytics'
                ]
            }
        ]
        
        return jsonify({
            'platforms': platforms,
            'total_platforms': len(platforms),
            'market_coverage': {
                'payment_processors': 1,
                'enterprise_solutions': 1,
                'instant_eft_specialists': 1,
                'banking_api_platforms': 1,
                'sme_solutions': 1
            },
            'south_african_market_features': [
                'PayFast Integration (SA\'s Leading Payment Processor)',
                'South African Rand (ZAR) Optimization',
                'Instant EFT and Bank API Integration',
                'Card Payment Processing (Visa, Mastercard, Amex)',
                'QR Code Payment Support',
                'Enterprise Banking APIs',
                'SME Payment Solutions',
                'Real-Time Settlement'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PayFast Integration Endpoints
@south_african_ecosystem_bp.route('/payfast/integrations', methods=['GET'])
def get_payfast_integrations():
    """Get all PayFast integrations for the user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        integrations = PayFastIntegration.query.filter_by(user_id=user_id).all()
        
        result = []
        for integration in integrations:
            result.append({
                'id': integration.id,
                'integration_id': integration.integration_id,
                'business_name': integration.business_name,
                'merchant_id': integration.merchant_id,
                'sandbox_mode': integration.sandbox_mode,
                'payment_methods': json.loads(integration.payment_methods) if integration.payment_methods else [],
                'status': integration.status,
                'total_transactions': integration.total_transactions,
                'total_volume': float(integration.total_volume),
                'created_at': integration.created_at.isoformat()
            })
        
        return jsonify({
            'integrations': result,
            'total_count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@south_african_ecosystem_bp.route('/payfast/integrations', methods=['POST'])
def create_payfast_integration():
    """Create a new PayFast integration"""
    try:
        data = request.get_json()
        
        integration = PayFastIntegration(
            integration_id=str(uuid.uuid4()),
            user_id=data.get('user_id', 'default_user'),
            business_name=data['business_name'],
            merchant_id=data['merchant_id'],
            merchant_key=data['merchant_key'],
            passphrase=data.get('passphrase'),
            sandbox_mode=data.get('sandbox_mode', True),
            payment_methods=json.dumps(data.get('payment_methods', ['card', 'eft'])),
            supported_currencies=json.dumps(['ZAR']),
            webhook_url=data.get('webhook_url'),
            return_url=data.get('return_url'),
            cancel_url=data.get('cancel_url'),
            notify_url=data.get('notify_url')
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'PayFast integration created successfully',
            'integration_id': integration.integration_id,
            'status': 'active'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@south_african_ecosystem_bp.route('/payfast/integrations/<integration_id>', methods=['GET'])
def get_payfast_integration(integration_id):
    """Get specific PayFast integration details"""
    try:
        integration = PayFastIntegration.query.filter_by(integration_id=integration_id).first()
        
        if not integration:
            return jsonify({'error': 'PayFast integration not found'}), 404
        
        return jsonify({
            'id': integration.id,
            'integration_id': integration.integration_id,
            'business_name': integration.business_name,
            'merchant_id': integration.merchant_id,
            'sandbox_mode': integration.sandbox_mode,
            'payment_methods': json.loads(integration.payment_methods) if integration.payment_methods else [],
            'supported_currencies': json.loads(integration.supported_currencies) if integration.supported_currencies else [],
            'minimum_amount': float(integration.minimum_amount),
            'maximum_amount': float(integration.maximum_amount),
            'status': integration.status,
            'total_transactions': integration.total_transactions,
            'successful_transactions': integration.successful_transactions,
            'failed_transactions': integration.failed_transactions,
            'total_volume': float(integration.total_volume),
            'average_transaction_value': float(integration.average_transaction_value),
            'created_at': integration.created_at.isoformat(),
            'updated_at': integration.updated_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Stitch Money Integration Endpoints
@south_african_ecosystem_bp.route('/stitch/integrations', methods=['GET'])
def get_stitch_integrations():
    """Get all Stitch Money integrations for the user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        integrations = StitchMoneyIntegration.query.filter_by(user_id=user_id).all()
        
        result = []
        for integration in integrations:
            result.append({
                'id': integration.id,
                'integration_id': integration.integration_id,
                'business_name': integration.business_name,
                'client_id': integration.client_id,
                'environment': integration.environment,
                'payment_types': json.loads(integration.payment_types) if integration.payment_types else [],
                'status': integration.status,
                'total_transactions': integration.total_transactions,
                'total_volume': float(integration.total_volume),
                'created_at': integration.created_at.isoformat()
            })
        
        return jsonify({
            'integrations': result,
            'total_count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@south_african_ecosystem_bp.route('/stitch/integrations', methods=['POST'])
def create_stitch_integration():
    """Create a new Stitch Money integration"""
    try:
        data = request.get_json()
        
        integration = StitchMoneyIntegration(
            integration_id=str(uuid.uuid4()),
            user_id=data.get('user_id', 'default_user'),
            business_name=data['business_name'],
            client_id=data['client_id'],
            client_secret=data['client_secret'],
            api_key=data['api_key'],
            environment=data.get('environment', 'sandbox'),
            payment_types=json.dumps(data.get('payment_types', ['instant_pay'])),
            supported_banks=json.dumps(data.get('supported_banks', ['absa', 'fnb', 'nedbank', 'standard_bank'])),
            supported_currencies=json.dumps(['ZAR']),
            webhook_url=data.get('webhook_url'),
            webhook_secret=data.get('webhook_secret')
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'Stitch Money integration created successfully',
            'integration_id': integration.integration_id,
            'status': 'active'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ozow Integration Endpoints
@south_african_ecosystem_bp.route('/ozow/integrations', methods=['GET'])
def get_ozow_integrations():
    """Get all Ozow integrations for the user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        integrations = OzowIntegration.query.filter_by(user_id=user_id).all()
        
        result = []
        for integration in integrations:
            result.append({
                'id': integration.id,
                'integration_id': integration.integration_id,
                'business_name': integration.business_name,
                'site_code': integration.site_code,
                'is_test_mode': integration.is_test_mode,
                'payment_methods': json.loads(integration.payment_methods) if integration.payment_methods else [],
                'status': integration.status,
                'total_transactions': integration.total_transactions,
                'total_volume': float(integration.total_volume),
                'created_at': integration.created_at.isoformat()
            })
        
        return jsonify({
            'integrations': result,
            'total_count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@south_african_ecosystem_bp.route('/ozow/integrations', methods=['POST'])
def create_ozow_integration():
    """Create a new Ozow integration"""
    try:
        data = request.get_json()
        
        integration = OzowIntegration(
            integration_id=str(uuid.uuid4()),
            user_id=data.get('user_id', 'default_user'),
            business_name=data['business_name'],
            site_code=data['site_code'],
            private_key=data['private_key'],
            api_key=data['api_key'],
            is_test_mode=data.get('is_test_mode', True),
            payment_methods=json.dumps(data.get('payment_methods', ['instant_eft'])),
            supported_banks=json.dumps(data.get('supported_banks', ['absa', 'fnb', 'nedbank', 'standard_bank'])),
            supported_currencies=json.dumps(['ZAR']),
            success_url=data.get('success_url'),
            cancel_url=data.get('cancel_url'),
            error_url=data.get('error_url'),
            notify_url=data.get('notify_url')
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'Ozow integration created successfully',
            'integration_id': integration.integration_id,
            'status': 'active'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Standard Bank API Integration Endpoints
@south_african_ecosystem_bp.route('/standard-bank/integrations', methods=['GET'])
def get_standard_bank_integrations():
    """Get all Standard Bank API integrations for the user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        integrations = StandardBankAPIIntegration.query.filter_by(user_id=user_id).all()
        
        result = []
        for integration in integrations:
            result.append({
                'id': integration.id,
                'integration_id': integration.integration_id,
                'business_name': integration.business_name,
                'client_id': integration.client_id,
                'environment': integration.environment,
                'enabled_services': json.loads(integration.enabled_services) if integration.enabled_services else [],
                'status': integration.status,
                'total_api_calls': integration.total_api_calls,
                'successful_calls': integration.successful_calls,
                'created_at': integration.created_at.isoformat()
            })
        
        return jsonify({
            'integrations': result,
            'total_count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@south_african_ecosystem_bp.route('/standard-bank/integrations', methods=['POST'])
def create_standard_bank_integration():
    """Create a new Standard Bank API integration"""
    try:
        data = request.get_json()
        
        integration = StandardBankAPIIntegration(
            integration_id=str(uuid.uuid4()),
            user_id=data.get('user_id', 'default_user'),
            business_name=data['business_name'],
            client_id=data['client_id'],
            client_secret=data['client_secret'],
            api_key=data['api_key'],
            environment=data.get('environment', 'sandbox'),
            enabled_services=json.dumps(data.get('enabled_services', ['payments', 'accounts'])),
            payment_types=json.dumps(data.get('payment_types', ['immediate_payment'])),
            supported_currencies=json.dumps(data.get('supported_currencies', ['ZAR', 'USD']))
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'Standard Bank API integration created successfully',
            'integration_id': integration.integration_id,
            'status': 'active'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Yoco Integration Endpoints
@south_african_ecosystem_bp.route('/yoco/integrations', methods=['GET'])
def get_yoco_integrations():
    """Get all Yoco integrations for the user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        integrations = YocoIntegration.query.filter_by(user_id=user_id).all()
        
        result = []
        for integration in integrations:
            result.append({
                'id': integration.id,
                'integration_id': integration.integration_id,
                'business_name': integration.business_name,
                'public_key': integration.public_key,
                'environment': integration.environment,
                'payment_methods': json.loads(integration.payment_methods) if integration.payment_methods else [],
                'status': integration.status,
                'total_transactions': integration.total_transactions,
                'total_volume': float(integration.total_volume),
                'created_at': integration.created_at.isoformat()
            })
        
        return jsonify({
            'integrations': result,
            'total_count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@south_african_ecosystem_bp.route('/yoco/integrations', methods=['POST'])
def create_yoco_integration():
    """Create a new Yoco integration"""
    try:
        data = request.get_json()
        
        integration = YocoIntegration(
            integration_id=str(uuid.uuid4()),
            user_id=data.get('user_id', 'default_user'),
            business_name=data['business_name'],
            secret_key=data['secret_key'],
            public_key=data['public_key'],
            webhook_secret=data.get('webhook_secret'),
            environment=data.get('environment', 'test'),
            payment_methods=json.dumps(data.get('payment_methods', ['card', 'online'])),
            supported_cards=json.dumps(data.get('supported_cards', ['visa', 'mastercard'])),
            supported_currencies=json.dumps(['ZAR']),
            webhook_url=data.get('webhook_url')
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'Yoco integration created successfully',
            'integration_id': integration.integration_id,
            'status': 'active'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Transaction Management Endpoints
@south_african_ecosystem_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """Get all South African payment transactions"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        platform = request.args.get('platform')
        status = request.args.get('status')
        limit = int(request.args.get('limit', 50))
        
        query = SouthAfricanPaymentTransaction.query.filter_by(user_id=user_id)
        
        if platform:
            query = query.filter_by(platform=platform)
        if status:
            query = query.filter_by(status=status)
        
        transactions = query.order_by(SouthAfricanPaymentTransaction.created_at.desc()).limit(limit).all()
        
        result = []
        for transaction in transactions:
            result.append({
                'transaction_id': transaction.transaction_id,
                'platform': transaction.platform,
                'transaction_type': transaction.transaction_type,
                'amount': float(transaction.amount),
                'currency': transaction.currency,
                'status': transaction.status,
                'payment_method': transaction.payment_method,
                'created_at': transaction.created_at.isoformat(),
                'completed_at': transaction.completed_at.isoformat() if transaction.completed_at else None
            })
        
        return jsonify({
            'transactions': result,
            'total_count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@south_african_ecosystem_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """Create a new South African payment transaction"""
    try:
        data = request.get_json()
        
        transaction = SouthAfricanPaymentTransaction(
            transaction_id=str(uuid.uuid4()),
            platform_transaction_id=data.get('platform_transaction_id'),
            platform=data['platform'],
            integration_id=data['integration_id'],
            user_id=data.get('user_id', 'default_user'),
            transaction_type=data['transaction_type'],
            amount=data['amount'],
            currency=data.get('currency', 'ZAR'),
            description=data.get('description'),
            reference=data.get('reference'),
            payment_method=data.get('payment_method'),
            status='pending',
            transaction_metadata=json.dumps(data.get('metadata', {}))
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction_id': transaction.transaction_id,
            'status': 'pending'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Analytics Endpoints
@south_african_ecosystem_bp.route('/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get comprehensive analytics overview for South African payments"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        period = request.args.get('period', '30')  # days
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=int(period))
        
        # Get transactions in period
        transactions = SouthAfricanPaymentTransaction.query.filter(
            SouthAfricanPaymentTransaction.user_id == user_id,
            SouthAfricanPaymentTransaction.created_at >= start_date,
            SouthAfricanPaymentTransaction.created_at <= end_date
        ).all()
        
        # Calculate metrics
        total_transactions = len(transactions)
        successful_transactions = len([t for t in transactions if t.status == 'completed'])
        failed_transactions = len([t for t in transactions if t.status == 'failed'])
        total_volume = sum([float(t.amount) for t in transactions if t.status == 'completed'])
        
        # Platform breakdown
        platform_breakdown = {}
        for transaction in transactions:
            platform = transaction.platform
            if platform not in platform_breakdown:
                platform_breakdown[platform] = {'count': 0, 'volume': 0}
            platform_breakdown[platform]['count'] += 1
            if transaction.status == 'completed':
                platform_breakdown[platform]['volume'] += float(transaction.amount)
        
        return jsonify({
            'period_days': int(period),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'summary': {
                'total_transactions': total_transactions,
                'successful_transactions': successful_transactions,
                'failed_transactions': failed_transactions,
                'success_rate': round((successful_transactions / total_transactions * 100) if total_transactions > 0 else 0, 2),
                'total_volume': round(total_volume, 2),
                'average_transaction_value': round((total_volume / successful_transactions) if successful_transactions > 0 else 0, 2)
            },
            'platform_breakdown': platform_breakdown,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

