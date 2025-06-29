#!/bin/bash
# CyberRotate Pro Enterprise Quick Start Script

echo "================================================================"
echo "  CyberRotate Pro Enterprise - Quick Start Script"
echo "  Created by Yashab Alam - Founder of ZehraSec"
echo "================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "ip_rotator.py" ]]; then
    print_error "Please run this script from the CyberRotate Pro directory"
    exit 1
fi

# Activate virtual environment if it exists
if [[ -d "venv" ]]; then
    print_status "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Choose your deployment mode:"
echo "1. Development Mode (Local testing)"
echo "2. Production Mode (Full deployment)"
echo "3. Enterprise Demo (All features enabled)"
echo "4. API Server Only"
echo "5. Analytics Dashboard Only"
echo ""
read -p "Enter your choice (1-5): " mode

case $mode in
    1)
        print_status "Starting Development Mode..."
        echo "Features enabled: Core rotation, GUI, basic monitoring"
        python3 ip_rotator.py --interactive
        ;;
    2)
        print_status "Starting Production Deployment..."
        chmod +x deploy_production.sh
        ./deploy_production.sh --full
        ;;
    3)
        print_status "Starting Enterprise Demo..."
        echo "This will start all enterprise features for demonstration."
        echo "Starting API server on port 8080..."
        python3 ip_rotator.py --api-server &
        API_PID=$!
        
        sleep 3
        echo "Starting analytics dashboard on port 8050..."
        python3 ip_rotator.py --dashboard &
        DASH_PID=$!
        
        sleep 3
        echo "Starting web dashboard on port 5000..."
        python3 ip_rotator.py --web-dashboard &
        WEB_PID=$!
        
        echo ""
        print_success "Enterprise demo started successfully!"
        echo "Access points:"
        echo "  - API Server: http://localhost:8080"
        echo "  - Analytics Dashboard: http://localhost:8050" 
        echo "  - Web Dashboard: http://localhost:5000"
        echo "  - API Documentation: http://localhost:8080/docs"
        echo ""
        echo "Press Ctrl+C to stop all services"
        
        # Wait for interrupt
        trap "echo 'Stopping services...'; kill $API_PID $DASH_PID $WEB_PID 2>/dev/null; exit 0" INT
        wait
        ;;
    4)
        print_status "Starting API Server Only..."
        python3 ip_rotator.py --api-server
        ;;
    5)
        print_status "Starting Analytics Dashboard Only..."
        python3 ip_rotator.py --dashboard
        ;;
    *)
        print_error "Invalid choice. Starting interactive mode..."
        python3 ip_rotator.py --interactive
        ;;
esac
