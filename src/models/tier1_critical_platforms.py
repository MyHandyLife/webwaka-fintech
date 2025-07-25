"""
WebWaka Tier 1 Critical African Payment Platform Integration Models
================================================================

This module contains specialized integration models for the most critical
African payment platforms: M-Pesa, MTN Mobile Money, Paystack, Flutterwave,
and Hubtel. These are the Tier 1 platforms that form the foundation of
African digital payments.

Features:
- M-Pesa Daraja API integration (Kenya's leading mobile money)
- MTN Mobile Money API integration (17+ countries, 900+ partners)
- Paystack API integration (Nigeria's leading payment gateway)
- Flutterwave API integration (34+ countries, 1M+ businesses)
- Hubtel API integration (Ghana's leading payment aggregator)
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime
import json
import uuid

# Import shared database instance
from src.models.user import db

class MPesaIntegration(db.Model):
    """
    M-Pesa Daraja API Integration Model
    
    Manages M-Pesa integrations with comprehensive support for all
    Daraja API endpoints including STK Push, C2B, B2C, and B2B.
    """
    __tablename__ = 'mpesa_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # M-Pesa specific configuration
    business_short_code = db.Column(db.String(20), nullable=False)  # Paybill or Till number
    consumer_key = db.Column(db.String(200), nullable=False)  # Encrypted
    consumer_secret = db.Column(db.String(200), nullable=False)  # Encrypted
    passkey = db.Column(db.String(200))  # For STK Push, encrypted
    
    # Environment and URLs
    environment = db.Column(db.String(20), default='sandbox')  # sandbox, production
    base_url = db.Column(db.String(200), default='https://sandbox.safaricom.co.ke')
    callback_url = db.Column(db.String(500))
    result_url = db.Column(db.String(500))
    timeout_url = db.Column(db.String(500))
    
    # API endpoints enabled
    stk_push_enabled = db.Column(db.Boolean, default=True)
    c2b_enabled = db.Column(db.Boolean, default=False)
    b2c_enabled = db.Column(db.Boolean, default=False)
    b2b_enabled = db.Column(db.Boolean, default=False)
    account_balance_enabled = db.Column(db.Boolean, default=False)
    transaction_status_enabled = db.Column(db.Boolean, default=True)
    reversal_enabled = db.Column(db.Boolean, default=False)
    
    # Transaction limits
    minimum_amount = db.Column(Numeric(10, 2), default=1.00)
    maximum_amount = db.Column(Numeric(10, 2), default=70000.00)
    daily_limit = db.Column(Numeric(15, 2), default=300000.00)
    monthly_limit = db.Column(Numeric(15, 2), default=6000000.00)
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(Numeric(15, 2), default=0.00)
    success_rate = db.Column(db.Float, default=0.0)
    average_response_time = db.Column(db.Integer, default=0)  # milliseconds
    
    # Status and health
    status = db.Column(db.String(20), default='Active')
    health_status = db.Column(db.String(20), default='Unknown')
    last_health_check = db.Column(db.DateTime)
    last_successful_transaction = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MPesaIntegration {self.integration_id} ({self.business_short_code})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses (excluding sensitive data)"""
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'business_short_code': self.business_short_code,
            'environment': self.environment,
            'stk_push_enabled': self.stk_push_enabled,
            'c2b_enabled': self.c2b_enabled,
            'b2c_enabled': self.b2c_enabled,
            'b2b_enabled': self.b2b_enabled,
            'minimum_amount': float(self.minimum_amount) if self.minimum_amount else 0.0,
            'maximum_amount': float(self.maximum_amount) if self.maximum_amount else 0.0,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'success_rate': self.success_rate,
            'status': self.status,
            'health_status': self.health_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MTNMoMoIntegration(db.Model):
    """
    MTN Mobile Money API Integration Model
    
    Manages MTN MoMo integrations with support for Collections,
    Disbursements, and Remittances across 17+ African countries.
    """
    __tablename__ = 'mtn_momo_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # MTN MoMo specific configuration
    subscription_key = db.Column(db.String(200), nullable=False)  # Encrypted
    api_user_id = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(200), nullable=False)  # Encrypted
    target_environment = db.Column(db.String(50), default='sandbox')  # sandbox, mtnrwanda, mtnuganda, etc.
    
    # Environment and URLs
    environment = db.Column(db.String(20), default='sandbox')  # sandbox, production
    base_url = db.Column(db.String(200), default='https://sandbox.momodeveloper.mtn.com')
    callback_host = db.Column(db.String(200))  # For webhook callbacks
    
    # Product subscriptions
    collections_enabled = db.Column(db.Boolean, default=True)  # Request to pay
    disbursements_enabled = db.Column(db.Boolean, default=False)  # Transfer to users
    remittances_enabled = db.Column(db.Boolean, default=False)  # Cross-border transfers
    
    # Country and currency configuration
    country_code = db.Column(db.String(3), default='UG')  # ISO country code
    currency = db.Column(db.String(3), default='UGX')  # Primary currency
    supported_countries = db.Column(db.Text)  # JSON array of supported countries
    
    # Transaction limits
    minimum_amount = db.Column(Numeric(10, 2), default=100.00)
    maximum_amount = db.Column(Numeric(10, 2), default=5000000.00)
    daily_limit = db.Column(Numeric(15, 2), default=10000000.00)
    monthly_limit = db.Column(Numeric(15, 2), default=50000000.00)
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(Numeric(15, 2), default=0.00)
    success_rate = db.Column(db.Float, default=0.0)
    average_response_time = db.Column(db.Integer, default=0)  # milliseconds
    
    # Status and health
    status = db.Column(db.String(20), default='Active')
    health_status = db.Column(db.String(20), default='Unknown')
    last_health_check = db.Column(db.DateTime)
    last_successful_transaction = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MTNMoMoIntegration {self.integration_id} ({self.country_code})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses (excluding sensitive data)"""
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'target_environment': self.target_environment,
            'environment': self.environment,
            'collections_enabled': self.collections_enabled,
            'disbursements_enabled': self.disbursements_enabled,
            'remittances_enabled': self.remittances_enabled,
            'country_code': self.country_code,
            'currency': self.currency,
            'supported_countries': json.loads(self.supported_countries) if self.supported_countries else [],
            'minimum_amount': float(self.minimum_amount) if self.minimum_amount else 0.0,
            'maximum_amount': float(self.maximum_amount) if self.maximum_amount else 0.0,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'success_rate': self.success_rate,
            'status': self.status,
            'health_status': self.health_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PaystackIntegration(db.Model):
    """
    Paystack API Integration Model
    
    Manages Paystack integrations with comprehensive support for
    payments, transfers, subscriptions, and multi-country operations.
    """
    __tablename__ = 'paystack_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Paystack specific configuration
    public_key = db.Column(db.String(200), nullable=False)
    secret_key = db.Column(db.String(200), nullable=False)  # Encrypted
    webhook_secret = db.Column(db.String(200))  # Encrypted
    
    # Environment and URLs
    environment = db.Column(db.String(20), default='test')  # test, live
    base_url = db.Column(db.String(200), default='https://api.paystack.co')
    webhook_url = db.Column(db.String(500))
    
    # Business configuration
    business_name = db.Column(db.String(200))
    business_email = db.Column(db.String(200))
    business_phone = db.Column(db.String(20))
    settlement_bank = db.Column(db.String(100))
    settlement_account = db.Column(db.String(20))
    
    # Features enabled
    payments_enabled = db.Column(db.Boolean, default=True)
    transfers_enabled = db.Column(db.Boolean, default=False)
    subscriptions_enabled = db.Column(db.Boolean, default=False)
    invoices_enabled = db.Column(db.Boolean, default=False)
    payment_pages_enabled = db.Column(db.Boolean, default=False)
    
    # Payment methods
    card_payments_enabled = db.Column(db.Boolean, default=True)
    bank_transfer_enabled = db.Column(db.Boolean, default=True)
    ussd_enabled = db.Column(db.Boolean, default=True)
    qr_enabled = db.Column(db.Boolean, default=True)
    mobile_money_enabled = db.Column(db.Boolean, default=True)
    
    # Country and currency configuration
    primary_country = db.Column(db.String(3), default='NG')  # NG, GH, ZA, KE
    primary_currency = db.Column(db.String(3), default='NGN')
    supported_countries = db.Column(db.Text)  # JSON array
    supported_currencies = db.Column(db.Text)  # JSON array
    
    # Transaction limits and fees
    minimum_amount = db.Column(Numeric(10, 2), default=50.00)  # NGN 50
    maximum_amount = db.Column(Numeric(15, 2), default=50000000.00)  # NGN 50M
    transaction_fee_percentage = db.Column(db.Float, default=1.5)  # 1.5%
    transaction_fee_cap = db.Column(Numeric(10, 2), default=2000.00)  # NGN 2000
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(Numeric(15, 2), default=0.00)
    total_fees_paid = db.Column(Numeric(15, 2), default=0.00)
    success_rate = db.Column(db.Float, default=0.0)
    average_response_time = db.Column(db.Integer, default=0)  # milliseconds
    
    # Status and health
    status = db.Column(db.String(20), default='Active')
    health_status = db.Column(db.String(20), default='Unknown')
    last_health_check = db.Column(db.DateTime)
    last_successful_transaction = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaystackIntegration {self.integration_id} ({self.primary_country})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses (excluding sensitive data)"""
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'environment': self.environment,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'payments_enabled': self.payments_enabled,
            'transfers_enabled': self.transfers_enabled,
            'subscriptions_enabled': self.subscriptions_enabled,
            'card_payments_enabled': self.card_payments_enabled,
            'bank_transfer_enabled': self.bank_transfer_enabled,
            'mobile_money_enabled': self.mobile_money_enabled,
            'primary_country': self.primary_country,
            'primary_currency': self.primary_currency,
            'supported_countries': json.loads(self.supported_countries) if self.supported_countries else [],
            'supported_currencies': json.loads(self.supported_currencies) if self.supported_currencies else [],
            'minimum_amount': float(self.minimum_amount) if self.minimum_amount else 0.0,
            'maximum_amount': float(self.maximum_amount) if self.maximum_amount else 0.0,
            'transaction_fee_percentage': self.transaction_fee_percentage,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'success_rate': self.success_rate,
            'status': self.status,
            'health_status': self.health_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class FlutterwaveIntegration(db.Model):
    """
    Flutterwave API Integration Model
    
    Manages Flutterwave integrations with support for payments,
    transfers, and multi-country operations across 34+ countries.
    """
    __tablename__ = 'flutterwave_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Flutterwave specific configuration
    public_key = db.Column(db.String(200), nullable=False)
    secret_key = db.Column(db.String(200), nullable=False)  # Encrypted
    encryption_key = db.Column(db.String(200), nullable=False)  # Encrypted
    webhook_secret_hash = db.Column(db.String(200))  # Encrypted
    
    # Environment and URLs
    environment = db.Column(db.String(20), default='staging')  # staging, live
    base_url = db.Column(db.String(200), default='https://api.flutterwave.com/v3')
    webhook_url = db.Column(db.String(500))
    redirect_url = db.Column(db.String(500))
    
    # Business configuration
    business_name = db.Column(db.String(200))
    business_email = db.Column(db.String(200))
    business_logo = db.Column(db.String(500))
    business_description = db.Column(db.Text)
    
    # Features enabled
    standard_payments_enabled = db.Column(db.Boolean, default=True)
    inline_payments_enabled = db.Column(db.Boolean, default=True)
    transfers_enabled = db.Column(db.Boolean, default=False)
    bills_enabled = db.Column(db.Boolean, default=False)
    subscriptions_enabled = db.Column(db.Boolean, default=False)
    payment_plans_enabled = db.Column(db.Boolean, default=False)
    
    # Payment methods
    card_payments_enabled = db.Column(db.Boolean, default=True)
    bank_transfer_enabled = db.Column(db.Boolean, default=True)
    ussd_enabled = db.Column(db.Boolean, default=True)
    mobile_money_enabled = db.Column(db.Boolean, default=True)
    qr_enabled = db.Column(db.Boolean, default=True)
    voucher_enabled = db.Column(db.Boolean, default=False)
    
    # Multi-country configuration
    primary_country = db.Column(db.String(3), default='NG')
    primary_currency = db.Column(db.String(3), default='NGN')
    supported_countries = db.Column(db.Text)  # JSON array of 34+ countries
    supported_currencies = db.Column(db.Text)  # JSON array of currencies
    
    # Transaction configuration
    minimum_amount = db.Column(Numeric(10, 2), default=1.00)
    maximum_amount = db.Column(Numeric(15, 2), default=100000000.00)
    transaction_fee_percentage = db.Column(db.Float, default=1.4)  # 1.4%
    international_fee_percentage = db.Column(db.Float, default=3.8)  # 3.8%
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(Numeric(15, 2), default=0.00)
    total_fees_paid = db.Column(Numeric(15, 2), default=0.00)
    success_rate = db.Column(db.Float, default=0.0)
    average_response_time = db.Column(db.Integer, default=0)  # milliseconds
    
    # Status and health
    status = db.Column(db.String(20), default='Active')
    health_status = db.Column(db.String(20), default='Unknown')
    last_health_check = db.Column(db.DateTime)
    last_successful_transaction = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<FlutterwaveIntegration {self.integration_id} ({self.primary_country})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses (excluding sensitive data)"""
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'environment': self.environment,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'standard_payments_enabled': self.standard_payments_enabled,
            'inline_payments_enabled': self.inline_payments_enabled,
            'transfers_enabled': self.transfers_enabled,
            'card_payments_enabled': self.card_payments_enabled,
            'bank_transfer_enabled': self.bank_transfer_enabled,
            'mobile_money_enabled': self.mobile_money_enabled,
            'primary_country': self.primary_country,
            'primary_currency': self.primary_currency,
            'supported_countries': json.loads(self.supported_countries) if self.supported_countries else [],
            'supported_currencies': json.loads(self.supported_currencies) if self.supported_currencies else [],
            'minimum_amount': float(self.minimum_amount) if self.minimum_amount else 0.0,
            'maximum_amount': float(self.maximum_amount) if self.maximum_amount else 0.0,
            'transaction_fee_percentage': self.transaction_fee_percentage,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'success_rate': self.success_rate,
            'status': self.status,
            'health_status': self.health_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class HubtelIntegration(db.Model):
    """
    Hubtel API Integration Model
    
    Manages Hubtel integrations with comprehensive support for
    Ghana's leading payment aggregator and multi-channel solutions.
    """
    __tablename__ = 'hubtel_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Hubtel specific configuration
    client_id = db.Column(db.String(200), nullable=False)
    client_secret = db.Column(db.String(200), nullable=False)  # Encrypted
    merchant_account_number = db.Column(db.String(50))
    api_key = db.Column(db.String(200))  # Encrypted
    
    # Environment and URLs
    environment = db.Column(db.String(20), default='sandbox')  # sandbox, live
    base_url = db.Column(db.String(200), default='https://api-sandbox.hubtel.com')
    callback_url = db.Column(db.String(500))
    return_url = db.Column(db.String(500))
    cancellation_url = db.Column(db.String(500))
    
    # Business configuration
    business_name = db.Column(db.String(200))
    business_email = db.Column(db.String(200))
    business_phone = db.Column(db.String(20))
    business_website = db.Column(db.String(200))
    
    # Features enabled
    receive_money_enabled = db.Column(db.Boolean, default=True)
    send_money_enabled = db.Column(db.Boolean, default=False)
    checkout_enabled = db.Column(db.Boolean, default=True)
    direct_pay_enabled = db.Column(db.Boolean, default=True)
    recurring_enabled = db.Column(db.Boolean, default=False)
    
    # Payment channels
    mobile_money_enabled = db.Column(db.Boolean, default=True)  # MTN, Vodafone, AirtelTigo
    card_payments_enabled = db.Column(db.Boolean, default=True)
    bank_payments_enabled = db.Column(db.Boolean, default=True)
    ussd_enabled = db.Column(db.Boolean, default=True)
    
    # Mobile money networks
    mtn_enabled = db.Column(db.Boolean, default=True)
    vodafone_enabled = db.Column(db.Boolean, default=True)
    airteltigo_enabled = db.Column(db.Boolean, default=True)
    
    # Country and currency (Ghana focus)
    country_code = db.Column(db.String(3), default='GH')
    primary_currency = db.Column(db.String(3), default='GHS')
    supported_currencies = db.Column(db.Text)  # JSON array
    
    # Transaction limits and fees
    minimum_amount = db.Column(Numeric(10, 2), default=1.00)  # GHS 1
    maximum_amount = db.Column(Numeric(15, 2), default=10000.00)  # GHS 10,000
    transaction_fee_percentage = db.Column(db.Float, default=1.95)  # 1.95%
    mobile_money_fee_percentage = db.Column(db.Float, default=1.0)  # 1.0%
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(Numeric(15, 2), default=0.00)
    total_fees_paid = db.Column(Numeric(15, 2), default=0.00)
    success_rate = db.Column(db.Float, default=0.0)
    average_response_time = db.Column(db.Integer, default=0)  # milliseconds
    
    # Status and health
    status = db.Column(db.String(20), default='Active')
    health_status = db.Column(db.String(20), default='Unknown')
    last_health_check = db.Column(db.DateTime)
    last_successful_transaction = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<HubtelIntegration {self.integration_id} ({self.merchant_account_number})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses (excluding sensitive data)"""
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'merchant_account_number': self.merchant_account_number,
            'environment': self.environment,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'receive_money_enabled': self.receive_money_enabled,
            'send_money_enabled': self.send_money_enabled,
            'checkout_enabled': self.checkout_enabled,
            'mobile_money_enabled': self.mobile_money_enabled,
            'card_payments_enabled': self.card_payments_enabled,
            'mtn_enabled': self.mtn_enabled,
            'vodafone_enabled': self.vodafone_enabled,
            'airteltigo_enabled': self.airteltigo_enabled,
            'country_code': self.country_code,
            'primary_currency': self.primary_currency,
            'supported_currencies': json.loads(self.supported_currencies) if self.supported_currencies else [],
            'minimum_amount': float(self.minimum_amount) if self.minimum_amount else 0.0,
            'maximum_amount': float(self.maximum_amount) if self.maximum_amount else 0.0,
            'transaction_fee_percentage': self.transaction_fee_percentage,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'success_rate': self.success_rate,
            'status': self.status,
            'health_status': self.health_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Tier1Transaction(db.Model):
    """
    Tier 1 Platform Transaction Model
    
    Specialized transaction model for tracking transactions across
    all Tier 1 critical platforms with platform-specific metadata.
    """
    __tablename__ = 'tier1_transactions'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    platform = db.Column(db.String(20), nullable=False, index=True)  # mpesa, mtn_momo, paystack, flutterwave, hubtel
    platform_integration_id = db.Column(db.String(100), nullable=False, index=True)
    
    # Transaction details
    external_transaction_id = db.Column(db.String(200))  # Platform's transaction ID
    reference = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Payment information
    amount = db.Column(Numeric(15, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_channel = db.Column(db.String(50))
    
    # Customer information
    customer_id = db.Column(db.String(100))
    customer_email = db.Column(db.String(200))
    customer_phone = db.Column(db.String(20))
    customer_name = db.Column(db.String(200))
    
    # Platform-specific data
    platform_request_data = db.Column(db.Text)  # JSON object with platform request
    platform_response_data = db.Column(db.Text)  # JSON object with platform response
    platform_callback_data = db.Column(db.Text)  # JSON object with callback data
    
    # Transaction status and flow
    status = db.Column(db.String(20), default='Pending')  # Pending, Processing, Success, Failed, Cancelled
    platform_status = db.Column(db.String(50))  # Platform-specific status
    failure_reason = db.Column(db.Text)
    
    # Timing information
    initiated_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    response_time = db.Column(db.Integer)  # milliseconds
    
    # Fees and charges
    platform_fee = db.Column(Numeric(10, 4), default=0.0000)
    gateway_fee = db.Column(Numeric(10, 4), default=0.0000)
    total_fees = db.Column(Numeric(10, 4), default=0.0000)
    net_amount = db.Column(Numeric(15, 2))
    
    # Geographic and network context
    country_code = db.Column(db.String(3), nullable=False)
    mobile_network = db.Column(db.String(50))  # For mobile money transactions
    bank_code = db.Column(db.String(20))  # For bank transactions
    
    # Audit trail
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tier1Transaction {self.transaction_id} ({self.platform})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'platform': self.platform,
            'platform_integration_id': self.platform_integration_id,
            'external_transaction_id': self.external_transaction_id,
            'reference': self.reference,
            'description': self.description,
            'amount': float(self.amount) if self.amount else 0.0,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'payment_channel': self.payment_channel,
            'customer_id': self.customer_id,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'customer_name': self.customer_name,
            'status': self.status,
            'platform_status': self.platform_status,
            'failure_reason': self.failure_reason,
            'country_code': self.country_code,
            'mobile_network': self.mobile_network,
            'bank_code': self.bank_code,
            'platform_fee': float(self.platform_fee) if self.platform_fee else 0.0,
            'gateway_fee': float(self.gateway_fee) if self.gateway_fee else 0.0,
            'total_fees': float(self.total_fees) if self.total_fees else 0.0,
            'net_amount': float(self.net_amount) if self.net_amount else 0.0,
            'response_time': self.response_time,
            'initiated_at': self.initiated_at.isoformat() if self.initiated_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

