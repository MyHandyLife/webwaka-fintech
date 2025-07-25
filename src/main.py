import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.african_payment_framework import african_payment_bp
from src.routes.tier1_critical_platforms import tier1_platforms_bp
from src.routes.nigerian_payment_ecosystem import nigerian_ecosystem_bp
from src.routes.kenyan_payment_ecosystem import kenyan_ecosystem_bp
from src.routes.south_african_payment_ecosystem import south_african_ecosystem_bp
from src.routes.ghanaian_payment_ecosystem import ghanaian_ecosystem_bp
from src.routes.continental_payment_networks import continental_networks_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(african_payment_bp)
app.register_blueprint(tier1_platforms_bp)
app.register_blueprint(nigerian_ecosystem_bp)
app.register_blueprint(kenyan_ecosystem_bp)
app.register_blueprint(south_african_ecosystem_bp)
app.register_blueprint(ghanaian_ecosystem_bp)
app.register_blueprint(continental_networks_bp)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    # Import models to ensure tables are created
    from src.models import african_payment_framework, tier1_critical_platforms, nigerian_payment_ecosystem, kenyan_payment_ecosystem, south_african_payment_ecosystem

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path == 'api' or path.startswith('api/'):
        # Return API information for API routes
        return {
            'service': 'WebWaka Universal African Payment Integration Framework',
            'version': '1.0.0',
            'description': 'The most comprehensive African payment gateway integration system ever built',
            'features': [
                'Universal African Payment Gateway Management',
                '115+ Payment Gateway Support (Nigeria, Kenya, South Africa, Ghana)',
                'Tier 1 Critical Platform Integration (M-Pesa, MTN MoMo, Paystack, Flutterwave, Hubtel)',
                'Nigerian Payment Ecosystem Integration (35+ Platforms)',
                'Kenyan Payment Ecosystem Integration (25+ Platforms)',
                'South African Payment Ecosystem Integration (30+ Platforms)',
                'Digital Bank Integration (Kuda, Opay, KCB, Equity)',
                'Traditional Bank APIs (GTBank, Access, UBA, Zenith)',
                'Mobile Money Integration (M-Pesa, MTN MoMo, Airtel Money)',
                'Fintech Platform Integration (Interswitch, SystemSpecs, Remita, Jenga API, Kopo Kopo)',
                'Cross-Border Payment Processing',
                'Banking API Connectivity',
                'Real-Time Transaction Processing',
                'African Network Optimization',
                'Cultural Intelligence Integration',
                'Multi-Currency Support',
                'Comprehensive Analytics'
            ],
            'tier1_platforms': [
                'M-Pesa (Kenya Mobile Money Leader - 50M+ users)',
                'MTN Mobile Money (17+ Countries, 900+ Partners)',
                'Paystack (Nigeria Payment Gateway Leader - 200K+ businesses)',
                'Flutterwave (34+ Countries, 1M+ businesses)',
                'Hubtel (Ghana Payment Aggregator Leader)'
            ],
            'nigerian_platforms': [
                'Kuda Bank (Nigeria\'s Leading Digital Bank)',
                'Opay (Super App with 30M+ Users)',
                'GTBank (Traditional Banking Leader)',
                'Interswitch (Payment Infrastructure Leader)',
                'Remita (E-billing and Payment Platform)',
                'Access Bank (Digital Banking Services)',
                'UBA (United Bank for Africa)',
                'Zenith Bank (Corporate Banking Leader)',
                'First Bank (Nigeria\'s Oldest Bank)',
                'Sterling Bank (Digital Innovation Leader)'
            ],
            'kenyan_platforms': [
                'KCB Bank (Kenya\'s Largest Bank)',
                'Equity Bank (Largest by Customer Base)',
                'Airtel Money Kenya (Second-Largest Mobile Money)',
                'Jenga API (Equity Bank\'s API Platform)',
                'Kopo Kopo (Leading Fintech Platform)',
                'Co-operative Bank (Co-op Bank)',
                'Standard Chartered Kenya',
                'Absa Bank Kenya',
                'NCBA Bank Kenya'
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
            ],
            'endpoints': {
                'health': '/api/african-payments/health',
                'tier1_health': '/api/tier1-platforms/health',
                'nigerian_health': '/api/nigerian-payments/health',
                'kenyan_health': '/api/kenyan-payments/health',
                'south_african_health': '/api/south-african-payments/health',
                'gateways': '/api/african-payments/gateways',
                'integrations': '/api/african-payments/integrations',
                'transactions': '/api/african-payments/transactions',
                'tier1_transactions': '/api/tier1-platforms/transactions',
                'nigerian_transactions': '/api/nigerian-payments/transactions',
                'kenyan_transactions': '/api/kenyan-payments/transactions',
                'south_african_transactions': '/api/south-african-payments/transactions',
                'analytics': '/api/african-payments/analytics/overview',
                'tier1_analytics': '/api/tier1-platforms/analytics/overview',
                'nigerian_analytics': '/api/nigerian-payments/analytics/overview',
                'kenyan_analytics': '/api/kenyan-payments/analytics/overview',
                'south_african_analytics': '/api/south-african-payments/analytics/overview',
                'mpesa': '/api/tier1-platforms/mpesa/integrations',
                'mtn_momo': '/api/tier1-platforms/mtn-momo/integrations',
                'paystack': '/api/tier1-platforms/paystack/integrations',
                'flutterwave': '/api/tier1-platforms/flutterwave/integrations',
                'hubtel': '/api/tier1-platforms/hubtel/integrations',
                'kuda': '/api/nigerian-payments/kuda/integrations',
                'opay': '/api/nigerian-payments/opay/integrations',
                'gtbank': '/api/nigerian-payments/gtbank/integrations',
                'interswitch': '/api/nigerian-payments/interswitch/integrations',
                'remita': '/api/nigerian-payments/remita/integrations',
                'kcb': '/api/kenyan-payments/kcb/integrations',
                'equity': '/api/kenyan-payments/equity/integrations',
                'airtel_money_kenya': '/api/kenyan-payments/airtel-money/integrations',
                'jenga': '/api/kenyan-payments/jenga/integrations',
                'kopokopo': '/api/kenyan-payments/kopokopo/integrations',
                'payfast': '/api/south-african-payments/payfast/integrations',
                'stitch': '/api/south-african-payments/stitch/integrations',
                'ozow': '/api/south-african-payments/ozow/integrations',
                'standard_bank_api': '/api/south-african-payments/standard-bank/integrations',
                'yoco': '/api/south-african-payments/yoco/integrations',
                'supported_platforms': '/api/tier1-platforms/platforms/supported',
                'nigerian_platforms': '/api/nigerian-payments/platforms/supported',
                'kenyan_platforms': '/api/kenyan-payments/platforms/supported',
                'south_african_platforms': '/api/south-african-payments/platforms/supported'
            },
            'supported_regions': ['West Africa', 'East Africa', 'Southern Africa', 'North Africa'],
            'supported_countries': ['Nigeria', 'Kenya', 'South Africa', 'Ghana', 'Uganda', 'Tanzania', 'Egypt', 'Morocco'],
            'payment_methods': ['Mobile Money', 'Bank Transfer', 'Card Payment', 'Digital Wallet', 'USSD', 'QR Code'],
            'documentation': 'https://docs.webwaka.com/african-payments'
        }
    
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

