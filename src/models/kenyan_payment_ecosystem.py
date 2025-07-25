"""
WebWaka Kenyan Payment Ecosystem Integration Models
=================================================

This module provides comprehensive database models for integrating with Kenya's
extensive payment ecosystem, including mobile money platforms, banks, and fintech services.

Kenya is the birthplace of mobile money and home to M-Pesa, making it a critical
market for WebWaka's African payment integration strategy.

Features:
- Complete coverage of Kenyan payment platforms
- M-Pesa and mobile money optimization
- Banking API integration models
- Kenyan-specific features (MPESA, KCB, Equity Bank)
- Shilling (KES) optimization and local payment methods
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import json

# Import database instance
from src.models.user import db

# ============================================================================
# KENYAN PAYMENT PLATFORM INTEGRATION MODELS
# ============================================================================

class KCBBankIntegration(db.Model):
    """
    Kenya Commercial Bank (KCB) Integration Model
    
    KCB is one of Kenya's largest banks with comprehensive API services
    including KCB BUNI platform for digital banking and payments.
    """
    __tablename__ = 'kcb_bank_integrations'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # KCB API credentials
    client_id = Column(String(100), nullable=False)
    client_secret = Column(Text, nullable=False)  # Should be encrypted in production
    api_key = Column(String(100))
    subscription_key = Column(String(100))
    
    # Environment and configuration
    environment = Column(String(20), default='sandbox')  # sandbox, production
    base_url = Column(String(200))
    
    # Business information
    business_name = Column(String(100))
    business_account_number = Column(String(50))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    business_address = Column(Text)
    
    # KCB-specific features
    kcb_buni_enabled = Column(Boolean, default=True)
    account_services_enabled = Column(Boolean, default=True)
    transfer_services_enabled = Column(Boolean, default=True)
    bill_payment_enabled = Column(Boolean, default=True)
    statement_services_enabled = Column(Boolean, default=True)
    forex_services_enabled = Column(Boolean, default=False)
    loan_services_enabled = Column(Boolean, default=False)
    
    # Integration status and metrics
    status = Column(String(20), default='active')  # active, inactive, suspended
    last_sync = Column(DateTime)
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    failed_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'environment': self.environment,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'business_phone': self.business_phone,
            'kcb_buni_enabled': self.kcb_buni_enabled,
            'account_services_enabled': self.account_services_enabled,
            'transfer_services_enabled': self.transfer_services_enabled,
            'bill_payment_enabled': self.bill_payment_enabled,
            'statement_services_enabled': self.statement_services_enabled,
            'forex_services_enabled': self.forex_services_enabled,
            'loan_services_enabled': self.loan_services_enabled,
            'status': self.status,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'failed_transactions': self.failed_transactions,
            'success_rate': (self.successful_transactions / self.total_transactions * 100) if self.total_transactions > 0 else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class EquityBankIntegration(db.Model):
    """
    Equity Bank Integration Model
    
    Equity Bank is Kenya's largest bank by customer base with comprehensive
    digital banking services and API platform.
    """
    __tablename__ = 'equity_bank_integrations'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Equity Bank API credentials
    client_id = Column(String(100), nullable=False)
    client_secret = Column(Text, nullable=False)  # Should be encrypted in production
    api_key = Column(String(100))
    merchant_code = Column(String(50))
    
    # Environment and configuration
    environment = Column(String(20), default='sandbox')  # sandbox, production
    base_url = Column(String(200))
    
    # Business information
    business_name = Column(String(100))
    business_account_number = Column(String(50))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    business_branch = Column(String(100))
    
    # Equity Bank-specific features
    eazzy_banking_enabled = Column(Boolean, default=True)
    account_inquiry_enabled = Column(Boolean, default=True)
    fund_transfer_enabled = Column(Boolean, default=True)
    bill_payment_enabled = Column(Boolean, default=True)
    statement_request_enabled = Column(Boolean, default=True)
    mobile_banking_enabled = Column(Boolean, default=True)
    agent_banking_enabled = Column(Boolean, default=False)
    
    # Integration status and metrics
    status = Column(String(20), default='active')  # active, inactive, suspended
    last_sync = Column(DateTime)
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    failed_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'environment': self.environment,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'business_phone': self.business_phone,
            'business_branch': self.business_branch,
            'eazzy_banking_enabled': self.eazzy_banking_enabled,
            'account_inquiry_enabled': self.account_inquiry_enabled,
            'fund_transfer_enabled': self.fund_transfer_enabled,
            'bill_payment_enabled': self.bill_payment_enabled,
            'statement_request_enabled': self.statement_request_enabled,
            'mobile_banking_enabled': self.mobile_banking_enabled,
            'agent_banking_enabled': self.agent_banking_enabled,
            'status': self.status,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'failed_transactions': self.failed_transactions,
            'success_rate': (self.successful_transactions / self.total_transactions * 100) if self.total_transactions > 0 else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AirtelMoneyKenyaIntegration(db.Model):
    """
    Airtel Money Kenya Integration Model
    
    Airtel Money is Kenya's second-largest mobile money platform
    with comprehensive API services for payments and transfers.
    """
    __tablename__ = 'airtel_money_kenya_integrations'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Airtel Money API credentials
    client_id = Column(String(100), nullable=False)
    client_secret = Column(Text, nullable=False)  # Should be encrypted in production
    api_key = Column(String(100))
    merchant_id = Column(String(50))
    
    # Environment and configuration
    environment = Column(String(20), default='sandbox')  # sandbox, production
    base_url = Column(String(200))
    country_code = Column(String(5), default='KE')
    
    # Business information
    business_name = Column(String(100))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    business_category = Column(String(50))
    
    # Airtel Money-specific features
    collection_enabled = Column(Boolean, default=True)
    disbursement_enabled = Column(Boolean, default=True)
    balance_inquiry_enabled = Column(Boolean, default=True)
    transaction_status_enabled = Column(Boolean, default=True)
    refund_enabled = Column(Boolean, default=True)
    bulk_payment_enabled = Column(Boolean, default=False)
    
    # Webhook configuration
    callback_url = Column(String(200))
    webhook_url = Column(String(200))
    notification_url = Column(String(200))
    
    # Integration status and metrics
    status = Column(String(20), default='active')  # active, inactive, suspended
    last_sync = Column(DateTime)
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    failed_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'environment': self.environment,
            'country_code': self.country_code,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'business_phone': self.business_phone,
            'business_category': self.business_category,
            'collection_enabled': self.collection_enabled,
            'disbursement_enabled': self.disbursement_enabled,
            'balance_inquiry_enabled': self.balance_inquiry_enabled,
            'transaction_status_enabled': self.transaction_status_enabled,
            'refund_enabled': self.refund_enabled,
            'bulk_payment_enabled': self.bulk_payment_enabled,
            'callback_url': self.callback_url,
            'webhook_url': self.webhook_url,
            'status': self.status,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'failed_transactions': self.failed_transactions,
            'success_rate': (self.successful_transactions / self.total_transactions * 100) if self.total_transactions > 0 else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class JengaAPIIntegration(db.Model):
    """
    Jenga API Integration Model
    
    Jenga API is Equity Bank's comprehensive API platform providing
    banking services, payments, and financial data access.
    """
    __tablename__ = 'jenga_api_integrations'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Jenga API credentials
    api_key = Column(String(100), nullable=False)
    merchant_code = Column(String(50), nullable=False)
    consumer_secret = Column(Text, nullable=False)  # Should be encrypted in production
    
    # Environment and configuration
    environment = Column(String(20), default='sandbox')  # sandbox, production
    base_url = Column(String(200))
    
    # Business information
    business_name = Column(String(100))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    business_account_number = Column(String(50))
    
    # Jenga API-specific features
    account_services_enabled = Column(Boolean, default=True)
    send_money_enabled = Column(Boolean, default=True)
    receive_money_enabled = Column(Boolean, default=True)
    bill_payment_enabled = Column(Boolean, default=True)
    airtime_enabled = Column(Boolean, default=True)
    forex_rates_enabled = Column(Boolean, default=True)
    id_verification_enabled = Column(Boolean, default=False)
    
    # Integration status and metrics
    status = Column(String(20), default='active')  # active, inactive, suspended
    last_sync = Column(DateTime)
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    failed_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'environment': self.environment,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'business_phone': self.business_phone,
            'business_account_number': self.business_account_number,
            'account_services_enabled': self.account_services_enabled,
            'send_money_enabled': self.send_money_enabled,
            'receive_money_enabled': self.receive_money_enabled,
            'bill_payment_enabled': self.bill_payment_enabled,
            'airtime_enabled': self.airtime_enabled,
            'forex_rates_enabled': self.forex_rates_enabled,
            'id_verification_enabled': self.id_verification_enabled,
            'status': self.status,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'failed_transactions': self.failed_transactions,
            'success_rate': (self.successful_transactions / self.total_transactions * 100) if self.total_transactions > 0 else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class KopokopoPesaIntegration(db.Model):
    """
    Kopo Kopo Pesa Integration Model
    
    Kopo Kopo is a leading Kenyan fintech platform providing
    payment processing and business management solutions.
    """
    __tablename__ = 'kopokopo_pesa_integrations'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    integration_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Kopo Kopo API credentials
    client_id = Column(String(100), nullable=False)
    client_secret = Column(Text, nullable=False)  # Should be encrypted in production
    api_key = Column(String(100))
    
    # Environment and configuration
    environment = Column(String(20), default='sandbox')  # sandbox, production
    base_url = Column(String(200))
    
    # Business information
    business_name = Column(String(100))
    business_email = Column(String(100))
    business_phone = Column(String(20))
    business_category = Column(String(50))
    
    # Kopo Kopo-specific features
    stk_push_enabled = Column(Boolean, default=True)
    pay_enabled = Column(Boolean, default=True)
    transfer_enabled = Column(Boolean, default=True)
    webhook_enabled = Column(Boolean, default=True)
    settlement_enabled = Column(Boolean, default=True)
    
    # Webhook configuration
    webhook_url = Column(String(200))
    webhook_secret = Column(String(100))
    
    # Integration status and metrics
    status = Column(String(20), default='active')  # active, inactive, suspended
    last_sync = Column(DateTime)
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    failed_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'user_id': self.user_id,
            'environment': self.environment,
            'business_name': self.business_name,
            'business_email': self.business_email,
            'business_phone': self.business_phone,
            'business_category': self.business_category,
            'stk_push_enabled': self.stk_push_enabled,
            'pay_enabled': self.pay_enabled,
            'transfer_enabled': self.transfer_enabled,
            'webhook_enabled': self.webhook_enabled,
            'settlement_enabled': self.settlement_enabled,
            'webhook_url': self.webhook_url,
            'status': self.status,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'failed_transactions': self.failed_transactions,
            'success_rate': (self.successful_transactions / self.total_transactions * 100) if self.total_transactions > 0 else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ============================================================================
# KENYAN PAYMENT TRANSACTION MODEL
# ============================================================================

class KenyanPaymentTransaction(db.Model):
    """
    Comprehensive transaction model for all Kenyan payment platforms
    
    This model tracks transactions across all integrated Kenyan payment
    platforms including M-Pesa, banks, and fintech services.
    """
    __tablename__ = 'kenyan_payment_transactions'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Platform identification
    platform = Column(String(50), nullable=False, index=True)  # mpesa, kcb_bank, equity_bank, airtel_money, jenga_api, kopokopo
    platform_integration_id = Column(String(100), nullable=False, index=True)
    external_transaction_id = Column(String(100), index=True)
    
    # Transaction details
    reference = Column(String(100), index=True)
    description = Column(Text)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(5), default='KES')
    
    # Payment method and channel
    payment_method = Column(String(50), nullable=False)  # mpesa, bank_transfer, card, airtel_money
    payment_channel = Column(String(50))  # stk_push, paybill, till, ussd, api
    
    # Customer information
    customer_id = Column(String(100))
    customer_email = Column(String(100))
    customer_phone = Column(String(20))
    customer_name = Column(String(100))
    customer_id_number = Column(String(20))  # Kenyan ID number
    
    # Kenyan-specific fields
    mpesa_receipt_number = Column(String(50))
    mpesa_phone_number = Column(String(20))
    paybill_number = Column(String(20))
    till_number = Column(String(20))
    account_reference = Column(String(100))
    
    # Bank-specific fields
    bank_code = Column(String(10))
    account_number = Column(String(50))
    account_name = Column(String(100))
    branch_code = Column(String(10))
    
    # Transaction status and processing
    status = Column(String(20), default='Pending', index=True)  # Pending, Success, Failed, Cancelled, Reversed
    status_description = Column(Text)
    processing_code = Column(String(20))
    response_code = Column(String(20))
    response_description = Column(Text)
    
    # Financial details
    fees = Column(Numeric(10, 2), default=0)
    net_amount = Column(Numeric(15, 2))
    exchange_rate = Column(Numeric(10, 4))
    
    # Timing information
    initiated_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    expires_at = Column(DateTime)
    
    # Platform-specific data
    platform_request_data = Column(Text)  # JSON string
    platform_response_data = Column(Text)  # JSON string
    platform_callback_data = Column(Text)  # JSON string
    
    # Additional information
    narration = Column(Text)
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
            'customer_id': self.customer_id,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'customer_name': self.customer_name,
            'customer_id_number': self.customer_id_number,
            'mpesa_receipt_number': self.mpesa_receipt_number,
            'mpesa_phone_number': self.mpesa_phone_number,
            'paybill_number': self.paybill_number,
            'till_number': self.till_number,
            'account_reference': self.account_reference,
            'bank_code': self.bank_code,
            'account_number': self.account_number,
            'account_name': self.account_name,
            'branch_code': self.branch_code,
            'status': self.status,
            'status_description': self.status_description,
            'processing_code': self.processing_code,
            'response_code': self.response_code,
            'response_description': self.response_description,
            'fees': float(self.fees) if self.fees else None,
            'net_amount': float(self.net_amount) if self.net_amount else None,
            'exchange_rate': float(self.exchange_rate) if self.exchange_rate else None,
            'initiated_at': self.initiated_at.isoformat() if self.initiated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'narration': self.narration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ============================================================================
# KENYAN PAYMENT ANALYTICS MODEL
# ============================================================================

class KenyanPaymentAnalytics(db.Model):
    """
    Analytics model for Kenyan payment ecosystem performance tracking
    
    This model provides comprehensive analytics and reporting capabilities
    for all Kenyan payment platform integrations.
    """
    __tablename__ = 'kenyan_payment_analytics'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    analytics_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Time period
    period_start = Column(DateTime, nullable=False, index=True)
    period_end = Column(DateTime, nullable=False, index=True)
    period_type = Column(String(20), nullable=False)  # hourly, daily, weekly, monthly
    
    # Platform identification
    platform = Column(String(50), index=True)  # specific platform or 'all'
    integration_id = Column(String(100), index=True)
    
    # Transaction metrics
    total_transactions = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    failed_transactions = Column(Integer, default=0)
    pending_transactions = Column(Integer, default=0)
    cancelled_transactions = Column(Integer, default=0)
    
    # Financial metrics
    total_volume = Column(Numeric(20, 2), default=0)
    successful_volume = Column(Numeric(20, 2), default=0)
    average_transaction_value = Column(Numeric(15, 2), default=0)
    total_fees = Column(Numeric(15, 2), default=0)
    
    # Performance metrics
    success_rate = Column(Numeric(5, 2), default=0)  # Percentage
    average_processing_time = Column(Numeric(10, 2), default=0)  # Seconds
    uptime_percentage = Column(Numeric(5, 2), default=0)
    
    # Kenyan-specific metrics
    mpesa_transactions = Column(Integer, default=0)
    airtel_money_transactions = Column(Integer, default=0)
    bank_transfer_transactions = Column(Integer, default=0)
    card_transactions = Column(Integer, default=0)
    
    # Payment channel breakdown
    stk_push_transactions = Column(Integer, default=0)
    paybill_transactions = Column(Integer, default=0)
    till_transactions = Column(Integer, default=0)
    ussd_transactions = Column(Integer, default=0)
    api_transactions = Column(Integer, default=0)
    
    # Geographic and demographic data
    nairobi_transactions = Column(Integer, default=0)
    mombasa_transactions = Column(Integer, default=0)
    kisumu_transactions = Column(Integer, default=0)
    nakuru_transactions = Column(Integer, default=0)
    other_cities_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'analytics_id': self.analytics_id,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'period_type': self.period_type,
            'platform': self.platform,
            'integration_id': self.integration_id,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'failed_transactions': self.failed_transactions,
            'pending_transactions': self.pending_transactions,
            'cancelled_transactions': self.cancelled_transactions,
            'total_volume': float(self.total_volume) if self.total_volume else None,
            'successful_volume': float(self.successful_volume) if self.successful_volume else None,
            'average_transaction_value': float(self.average_transaction_value) if self.average_transaction_value else None,
            'total_fees': float(self.total_fees) if self.total_fees else None,
            'success_rate': float(self.success_rate) if self.success_rate else None,
            'average_processing_time': float(self.average_processing_time) if self.average_processing_time else None,
            'uptime_percentage': float(self.uptime_percentage) if self.uptime_percentage else None,
            'mpesa_transactions': self.mpesa_transactions,
            'airtel_money_transactions': self.airtel_money_transactions,
            'bank_transfer_transactions': self.bank_transfer_transactions,
            'card_transactions': self.card_transactions,
            'stk_push_transactions': self.stk_push_transactions,
            'paybill_transactions': self.paybill_transactions,
            'till_transactions': self.till_transactions,
            'ussd_transactions': self.ussd_transactions,
            'api_transactions': self.api_transactions,
            'nairobi_transactions': self.nairobi_transactions,
            'mombasa_transactions': self.mombasa_transactions,
            'kisumu_transactions': self.kisumu_transactions,
            'nakuru_transactions': self.nakuru_transactions,
            'other_cities_transactions': self.other_cities_transactions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

