#!/bin/bash
echo "═══════════════════════════════════════════════════════"
echo "          📱 STARTING EXPO WEB SERVER"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Starting Expo web server..."
echo "This may take 15-20 seconds..."
echo ""
echo "Once started, open: http://localhost:8081"
echo ""
echo "If it doesn't work, use iOS Simulator instead:"
echo "  Press 'i' in the Expo terminal"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""

cd ~/code/iqra/frontend
npx expo start --web --port 8081
