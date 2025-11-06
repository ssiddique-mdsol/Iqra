# How to View the Mobile App (React Native/Expo)

## Current Setup

You have **two frontends**:
1. **Web version** (`frontend/web/index.html`) - Simple HTML/JS, works in any browser
2. **Mobile app** (`frontend/App.js`) - React Native/Expo, designed for mobile

## View Mobile App on Desktop

### Option 1: Expo Web (Easiest - Browser)

```bash
cd ~/code/iqra/frontend
npm install
npx expo start --web
```

Then open: **http://localhost:8081** in your browser

**Note:** React Native web support may have limitations. Some features work better on actual mobile.

### Option 2: iOS Simulator (Mac only - Best Experience)

**Requirements:**
- Xcode installed (`xcode-select --install`)
- iOS Simulator

**Steps:**
```bash
cd ~/code/iqra/frontend
npm install
npx expo start
```

Then press **`i`** in the terminal to open iOS Simulator.

### Option 3: Android Emulator

**Requirements:**
- Android Studio installed
- Android Emulator set up

**Steps:**
```bash
cd ~/code/iqra/frontend
npm install
npx expo start
```

Then press **`a`** in the terminal to open Android Emulator.

### Option 4: Physical Phone (Best for Testing)

**Steps:**
1. Install **Expo Go** app on your phone:
   - iOS: App Store → Search "Expo Go"
   - Android: Play Store → Search "Expo Go"

2. Start Expo:
   ```bash
   cd ~/code/iqra/frontend
   npm install
   npx expo start
   ```

3. Scan QR code:
   - **iOS:** Open Camera app → Point at QR code
   - **Android:** Open Expo Go app → Tap "Scan QR code"

4. The app will load on your phone!

## Quick Start

**Easiest way (Web):**
```bash
cd ~/code/iqra/frontend
npm install
npx expo start --web
```

**Best experience (Phone):**
```bash
cd ~/code/iqra/frontend
npm install
npx expo start
# Then scan QR code with Expo Go app
```

## Troubleshooting

**Expo web not working?**
- React Native web has limited support
- Use iOS Simulator or phone for full features

**iOS Simulator not opening?**
- Install Xcode: `xcode-select --install`
- Or use Android Emulator

**Can't connect phone?**
- Make sure phone and computer are on same WiFi
- Update `frontend/.env` with your Mac's IP:
  ```
  API_BASE_URL=http://YOUR_MAC_IP:8000
  ```

## Differences: Web vs Mobile App

**Web version** (`frontend/web/index.html`):
- ✅ Works immediately in browser
- ✅ Simple HTML/JS
- ✅ All features work
- ⚠️ Not optimized for mobile UI

**Mobile app** (`frontend/App.js`):
- ✅ Native mobile experience
- ✅ Better UI/UX for mobile
- ✅ Can use device features (camera, etc.)
- ⚠️ Requires Expo/React Native setup

## Recommendation

For **development/testing**: Use the web version (already working)
For **mobile experience**: Use Expo Go on your phone (best way to test)

