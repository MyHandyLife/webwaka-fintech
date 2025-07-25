"""
WebWaka South African Payment Ecosystem Integration Models
========================================================

This module contains the database models for South African payment gateway
integrations, representing the most sophisticated financial market in Africa.

South Africa Features:
- Most advanced banking APIs in Africa
- 85%+ banking penetration (highest in Africa)
- Leading fintech innovation hub
- Open banking development by FSCA
- Enterprise-grade payment solutions

Supported Platforms:
- PayFast (South Africa's leading payment processor)
- Stitch Money (Enterprise payment solutions)
- Ozow (Instant EFT specialist)
- Standard Bank API Marketplace
- Nedbank API Platform
- Absa Bank APIs
- FNB APIs
- Capitec Bank APIs
- Yoco (SME payment solutions)
- SnapScan (QR code payments)
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime
import json

# Import shared database instance
from src.models.user import db

class PayFastIntegration(db.Model):
    """
    PayFast Integration Model
    
    PayFast is South Africa's leading payment processor with 70+ plugin
    integrations and comprehensive payment solutions.
    """
    __tablename__ = 'payfast_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    business_name = db.Column(db.String(200), nullable=False)
    
    # PayFast configuration
    merchant_id = db.Column(db.String(100), nullable=False)
    merchant_key = db.Column(db.String(200), nullable=False)
    passphrase = db.Column(db.String(200))  # Optional passphrase
    sandbox_mode = db.Column(db.Boolean, default=True)
    
    # Payment configuration
    payment_methods = db.Column(db.Text)  # JSON: ['card', 'eft', 'instant_eft', 'bitcoin', 'mobicred', 'rcs']
    supported_currencies = db.Column(db.Text)  # JSON: ['ZAR']
    minimum_amount = db.Column(db.Numeric(10, 2), default=5.00)  # R5.00 minimum
    maximum_amount = db.Column(db.Numeric(12, 2), default=1000000.00)  # R1M maximum
    
    # South African specific features
    vat_number = db.Column(db.String(50))  # South African VAT number
    company_registration = db.Column(db.String(50))  # Company registration number
    bank_account_details = db.Column(db.Text)  # JSON: bank account information
    settlement_period = db.Column(db.String(20), default='T+2')  # Settlement period
    
    # API configuration
    api_version = db.Column(db.String(20), default='v1')
    webhook_url = db.Column(db.String(500))
    return_url = db.Column(db.String(500))
    cancel_url = db.Column(db.String(500))
    notify_url = db.Column(db.String(500))
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(db.Numeric(15, 2), default=0.00)
    average_transaction_value = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Status and timestamps
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_transaction_at = db.Column(db.DateTime)

class StitchMoneyIntegration(db.Model):
    """
    Stitch Money Integration Model
    
    Stitch Money provides enterprise payment solutions with real-time
    bank APIs and advanced payment processing capabilities.
    """
    __tablename__ = 'stitch_money_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    business_name = db.Column(db.String(200), nullable=False)
    
    # Stitch Money configuration
    client_id = db.Column(db.String(100), nullable=False)
    client_secret = db.Column(db.String(200), nullable=False)
    api_key = db.Column(db.String(200), nullable=False)
    environment = db.Column(db.String(20), default='sandbox')  # sandbox, production
    
    # Payment configuration
    payment_types = db.Column(db.Text)  # JSON: ['instant_pay', 'debit_order', 'refund']
    supported_banks = db.Column(db.Text)  # JSON: ['absa', 'fnb', 'nedbank', 'standard_bank', 'capitec']
    supported_currencies = db.Column(db.Text)  # JSON: ['ZAR']
    minimum_amount = db.Column(db.Numeric(10, 2), default=1.00)  # R1.00 minimum
    maximum_amount = db.Column(db.Numeric(12, 2), default=5000000.00)  # R5M maximum
    
    # Enterprise features
    white_label_enabled = db.Column(db.Boolean, default=False)
    custom_branding = db.Column(db.Text)  # JSON: branding configuration
    multi_tenant_support = db.Column(db.Boolean, default=False)
    api_rate_limit = db.Column(db.Integer, default=1000)  # Requests per minute
    
    # Real-time bank API features
    bank_verification_enabled = db.Column(db.Boolean, default=True)
    account_verification_enabled = db.Column(db.Boolean, default=True)
    real_time_settlement = db.Column(db.Boolean, default=True)
    instant_payment_notification = db.Column(db.Boolean, default=True)
    
    # Webhook configuration
    webhook_url = db.Column(db.String(500))
    webhook_secret = db.Column(db.String(200))
    webhook_events = db.Column(db.Text)  # JSON: ['payment.completed', 'payment.failed', 'refund.processed']
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(db.Numeric(15, 2), default=0.00)
    average_processing_time = db.Column(db.Float, default=0.0)  # Seconds
    
    # Status and timestamps
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_transaction_at = db.Column(db.DateTime)

class OzowIntegration(db.Model):
    """
    Ozow Integration Model
    
    Ozow is South Africa's instant EFT specialist with bank API
    technology and real-time payment processing.
    """
    __tablename__ = 'ozow_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    business_name = db.Column(db.String(200), nullable=False)
    
    # Ozow configuration
    site_code = db.Column(db.String(100), nullable=False)
    private_key = db.Column(db.String(500), nullable=False)
    api_key = db.Column(db.String(200), nullable=False)
    is_test_mode = db.Column(db.Boolean, default=True)
    
    # Payment configuration
    payment_methods = db.Column(db.Text)  # JSON: ['instant_eft', 'smart_eft', 'qr_code']
    supported_banks = db.Column(db.Text)  # JSON: ['absa', 'fnb', 'nedbank', 'standard_bank', 'capitec', 'investec']
    supported_currencies = db.Column(db.Text)  # JSON: ['ZAR']
    minimum_amount = db.Column(db.Numeric(10, 2), default=1.00)  # R1.00 minimum
    maximum_amount = db.Column(db.Numeric(12, 2), default=3000000.00)  # R3M maximum
    
    # Instant EFT features
    instant_settlement = db.Column(db.Boolean, default=True)
    real_time_verification = db.Column(db.Boolean, default=True)
    bank_api_integration = db.Column(db.Boolean, default=True)
    smart_routing = db.Column(db.Boolean, default=True)
    
    # QR code payment features
    qr_code_enabled = db.Column(db.Boolean, default=False)
    qr_code_expiry = db.Column(db.Integer, default=300)  # 5 minutes
    dynamic_qr_codes = db.Column(db.Boolean, default=True)
    
    # Notification configuration
    success_url = db.Column(db.String(500))
    cancel_url = db.Column(db.String(500))
    error_url = db.Column(db.String(500))
    notify_url = db.Column(db.String(500))
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(db.Numeric(15, 2), default=0.00)
    average_processing_time = db.Column(db.Float, default=0.0)  # Seconds
    
    # Status and timestamps
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_transaction_at = db.Column(db.DateTime)

class StandardBankAPIIntegration(db.Model):
    """
    Standard Bank API Integration Model
    
    Standard Bank API Marketplace provides comprehensive banking APIs
    including the award-winning "Best Open Banking API" platform.
    """
    __tablename__ = 'standard_bank_api_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    business_name = db.Column(db.String(200), nullable=False)
    
    # Standard Bank API configuration
    client_id = db.Column(db.String(100), nullable=False)
    client_secret = db.Column(db.String(200), nullable=False)
    api_key = db.Column(db.String(200), nullable=False)
    environment = db.Column(db.String(20), default='sandbox')  # sandbox, production
    
    # API services
    enabled_services = db.Column(db.Text)  # JSON: ['payments', 'accounts', 'cards', 'loans', 'forex', 'trade']
    api_version = db.Column(db.String(20), default='v1')
    rate_limit = db.Column(db.Integer, default=1000)  # Requests per minute
    
    # Payment services
    payment_types = db.Column(db.Text)  # JSON: ['immediate_payment', 'future_dated', 'recurring', 'bulk_payment']
    supported_currencies = db.Column(db.Text)  # JSON: ['ZAR', 'USD', 'EUR', 'GBP']
    minimum_amount = db.Column(db.Numeric(10, 2), default=0.01)  # 1 cent minimum
    maximum_amount = db.Column(db.Numeric(15, 2), default=10000000.00)  # R10M maximum
    
    # Account services
    account_types = db.Column(db.Text)  # JSON: ['current', 'savings', 'credit_card', 'loan']
    balance_inquiry_enabled = db.Column(db.Boolean, default=True)
    transaction_history_enabled = db.Column(db.Boolean, default=True)
    statement_generation_enabled = db.Column(db.Boolean, default=True)
    
    # Advanced features
    forex_services_enabled = db.Column(db.Boolean, default=False)
    trade_finance_enabled = db.Column(db.Boolean, default=False)
    card_services_enabled = db.Column(db.Boolean, default=False)
    loan_services_enabled = db.Column(db.Boolean, default=False)
    
    # Security configuration
    oauth2_enabled = db.Column(db.Boolean, default=True)
    jwt_token_expiry = db.Column(db.Integer, default=3600)  # 1 hour
    refresh_token_enabled = db.Column(db.Boolean, default=True)
    encryption_enabled = db.Column(db.Boolean, default=True)
    
    # Performance metrics
    total_api_calls = db.Column(db.BigInteger, default=0)
    successful_calls = db.Column(db.BigInteger, default=0)
    failed_calls = db.Column(db.BigInteger, default=0)
    average_response_time = db.Column(db.Float, default=0.0)  # Milliseconds
    
    # Status and timestamps
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_api_call_at = db.Column(db.DateTime)

class YocoIntegration(db.Model):
    """
    Yoco Integration Model
    
    Yoco provides SME payment solutions with card readers,
    online payments, and business management tools.
    """
    __tablename__ = 'yoco_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    business_name = db.Column(db.String(200), nullable=False)
    
    # Yoco configuration
    secret_key = db.Column(db.String(200), nullable=False)
    public_key = db.Column(db.String(200), nullable=False)
    webhook_secret = db.Column(db.String(200))
    environment = db.Column(db.String(20), default='test')  # test, live
    
    # Payment configuration
    payment_methods = db.Column(db.Text)  # JSON: ['card', 'online', 'qr_code', 'tap_to_pay']
    supported_cards = db.Column(db.Text)  # JSON: ['visa', 'mastercard', 'american_express']
    supported_currencies = db.Column(db.Text)  # JSON: ['ZAR']
    minimum_amount = db.Column(db.Numeric(10, 2), default=1.00)  # R1.00 minimum
    maximum_amount = db.Column(db.Numeric(12, 2), default=500000.00)  # R500K maximum
    
    # SME features
    card_reader_enabled = db.Column(db.Boolean, default=False)
    online_payments_enabled = db.Column(db.Boolean, default=True)
    qr_code_payments_enabled = db.Column(db.Boolean, default=False)
    tap_to_pay_enabled = db.Column(db.Boolean, default=False)
    
    # Business management features
    inventory_management = db.Column(db.Boolean, default=False)
    sales_reporting = db.Column(db.Boolean, default=True)
    customer_management = db.Column(db.Boolean, default=False)
    receipt_management = db.Column(db.Boolean, default=True)
    
    # Webhook configuration
    webhook_url = db.Column(db.String(500))
    webhook_events = db.Column(db.Text)  # JSON: ['payment.succeeded', 'payment.failed', 'refund.succeeded']
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(db.Numeric(15, 2), default=0.00)
    average_transaction_value = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Status and timestamps
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_transaction_at = db.Column(db.DateTime)

class SouthAfricanPaymentTransaction(db.Model):
    """
    South African Payment Transaction Model
    
    Comprehensive transaction tracking for all South African payment platforms
    with advanced analytics and reporting capabilities.
    """
    __tablename__ = 'south_african_payment_transactions'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    platform_transaction_id = db.Column(db.String(200), index=True)
    
    # Platform and user information
    platform = db.Column(db.String(50), nullable=False, index=True)  # payfast, stitch, ozow, standard_bank, yoco
    integration_id = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    
    # Transaction details
    transaction_type = db.Column(db.String(50), nullable=False)  # payment, refund, transfer, inquiry
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    description = db.Column(db.Text)
    reference = db.Column(db.String(200))
    
    # Payment method details
    payment_method = db.Column(db.String(50))  # card, eft, instant_eft, qr_code, api
    bank_name = db.Column(db.String(100))  # For EFT transactions
    card_type = db.Column(db.String(50))  # visa, mastercard, amex
    
    # Status and processing
    status = db.Column(db.String(20), nullable=False, index=True)  # pending, completed, failed, cancelled, refunded
    processing_time = db.Column(db.Float)  # Processing time in seconds
    failure_reason = db.Column(db.Text)
    
    # South African specific fields
    vat_amount = db.Column(db.Numeric(10, 2), default=0.00)
    vat_rate = db.Column(db.Float, default=15.0)  # 15% VAT in South Africa
    settlement_date = db.Column(db.Date)
    settlement_amount = db.Column(db.Numeric(15, 2))
    
    # Fees and charges
    platform_fee = db.Column(db.Numeric(10, 2), default=0.00)
    processing_fee = db.Column(db.Numeric(10, 2), default=0.00)
    total_fees = db.Column(db.Numeric(10, 2), default=0.00)
    net_amount = db.Column(db.Numeric(15, 2))
    
    # Metadata and context
    transaction_metadata = db.Column(db.Text)  # JSON: additional transaction data
    customer_info = db.Column(db.Text)  # JSON: customer information
    device_info = db.Column(db.Text)  # JSON: device and browser information
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    settled_at = db.Column(db.DateTime)

class SouthAfricanPaymentAnalytics(db.Model):
    """
    South African Payment Analytics Model
    
    Advanced analytics and reporting for South African payment ecosystem
    with business intelligence and performance metrics.
    """
    __tablename__ = 'south_african_payment_analytics'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    analytics_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Scope and period
    user_id = db.Column(db.String(100), nullable=False, index=True)
    platform = db.Column(db.String(50), index=True)  # Specific platform or 'all'
    period_type = db.Column(db.String(20), nullable=False)  # daily, weekly, monthly, yearly
    period_start = db.Column(db.DateTime, nullable=False, index=True)
    period_end = db.Column(db.DateTime, nullable=False, index=True)
    
    # Transaction metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    refunded_transactions = db.Column(db.BigInteger, default=0)
    success_rate = db.Column(db.Float, default=0.0)
    
    # Volume metrics
    total_volume = db.Column(db.Numeric(20, 2), default=0.00)
    successful_volume = db.Column(db.Numeric(20, 2), default=0.00)
    refunded_volume = db.Column(db.Numeric(20, 2), default=0.00)
    net_volume = db.Column(db.Numeric(20, 2), default=0.00)
    average_transaction_value = db.Column(db.Numeric(15, 2), default=0.00)
    
    # Performance metrics
    average_processing_time = db.Column(db.Float, default=0.0)  # Seconds
    fastest_transaction = db.Column(db.Float, default=0.0)
    slowest_transaction = db.Column(db.Float, default=0.0)
    uptime_percentage = db.Column(db.Float, default=100.0)
    
    # Payment method breakdown
    card_transactions = db.Column(db.BigInteger, default=0)
    eft_transactions = db.Column(db.BigInteger, default=0)
    instant_eft_transactions = db.Column(db.BigInteger, default=0)
    qr_code_transactions = db.Column(db.BigInteger, default=0)
    api_transactions = db.Column(db.BigInteger, default=0)
    
    # Financial metrics
    total_fees_collected = db.Column(db.Numeric(15, 2), default=0.00)
    total_vat_collected = db.Column(db.Numeric(15, 2), default=0.00)
    net_settlement_amount = db.Column(db.Numeric(20, 2), default=0.00)
    
    # South African market metrics
    rand_volume = db.Column(db.Numeric(20, 2), default=0.00)
    foreign_currency_volume = db.Column(db.Numeric(20, 2), default=0.00)
    cross_border_transactions = db.Column(db.BigInteger, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

