# How to View the Frontend in Browser

## Current Status

✅ **Backend is running:** http://localhost:8000
- You're seeing: `{"message": "Iqra API is running", "version": "1.0.0"}`
- API Docs: http://localhost:8000/docs

## View Frontend in Browser

### Option 1: Web Version (Recommended for Browser)

The frontend is a React Native app, but Expo supports web. Run:

```bash
cd ~/code/iqra/frontend
npm run web
```

This will:
- Start the web server (usually on port 8081 or 19006)
- Automatically open your browser
- Show the app in the browser

**If web dependencies are missing:**
```bash
cd ~/code/iqra/frontend
npx expo install react-native-web react-dom @expo/metro-runtime
npm run web
```

### Option 2: Mobile App (Recommended for Full Experience)

Since this is a mobile app, the best experience is on a phone:

1. **Make sure Expo is running:**
   ```bash
   cd ~/code/iqra/frontend
   npm start
   ```

2. **You'll see a QR code in the terminal**

3. **On your phone:**
   - **iOS:** Open Camera app → Scan QR code
   - **Android:** Install "Expo Go" app → Scan QR code

4. **The app will open on your phone!**

### Option 3: iOS Simulator (Mac only)

If you have Xcode installed:

```bash
cd ~/code/iqra/frontend
npm run ios
```

This will open the iOS Simulator.

### Option 4: Android Emulator

If you have Android Studio installed:

```bash
cd ~/code/iqra/frontend
npm run android
```

## Quick Access URLs

Once running, you can access:

- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Backend Health:** http://localhost:8000/health
- **Frontend Web (if running):** http://localhost:8081 or http://localhost:19006

## Troubleshooting

**Web version not working?**
- Make sure you ran: `npx expo install react-native-web react-dom @expo/metro-runtime`
- Check if port is already in use
- Try: `npx expo start --web --port 19006`

**Can't see QR code?**
- Make sure `npm start` is running
- Check that your phone and computer are on the same WiFi network
- For physical device, update `frontend/.env` with your Mac's IP:
  ```
  API_BASE_URL=http://YOUR_MAC_IP:8000
  ```

**Port conflicts?**
- Backend: Change port in `uvicorn app.main:app --reload --port 8001`
- Frontend: Use `npx expo start --port 19007`

## Recommended Setup

**Terminal 1 - Backend:**
```bash
cd ~/code/iqra/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd ~/code/iqra/frontend
npm start
```

Then scan the QR code with Expo Go app on your phone for the best experience!

