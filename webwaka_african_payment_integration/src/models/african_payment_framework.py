"""
WebWaka Universal African Payment Integration Framework Models
===========================================================

This module contains the core database models for the most comprehensive
African payment gateway integration system ever built. It supports 115+
payment gateways across Nigeria, Kenya, South Africa, Ghana and beyond.

Features:
- Universal payment gateway management
- African-optimized payment processing
- Cross-border payment support
- Mobile money integration
- Banking API connectivity
- Real-time payment analytics
- Cultural intelligence integration
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime
import json

# Import shared database instance
from src.models.user import db

class AfricanPaymentGateway(db.Model):
    """
    Universal African Payment Gateway Model
    
    Manages all payment gateways across Africa with comprehensive
    metadata, configuration, and performance tracking.
    """
    __tablename__ = 'african_payment_gateways'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    gateway_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Geographic and market information
    country_code = db.Column(db.String(3), nullable=False, index=True)  # ISO 3166-1 alpha-3
    country_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False, index=True)  # West, East, Southern, North, Central
    coverage_countries = db.Column(db.Text)  # JSON array of supported countries
    market_share = db.Column(db.Float, default=0.0)  # Market share percentage
    user_base = db.Column(db.BigInteger, default=0)  # Number of users
    
    # Technical integration details
    api_type = db.Column(db.String(50), nullable=False)  # REST, SOAP, GraphQL, Webhook
    api_version = db.Column(db.String(20))
    api_documentation_url = db.Column(db.String(500))
    developer_portal_url = db.Column(db.String(500))
    sandbox_url = db.Column(db.String(500))
    production_url = db.Column(db.String(500))
    
    # Authentication and security
    auth_type = db.Column(db.String(50), nullable=False)  # API_KEY, OAUTH2, JWT, BASIC, CUSTOM
    auth_requirements = db.Column(db.Text)  # JSON object with auth details
    security_features = db.Column(db.Text)  # JSON array of security features
    compliance_standards = db.Column(db.Text)  # JSON array (PCI_DSS, ISO27001, etc.)
    
    # Payment method support
    supported_payment_methods = db.Column(db.Text, nullable=False)  # JSON array
    mobile_money_networks = db.Column(db.Text)  # JSON array of supported networks
    card_types = db.Column(db.Text)  # JSON array (VISA, MASTERCARD, AMEX, etc.)
    bank_transfer_types = db.Column(db.Text)  # JSON array (EFT, ACH, SEPA, etc.)
    alternative_methods = db.Column(db.Text)  # JSON array (QR, USSD, etc.)
    
    # Currency and pricing
    supported_currencies = db.Column(db.Text, nullable=False)  # JSON array of currency codes
    primary_currency = db.Column(db.String(3), nullable=False)  # Primary currency code
    transaction_fees = db.Column(db.Text)  # JSON object with fee structure
    settlement_period = db.Column(db.String(50))  # T+0, T+1, T+2, etc.
    minimum_amount = db.Column(Numeric(15, 2), default=0.00)
    maximum_amount = db.Column(Numeric(15, 2))
    
    # Performance and reliability
    uptime_percentage = db.Column(db.Float, default=99.0)
    average_response_time = db.Column(db.Integer, default=1000)  # milliseconds
    success_rate = db.Column(db.Float, default=99.0)  # percentage
    rate_limits = db.Column(db.Text)  # JSON object with rate limiting info
    
    # African optimization features
    mobile_optimization_score = db.Column(db.Float, default=0.0)  # 0-100
    network_optimization_score = db.Column(db.Float, default=0.0)  # 0-100
    offline_capability_score = db.Column(db.Float, default=0.0)  # 0-100
    cultural_intelligence_score = db.Column(db.Float, default=0.0)  # 0-100
    local_language_support = db.Column(db.Text)  # JSON array of supported languages
    traditional_payment_support = db.Column(db.Boolean, default=False)
    
    # Business and operational details
    company_name = db.Column(db.String(200), nullable=False)
    company_website = db.Column(db.String(500))
    headquarters_location = db.Column(db.String(200))
    founded_year = db.Column(db.Integer)
    business_model = db.Column(db.String(100))  # B2B, B2C, B2B2C
    target_market = db.Column(db.String(100))  # SME, Enterprise, Consumer, All
    
    # Integration complexity and support
    integration_complexity = db.Column(db.String(20), default='Medium')  # Low, Medium, High
    sdk_availability = db.Column(db.Text)  # JSON array of available SDKs
    webhook_support = db.Column(db.Boolean, default=False)
    callback_support = db.Column(db.Boolean, default=False)
    testing_environment = db.Column(db.String(50))  # Full, Limited, None
    developer_support_quality = db.Column(db.String(20), default='Good')  # Poor, Fair, Good, Excellent
    
    # Regulatory and licensing
    regulatory_licenses = db.Column(db.Text)  # JSON array of licenses
    regulatory_bodies = db.Column(db.Text)  # JSON array of regulatory bodies
    kyc_requirements = db.Column(db.Text)  # JSON object with KYC details
    aml_compliance = db.Column(db.Boolean, default=False)
    
    # Status and metadata
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, Deprecated, Beta
    tier = db.Column(db.Integer, default=2)  # 1=Critical, 2=Important, 3=Standard, 4=Niche
    priority_score = db.Column(db.Float, default=50.0)  # 0-100 integration priority
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    integrations = db.relationship('PaymentGatewayIntegration', backref='gateway', lazy=True)
    transactions = db.relationship('PaymentTransaction', backref='gateway', lazy=True)
    analytics = db.relationship('PaymentGatewayAnalytics', backref='gateway', lazy=True)
    
    def __repr__(self):
        return f'<AfricanPaymentGateway {self.name} ({self.country_code})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'gateway_id': self.gateway_id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'country_code': self.country_code,
            'country_name': self.country_name,
            'region': self.region,
            'coverage_countries': json.loads(self.coverage_countries) if self.coverage_countries else [],
            'market_share': self.market_share,
            'user_base': self.user_base,
            'api_type': self.api_type,
            'api_version': self.api_version,
            'api_documentation_url': self.api_documentation_url,
            'developer_portal_url': self.developer_portal_url,
            'auth_type': self.auth_type,
            'supported_payment_methods': json.loads(self.supported_payment_methods) if self.supported_payment_methods else [],
            'supported_currencies': json.loads(self.supported_currencies) if self.supported_currencies else [],
            'primary_currency': self.primary_currency,
            'mobile_optimization_score': self.mobile_optimization_score,
            'network_optimization_score': self.network_optimization_score,
            'offline_capability_score': self.offline_capability_score,
            'cultural_intelligence_score': self.cultural_intelligence_score,
            'uptime_percentage': self.uptime_percentage,
            'success_rate': self.success_rate,
            'status': self.status,
            'tier': self.tier,
            'priority_score': self.priority_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class PaymentGatewayIntegration(db.Model):
    """
    Payment Gateway Integration Configuration
    
    Manages the integration configuration and credentials for each
    payment gateway, supporting multiple environments and user contexts.
    """
    __tablename__ = 'payment_gateway_integrations'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    gateway_id = db.Column(db.String(100), db.ForeignKey('african_payment_gateways.gateway_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)  # WebWaka user ID
    
    # Integration configuration
    environment = db.Column(db.String(20), default='sandbox')  # sandbox, production
    integration_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Credentials and authentication (encrypted)
    api_credentials = db.Column(db.Text, nullable=False)  # Encrypted JSON object
    webhook_url = db.Column(db.String(500))
    callback_url = db.Column(db.String(500))
    
    # Configuration settings
    configuration = db.Column(db.Text)  # JSON object with gateway-specific config
    payment_methods_enabled = db.Column(db.Text)  # JSON array of enabled methods
    currencies_enabled = db.Column(db.Text)  # JSON array of enabled currencies
    
    # Limits and restrictions
    daily_limit = db.Column(Numeric(15, 2))
    monthly_limit = db.Column(Numeric(15, 2))
    per_transaction_limit = db.Column(Numeric(15, 2))
    
    # Status and monitoring
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, Suspended, Error
    health_status = db.Column(db.String(20), default='Unknown')  # Healthy, Warning, Critical, Unknown
    last_health_check = db.Column(db.DateTime)
    last_successful_transaction = db.Column(db.DateTime)
    
    # Performance metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    total_volume = db.Column(Numeric(15, 2), default=0.00)
    success_rate = db.Column(db.Float, default=0.0)
    average_response_time = db.Column(db.Integer, default=0)  # milliseconds
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    
    # Relationships
    transactions = db.relationship('PaymentTransaction', backref='integration', lazy=True)
    
    def __repr__(self):
        return f'<PaymentGatewayIntegration {self.integration_name} ({self.gateway_id})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses (excluding sensitive data)"""
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'gateway_id': self.gateway_id,
            'user_id': self.user_id,
            'environment': self.environment,
            'integration_name': self.integration_name,
            'description': self.description,
            'payment_methods_enabled': json.loads(self.payment_methods_enabled) if self.payment_methods_enabled else [],
            'currencies_enabled': json.loads(self.currencies_enabled) if self.currencies_enabled else [],
            'status': self.status,
            'health_status': self.health_status,
            'total_transactions': self.total_transactions,
            'total_volume': float(self.total_volume) if self.total_volume else 0.0,
            'success_rate': self.success_rate,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used': self.last_used.isoformat() if self.last_used else None
        }

class PaymentTransaction(db.Model):
    """
    Payment Transaction Model
    
    Records all payment transactions processed through the African
    payment gateway integration system with comprehensive tracking.
    """
    __tablename__ = 'payment_transactions'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    gateway_id = db.Column(db.String(100), db.ForeignKey('african_payment_gateways.gateway_id'), nullable=False)
    integration_id = db.Column(db.String(100), db.ForeignKey('payment_gateway_integrations.integration_id'), nullable=False)
    
    # Transaction details
    external_transaction_id = db.Column(db.String(200))  # Gateway's transaction ID
    reference = db.Column(db.String(200), nullable=False)  # Merchant reference
    description = db.Column(db.Text)
    
    # Payment information
    amount = db.Column(Numeric(15, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_channel = db.Column(db.String(50))  # mobile_money, card, bank_transfer, etc.
    
    # Customer information
    customer_id = db.Column(db.String(100))
    customer_email = db.Column(db.String(200))
    customer_phone = db.Column(db.String(20))
    customer_name = db.Column(db.String(200))
    
    # Transaction status and flow
    status = db.Column(db.String(20), default='Pending')  # Pending, Processing, Success, Failed, Cancelled
    gateway_status = db.Column(db.String(50))  # Gateway-specific status
    failure_reason = db.Column(db.Text)
    
    # Timing information
    initiated_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    response_time = db.Column(db.Integer)  # milliseconds
    
    # Gateway response data
    gateway_response = db.Column(db.Text)  # JSON object with full gateway response
    callback_data = db.Column(db.Text)  # JSON object with callback/webhook data
    
    # Fees and charges
    gateway_fee = db.Column(Numeric(10, 4), default=0.0000)
    platform_fee = db.Column(Numeric(10, 4), default=0.0000)
    total_fees = db.Column(Numeric(10, 4), default=0.0000)
    net_amount = db.Column(Numeric(15, 2))
    
    # African context
    country_code = db.Column(db.String(3), nullable=False)
    mobile_network = db.Column(db.String(50))  # For mobile money transactions
    bank_code = db.Column(db.String(20))  # For bank transfer transactions
    
    # Metadata
    transaction_metadata = db.Column(db.Text)  # JSON object for additional data
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Audit trail
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaymentTransaction {self.transaction_id} ({self.amount} {self.currency})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'gateway_id': self.gateway_id,
            'integration_id': self.integration_id,
            'external_transaction_id': self.external_transaction_id,
            'reference': self.reference,
            'description': self.description,
            'amount': float(self.amount) if self.amount else 0.0,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'payment_channel': self.payment_channel,
            'status': self.status,
            'gateway_status': self.gateway_status,
            'failure_reason': self.failure_reason,
            'customer_id': self.customer_id,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'customer_name': self.customer_name,
            'country_code': self.country_code,
            'mobile_network': self.mobile_network,
            'bank_code': self.bank_code,
            'gateway_fee': float(self.gateway_fee) if self.gateway_fee else 0.0,
            'platform_fee': float(self.platform_fee) if self.platform_fee else 0.0,
            'total_fees': float(self.total_fees) if self.total_fees else 0.0,
            'net_amount': float(self.net_amount) if self.net_amount else 0.0,
            'response_time': self.response_time,
            'initiated_at': self.initiated_at.isoformat() if self.initiated_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PaymentGatewayAnalytics(db.Model):
    """
    Payment Gateway Analytics Model
    
    Tracks performance analytics and metrics for each payment gateway
    to enable data-driven optimization and monitoring.
    """
    __tablename__ = 'payment_gateway_analytics'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    analytics_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    gateway_id = db.Column(db.String(100), db.ForeignKey('african_payment_gateways.gateway_id'), nullable=False)
    
    # Time period
    period_type = db.Column(db.String(20), nullable=False)  # hourly, daily, weekly, monthly
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)
    
    # Transaction metrics
    total_transactions = db.Column(db.BigInteger, default=0)
    successful_transactions = db.Column(db.BigInteger, default=0)
    failed_transactions = db.Column(db.BigInteger, default=0)
    pending_transactions = db.Column(db.BigInteger, default=0)
    
    # Volume metrics
    total_volume = db.Column(Numeric(15, 2), default=0.00)
    successful_volume = db.Column(Numeric(15, 2), default=0.00)
    average_transaction_value = db.Column(Numeric(15, 2), default=0.00)
    
    # Performance metrics
    success_rate = db.Column(db.Float, default=0.0)  # percentage
    average_response_time = db.Column(db.Integer, default=0)  # milliseconds
    uptime_percentage = db.Column(db.Float, default=0.0)
    error_rate = db.Column(db.Float, default=0.0)
    
    # Payment method breakdown
    mobile_money_transactions = db.Column(db.BigInteger, default=0)
    card_transactions = db.Column(db.BigInteger, default=0)
    bank_transfer_transactions = db.Column(db.BigInteger, default=0)
    other_transactions = db.Column(db.BigInteger, default=0)
    
    # Geographic breakdown
    country_breakdown = db.Column(db.Text)  # JSON object with country-wise metrics
    currency_breakdown = db.Column(db.Text)  # JSON object with currency-wise metrics
    
    # African optimization metrics
    mobile_optimization_performance = db.Column(db.Float, default=0.0)
    network_optimization_performance = db.Column(db.Float, default=0.0)
    offline_capability_usage = db.Column(db.Float, default=0.0)
    
    # Fee and revenue metrics
    total_fees_collected = db.Column(Numeric(15, 2), default=0.00)
    platform_revenue = db.Column(Numeric(15, 2), default=0.00)
    gateway_costs = db.Column(Numeric(15, 2), default=0.00)
    
    # Quality metrics
    customer_satisfaction_score = db.Column(db.Float, default=0.0)
    integration_health_score = db.Column(db.Float, default=0.0)
    reliability_score = db.Column(db.Float, default=0.0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaymentGatewayAnalytics {self.gateway_id} ({self.period_type})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'analytics_id': self.analytics_id,
            'gateway_id': self.gateway_id,
            'period_type': self.period_type,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'total_transactions': self.total_transactions,
            'successful_transactions': self.successful_transactions,
            'failed_transactions': self.failed_transactions,
            'total_volume': float(self.total_volume) if self.total_volume else 0.0,
            'successful_volume': float(self.successful_volume) if self.successful_volume else 0.0,
            'average_transaction_value': float(self.average_transaction_value) if self.average_transaction_value else 0.0,
            'success_rate': self.success_rate,
            'average_response_time': self.average_response_time,
            'uptime_percentage': self.uptime_percentage,
            'mobile_money_transactions': self.mobile_money_transactions,
            'card_transactions': self.card_transactions,
            'bank_transfer_transactions': self.bank_transfer_transactions,
            'country_breakdown': json.loads(self.country_breakdown) if self.country_breakdown else {},
            'currency_breakdown': json.loads(self.currency_breakdown) if self.currency_breakdown else {},
            'mobile_optimization_performance': self.mobile_optimization_performance,
            'network_optimization_performance': self.network_optimization_performance,
            'total_fees_collected': float(self.total_fees_collected) if self.total_fees_collected else 0.0,
            'platform_revenue': float(self.platform_revenue) if self.platform_revenue else 0.0,
            'customer_satisfaction_score': self.customer_satisfaction_score,
            'integration_health_score': self.integration_health_score,
            'reliability_score': self.reliability_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AfricanPaymentMethod(db.Model):
    """
    African Payment Method Model
    
    Catalogs all payment methods available across Africa with detailed
    information about their characteristics and integration requirements.
    """
    __tablename__ = 'african_payment_methods'
    
    # Primary identification
    id = db.Column(db.Integer, primary_key=True)
    method_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Classification
    category = db.Column(db.String(50), nullable=False)  # mobile_money, card, bank_transfer, crypto, etc.
    subcategory = db.Column(db.String(50))  # visa, mastercard, mtn_momo, m_pesa, etc.
    type = db.Column(db.String(50), nullable=False)  # credit, debit, prepaid, wallet, etc.
    
    # Geographic availability
    available_countries = db.Column(db.Text, nullable=False)  # JSON array of country codes
    primary_country = db.Column(db.String(3), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    
    # Technical details
    requires_authentication = db.Column(db.Boolean, default=True)
    supports_recurring = db.Column(db.Boolean, default=False)
    supports_refunds = db.Column(db.Boolean, default=False)
    supports_partial_refunds = db.Column(db.Boolean, default=False)
    real_time_processing = db.Column(db.Boolean, default=False)
    
    # Limits and constraints
    minimum_amount = db.Column(Numeric(15, 2), default=0.00)
    maximum_amount = db.Column(Numeric(15, 2))
    daily_limit = db.Column(Numeric(15, 2))
    monthly_limit = db.Column(Numeric(15, 2))
    
    # Currency support
    supported_currencies = db.Column(db.Text, nullable=False)  # JSON array
    primary_currency = db.Column(db.String(3), nullable=False)
    
    # African context
    mobile_network = db.Column(db.String(50))  # For mobile money methods
    bank_network = db.Column(db.String(50))  # For bank-based methods
    traditional_name = db.Column(db.String(200))  # Traditional/local name
    cultural_significance = db.Column(db.Text)  # Cultural context and usage
    
    # Usage statistics
    adoption_rate = db.Column(db.Float, default=0.0)  # percentage
    user_base = db.Column(db.BigInteger, default=0)
    transaction_volume = db.Column(db.BigInteger, default=0)
    
    # Integration information
    integration_complexity = db.Column(db.String(20), default='Medium')
    api_support_quality = db.Column(db.String(20), default='Good')
    documentation_quality = db.Column(db.String(20), default='Good')
    
    # Status and metadata
    status = db.Column(db.String(20), default='Active')
    popularity_score = db.Column(db.Float, default=50.0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AfricanPaymentMethod {self.name} ({self.primary_country})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'method_id': self.method_id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory,
            'type': self.type,
            'available_countries': json.loads(self.available_countries) if self.available_countries else [],
            'primary_country': self.primary_country,
            'region': self.region,
            'requires_authentication': self.requires_authentication,
            'supports_recurring': self.supports_recurring,
            'supports_refunds': self.supports_refunds,
            'real_time_processing': self.real_time_processing,
            'minimum_amount': float(self.minimum_amount) if self.minimum_amount else 0.0,
            'maximum_amount': float(self.maximum_amount) if self.maximum_amount else None,
            'supported_currencies': json.loads(self.supported_currencies) if self.supported_currencies else [],
            'primary_currency': self.primary_currency,
            'mobile_network': self.mobile_network,
            'bank_network': self.bank_network,
            'traditional_name': self.traditional_name,
            'adoption_rate': self.adoption_rate,
            'user_base': self.user_base,
            'integration_complexity': self.integration_complexity,
            'status': self.status,
            'popularity_score': self.popularity_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

