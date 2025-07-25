"""
WebWaka Nigerian Payment Ecosystem Integration Models
==================================================

This module provides comprehensive database models for managing integrations
with Nigeria's extensive payment ecosystem, including digital banks, traditional
bank APIs, fintech platforms, and specialized payment services.

Nigeria is Africa's largest fintech market with 35+ payment gateways, making
this integration critical for WebWaka's continental payment dominance.

Features:
- Complete Nigerian payment gateway coverage
- Digital bank integration (Kuda, Opay, PalmPay, Carbon, etc.)
- Traditional bank API support (GTBank, Access Bank, UBA, etc.)
- Fintech platform integration (Interswitch, SystemSpecs, etc.)
- Specialized payment services (Remita, QuickTeller, etc.)
- Nigerian-specific optimization and cultural intelligence
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, JSON
from src.models.user import db
import json

# ============================================================================
# DIGITAL BANKS INTEGRATION MODELS
# ============================================================================

class KudaBankIntegration(db.Model):
    """Kuda Bank API Integration Model - Nigeria's leading digital bank"""
    __tablename__ = 'kuda_bank_integrations'
    
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # API Configuration
    client_key = Column(String(255), nullable=False)  # Should be encrypted in production
    token_url = Column(String(255), default='https://kuda-openapi.kuda.com/v2.1/Account/GetToken')
    base_url = Column(String(255), default='https://kuda-openapi.kuda.com/v2.1')
    environment = Column(String(20), default='live')  # live, sandbox
    
    # Business Information
    business_name = Column(String(100))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    business_address = Column(Text)
    
    # API Capabilities
    account_creation_enabled = Column(Boolean, default=True)
    fund_transfer_enabled = Column(Boolean, default=True)
    bill_payment_enabled = Column(Boolean, default=True)
    virtual_account_enabled = Column(Boolean, default=True)
    card_services_enabled = Column(Boolean, default=False)
    loan_services_enabled = Column(Boolean, default=False)
    
    # Transaction Limits
    daily_transaction_limit = Column(Numeric(15, 2), default=5000000.00)  # 5M NGN
    monthly_transaction_limit = Column(Numeric(15, 2), default=50000000.00)  # 50M NGN
    single_transaction_limit = Column(Numeric(15, 2), default=1000000.00)  # 1M NGN
    
    # Nigerian Optimization
    naira_optimization = Column(Boolean, default=True)
    bvn_verification_enabled = Column(Boolean, default=True)
    nin_verification_enabled = Column(Boolean, default=True)
    cbn_compliance_enabled = Column(Boolean, default=True)
    
    # Status and Metrics
    status = Column(String(20), default='active')  # active, inactive, suspended
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    total_volume = Column(Numeric(15, 2), default=0.00)
    last_transaction_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'environment': self.environment,
            'capabilities': {
                'account_creation': self.account_creation_enabled,
                'fund_transfer': self.fund_transfer_enabled,
                'bill_payment': self.bill_payment_enabled,
                'virtual_account': self.virtual_account_enabled,
                'card_services': self.card_services_enabled,
                'loan_services': self.loan_services_enabled
            },
            'limits': {
                'daily_limit': float(self.daily_transaction_limit) if self.daily_transaction_limit else None,
                'monthly_limit': float(self.monthly_transaction_limit) if self.monthly_transaction_limit else None,
                'single_limit': float(self.single_transaction_limit) if self.single_transaction_limit else None
            },
            'nigerian_features': {
                'naira_optimization': self.naira_optimization,
                'bvn_verification': self.bvn_verification_enabled,
                'nin_verification': self.nin_verification_enabled,
                'cbn_compliance': self.cbn_compliance_enabled
            },
            'metrics': {
                'status': self.status,
                'total_transactions': self.total_transactions,
                'successful_transactions': self.successful_transactions,
                'total_volume': float(self.total_volume) if self.total_volume else 0.0,
                'success_rate': (self.successful_transactions / self.total_transactions * 100) if self.total_transactions > 0 else 0
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class OpayIntegration(db.Model):
    """Opay API Integration Model - Nigeria's super app with 30M+ users"""
    __tablename__ = 'opay_integrations'
    
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # API Configuration
    merchant_id = Column(String(100), nullable=False)
    public_key = Column(String(255), nullable=False)
    private_key = Column(Text, nullable=False)  # Should be encrypted in production
    base_url = Column(String(255), default='https://sandboxapi.opayweb.com')
    environment = Column(String(20), default='sandbox')  # live, sandbox
    
    # Business Information
    business_name = Column(String(100))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    business_category = Column(String(50))
    
    # Service Configuration
    payment_enabled = Column(Boolean, default=True)
    transfer_enabled = Column(Boolean, default=True)
    inquiry_enabled = Column(Boolean, default=True)
    cashout_enabled = Column(Boolean, default=False)
    
    # Supported Services
    supported_countries = Column(Text, default='["NG"]')  # JSON array
    supported_currencies = Column(Text, default='["NGN"]')  # JSON array
    supported_channels = Column(Text, default='["account", "ussd", "qrcode", "transfer"]')
    
    # Transaction Configuration
    callback_url = Column(String(255))
    return_url = Column(String(255))
    webhook_url = Column(String(255))
    
    # Nigerian Market Features
    super_app_integration = Column(Boolean, default=True)
    ride_hailing_payments = Column(Boolean, default=False)
    food_delivery_payments = Column(Boolean, default=False)
    bill_payment_services = Column(Boolean, default=True)
    
    # Status and Metrics
    status = Column(String(20), default='active')
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    total_volume = Column(Numeric(15, 2), default=0.00)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'merchant_id': self.merchant_id,
            'business_name': self.business_name,
            'environment': self.environment,
            'services': {
                'payment': self.payment_enabled,
                'transfer': self.transfer_enabled,
                'inquiry': self.inquiry_enabled,
                'cashout': self.cashout_enabled
            },
            'supported_countries': json.loads(self.supported_countries) if self.supported_countries else [],
            'supported_currencies': json.loads(self.supported_currencies) if self.supported_currencies else [],
            'supported_channels': json.loads(self.supported_channels) if self.supported_channels else [],
            'super_app_features': {
                'integration': self.super_app_integration,
                'ride_hailing': self.ride_hailing_payments,
                'food_delivery': self.food_delivery_payments,
                'bill_payment': self.bill_payment_services
            },
            'metrics': {
                'status': self.status,
                'total_transactions': self.total_transactions,
                'successful_transactions': self.successful_transactions,
                'total_volume': float(self.total_volume) if self.total_volume else 0.0
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ============================================================================
# TRADITIONAL BANK API INTEGRATION MODELS
# ============================================================================

class GTBankIntegration(db.Model):
    """GTBank API Integration Model - Nigeria's leading traditional bank"""
    __tablename__ = 'gtbank_integrations'
    
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # API Configuration
    client_id = Column(String(100), nullable=False)
    client_secret = Column(String(255), nullable=False)  # Should be encrypted
    subscription_key = Column(String(255), nullable=False)
    base_url = Column(String(255), default='https://api.gtbank.com')
    environment = Column(String(20), default='sandbox')
    
    # Business Information
    business_name = Column(String(100))
    business_account_number = Column(String(20))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    
    # API Services
    account_services_enabled = Column(Boolean, default=True)
    transfer_services_enabled = Column(Boolean, default=True)
    bill_payment_enabled = Column(Boolean, default=True)
    statement_services_enabled = Column(Boolean, default=True)
    
    # GTBank Specific Features
    gtworld_integration = Column(Boolean, default=False)
    gtpay_integration = Column(Boolean, default=True)
    quickteller_integration = Column(Boolean, default=True)
    
    # Status and Metrics
    status = Column(String(20), default='active')
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'business_account_number': self.business_account_number,
            'environment': self.environment,
            'services': {
                'account_services': self.account_services_enabled,
                'transfer_services': self.transfer_services_enabled,
                'bill_payment': self.bill_payment_enabled,
                'statement_services': self.statement_services_enabled
            },
            'gtbank_features': {
                'gtworld': self.gtworld_integration,
                'gtpay': self.gtpay_integration,
                'quickteller': self.quickteller_integration
            },
            'metrics': {
                'status': self.status,
                'total_transactions': self.total_transactions,
                'successful_transactions': self.successful_transactions
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ============================================================================
# FINTECH PLATFORM INTEGRATION MODELS
# ============================================================================

class InterswitchIntegration(db.Model):
    """Interswitch API Integration Model - Nigeria's payment infrastructure leader"""
    __tablename__ = 'interswitch_integrations'
    
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # API Configuration
    client_id = Column(String(100), nullable=False)
    client_secret = Column(String(255), nullable=False)
    merchant_code = Column(String(50))
    base_url = Column(String(255), default='https://sandbox.interswitchng.com')
    environment = Column(String(20), default='sandbox')
    
    # Product Configuration
    webpay_enabled = Column(Boolean, default=True)
    paydirect_enabled = Column(Boolean, default=True)
    quickteller_enabled = Column(Boolean, default=True)
    verve_card_enabled = Column(Boolean, default=True)
    
    # Business Information
    business_name = Column(String(100))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    
    # Nigerian Infrastructure Features
    nibss_integration = Column(Boolean, default=True)
    cbn_compliance = Column(Boolean, default=True)
    verve_network_access = Column(Boolean, default=True)
    
    # Status and Metrics
    status = Column(String(20), default='active')
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'merchant_code': self.merchant_code,
            'business_name': self.business_name,
            'environment': self.environment,
            'products': {
                'webpay': self.webpay_enabled,
                'paydirect': self.paydirect_enabled,
                'quickteller': self.quickteller_enabled,
                'verve_card': self.verve_card_enabled
            },
            'infrastructure_features': {
                'nibss_integration': self.nibss_integration,
                'cbn_compliance': self.cbn_compliance,
                'verve_network': self.verve_network_access
            },
            'metrics': {
                'status': self.status,
                'total_transactions': self.total_transactions,
                'successful_transactions': self.successful_transactions
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RemitaIntegration(db.Model):
    """Remita API Integration Model - Nigeria's e-billing and payment platform"""
    __tablename__ = 'remita_integrations'
    
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # API Configuration
    merchant_id = Column(String(100), nullable=False)
    api_key = Column(String(255), nullable=False)
    api_token = Column(String(255), nullable=False)
    service_type_id = Column(String(50))
    base_url = Column(String(255), default='https://remitademo.net')
    environment = Column(String(20), default='demo')
    
    # Service Configuration
    single_payment_enabled = Column(Boolean, default=True)
    bulk_payment_enabled = Column(Boolean, default=True)
    salary_payment_enabled = Column(Boolean, default=False)
    loan_disbursement_enabled = Column(Boolean, default=False)
    
    # Business Information
    business_name = Column(String(100))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    
    # Government Integration Features
    treasury_single_account = Column(Boolean, default=False)  # TSA integration
    government_payments = Column(Boolean, default=False)
    tax_payment_services = Column(Boolean, default=False)
    
    # Status and Metrics
    status = Column(String(20), default='active')
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'merchant_id': self.merchant_id,
            'service_type_id': self.service_type_id,
            'business_name': self.business_name,
            'environment': self.environment,
            'services': {
                'single_payment': self.single_payment_enabled,
                'bulk_payment': self.bulk_payment_enabled,
                'salary_payment': self.salary_payment_enabled,
                'loan_disbursement': self.loan_disbursement_enabled
            },
            'government_features': {
                'tsa_integration': self.treasury_single_account,
                'government_payments': self.government_payments,
                'tax_services': self.tax_payment_services
            },
            'metrics': {
                'status': self.status,
                'total_transactions': self.total_transactions,
                'successful_transactions': self.successful_transactions
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ============================================================================
# UNIFIED NIGERIAN TRANSACTION MODEL
# ============================================================================

class NigerianPaymentTransaction(db.Model):
    """Unified transaction model for all Nigerian payment platforms"""
    __tablename__ = 'nigerian_payment_transactions'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Platform Information
    platform = Column(String(50), nullable=False, index=True)  # kuda, opay, gtbank, interswitch, remita, etc.
    platform_integration_id = Column(String(100), nullable=False, index=True)
    external_transaction_id = Column(String(100), index=True)
    reference = Column(String(100), nullable=False, index=True)
    
    # Transaction Details
    description = Column(Text)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), default='NGN')
    payment_method = Column(String(50), nullable=False)  # account, card, ussd, transfer, etc.
    payment_channel = Column(String(50))  # web, mobile, api, ussd, etc.
    
    # Customer Information
    customer_id = Column(String(100))
    customer_email = Column(String(100))
    customer_phone = Column(String(20))
    customer_name = Column(String(100))
    customer_bvn = Column(String(11))  # Nigerian BVN
    customer_nin = Column(String(11))  # Nigerian NIN
    
    # Nigerian Specific Fields
    bank_code = Column(String(10))  # Nigerian bank codes
    account_number = Column(String(20))
    account_name = Column(String(100))
    narration = Column(String(255))
    
    # Transaction Status
    status = Column(String(20), default='Pending', index=True)  # Pending, Processing, Success, Failed, Cancelled
    platform_status = Column(String(50))
    failure_reason = Column(Text)
    
    # Timing Information
    initiated_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    completed_at = Column(DateTime)
    response_time = Column(Integer)  # Response time in milliseconds
    
    # Financial Information
    platform_fee = Column(Numeric(10, 2), default=0.00)
    gateway_fee = Column(Numeric(10, 2), default=0.00)
    total_fees = Column(Numeric(10, 2), default=0.00)
    net_amount = Column(Numeric(15, 2))
    
    # Platform Response Data
    platform_request_data = Column(Text)  # JSON string
    platform_response_data = Column(Text)  # JSON string
    platform_callback_data = Column(Text)  # JSON string
    
    # Metadata
    ip_address = Column(String(45))
    user_agent = Column(Text)
    transaction_metadata = Column(Text)  # JSON string for additional metadata
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'platform': self.platform,
            'platform_integration_id': self.platform_integration_id,
            'external_transaction_id': self.external_transaction_id,
            'reference': self.reference,
            'description': self.description,
            'amount': float(self.amount) if self.amount else None,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'payment_channel': self.payment_channel,
            'customer': {
                'id': self.customer_id,
                'email': self.customer_email,
                'phone': self.customer_phone,
                'name': self.customer_name,
                'bvn': self.customer_bvn,
                'nin': self.customer_nin
            },
            'nigerian_details': {
                'bank_code': self.bank_code,
                'account_number': self.account_number,
                'account_name': self.account_name,
                'narration': self.narration
            },
            'status': {
                'current': self.status,
                'platform_status': self.platform_status,
                'failure_reason': self.failure_reason
            },
            'timing': {
                'initiated_at': self.initiated_at.isoformat() if self.initiated_at else None,
                'processed_at': self.processed_at.isoformat() if self.processed_at else None,
                'completed_at': self.completed_at.isoformat() if self.completed_at else None,
                'response_time': self.response_time
            },
            'financial': {
                'platform_fee': float(self.platform_fee) if self.platform_fee else 0.0,
                'gateway_fee': float(self.gateway_fee) if self.gateway_fee else 0.0,
                'total_fees': float(self.total_fees) if self.total_fees else 0.0,
                'net_amount': float(self.net_amount) if self.net_amount else None
            },
            'metadata': {
                'ip_address': self.ip_address,
                'user_agent': self.user_agent,
                'additional_data': json.loads(self.metadata) if self.metadata else {}
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ============================================================================
# NIGERIAN PAYMENT ANALYTICS MODEL
# ============================================================================

class NigerianPaymentAnalytics(db.Model):
    """Analytics model for Nigerian payment ecosystem performance"""
    __tablename__ = 'nigerian_payment_analytics'
    
    id = Column(Integer, primary_key=True)
    analytics_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Time Period
    date = Column(DateTime, nullable=False, index=True)
    period_type = Column(String(20), default='daily')  # hourly, daily, weekly, monthly
    
    # Platform Performance
    platform = Column(String(50), nullable=False, index=True)
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    failed_transactions = Column(Integer, default=0)
    total_volume = Column(Numeric(15, 2), default=0.00)
    
    # Performance Metrics
    success_rate = Column(Numeric(5, 2), default=0.00)  # Percentage
    average_response_time = Column(Integer, default=0)  # Milliseconds
    uptime_percentage = Column(Numeric(5, 2), default=100.00)
    
    # Nigerian Market Metrics
    naira_volume = Column(Numeric(15, 2), default=0.00)
    bank_transfer_volume = Column(Numeric(15, 2), default=0.00)
    card_payment_volume = Column(Numeric(15, 2), default=0.00)
    ussd_transaction_count = Column(Integer, default=0)
    
    # User Engagement
    unique_customers = Column(Integer, default=0)
    returning_customers = Column(Integer, default=0)
    new_customers = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'analytics_id': self.analytics_id,
            'date': self.date.isoformat() if self.date else None,
            'period_type': self.period_type,
            'platform': self.platform,
            'transactions': {
                'total': self.total_transactions,
                'successful': self.successful_transactions,
                'failed': self.failed_transactions,
                'total_volume': float(self.total_volume) if self.total_volume else 0.0
            },
            'performance': {
                'success_rate': float(self.success_rate) if self.success_rate else 0.0,
                'average_response_time': self.average_response_time,
                'uptime_percentage': float(self.uptime_percentage) if self.uptime_percentage else 100.0
            },
            'nigerian_metrics': {
                'naira_volume': float(self.naira_volume) if self.naira_volume else 0.0,
                'bank_transfer_volume': float(self.bank_transfer_volume) if self.bank_transfer_volume else 0.0,
                'card_payment_volume': float(self.card_payment_volume) if self.card_payment_volume else 0.0,
                'ussd_transactions': self.ussd_transaction_count
            },
            'customers': {
                'unique': self.unique_customers,
                'returning': self.returning_customers,
                'new': self.new_customers
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

