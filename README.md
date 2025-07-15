# MultiWebViewApp: A Multi-WebView Android Application for Debugging & Testing

This project is a simple Android application specifically designed as a **testing use case for QA testers and developers** to verify and debug `WebView` behavior within Android applications. It hosts multiple `WebView` instances within a single activity, providing a controlled environment to understand and practice **Android WebView remote debugging** capabilities using ADB and Chrome DevTools.

## What it Does

`MultiWebViewApp` demonstrates the integration of several `WebView` components into an Android layout. Each WebView is configured to load a different URL, showcasing how multiple web contexts can coexist within one application. Crucially, it includes the necessary configuration to enable remote debugging for all its WebViews, making them discoverable and inspectable via Chrome DevTools.

**Key Features:**

  * **Multiple WebViews:** Displays three distinct `WebView` components simultaneously.

  * **Dynamic Content Loading:** Each WebView loads a different web page (e.g., Google, Android Developers documentation, or a blank page).

  * **Remote Debugging Enabled:** Configured with `WebView.setWebContentsDebuggingEnabled(true)` to allow inspection of WebView content using Chrome DevTools.

## How to Use

Follow these steps to get the `MultiWebViewApp` running on your Android device and begin testing its WebView debugging features.

### Prerequisites

  * **Android Studio:** Installed on your macOS machine.

  * **Android Device/Emulator:** A physical Android device with USB debugging enabled, or an Android Emulator.

  * **ADB (Android Debug Bridge):** Installed and configured in your system's PATH (usually comes with Android Studio).

  * **Google Chrome Browser:** Essential for `chrome://inspect`.

  * **Python 3 (Optional):** For running the continuous polling script.

### Getting Started

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/MultiWebViewApp.git
    cd MultiWebViewApp
    ```

    *(Replace `your-username` with your actual GitHub username)*

2.  **Open in Android Studio:**

      * Launch Android Studio.
      * Select `File > Open...` and navigate to the `MultiWebViewApp` directory you just cloned.
      * Click `Open`. Android Studio will import and sync the project.

3.  **Run on a Device/Emulator:**

      * Connect your Android device via USB and ensure USB debugging is enabled. If using an emulator, launch one.
      * Select your connected device or emulator from the target device dropdown in Android Studio's toolbar.
      * Click the `Run 'app'` button (green triangle icon).
      * The app will build, install, and launch on your device. You should see three distinct WebView areas.

### Important: WebView Debugging Configuration

The `MainActivity.kt` (or `MainActivity.java`) file explicitly includes the line `WebView.setWebContentsDebuggingEnabled(true)`. This line is vital for enabling remote debugging. Without it, your WebViews will not be discoverable by Chrome DevTools.

```kotlin
// In MainActivity.kt (or MainActivity.java)
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        // ...
        WebView.setWebContentsDebuggingEnabled(true) // This line enables debugging
        // ...
    }
}
```

## Use Cases for Testing

This application is ideal for practicing and verifying remote WebView debugging, making it a valuable tool for **QA testers and developers** when working with Android applications that embed web content.

1.  **Remote Debugging with Chrome DevTools:**

      * Ensure the `MultiWebViewApp` is running on your Android device.
      * Open **Google Chrome** on your Mac.
      * Navigate to `chrome://inspect/#devices`.
      * You should see your connected Android device listed. Below it, you will find a section for `MultiWebViewApp` with entries for each debuggable WebView (identified by their loaded URL or title).
      * Click the `inspect` button next to any of the WebViews. A new Chrome DevTools window will open, allowing you to:
          * Inspect the HTML, CSS, and JavaScript of that specific WebView.
          * Use the Console for JavaScript execution and logging.
          * Analyze network requests made by the WebView.
          * Debug JavaScript code.

2.  **Continuous WebView Detection (using Python script):**

      * While the `MultiWebViewApp` is running, use the provided Python script (`webview_poller.py` from the previous interaction) on your Mac.
      * Ensure `chrome://inspect/#devices` is open in your Chrome browser to facilitate the ADB forwarding.
      * Run the script: `python3 webview_poller.py`
      * Observe the script continuously listing the detected debuggable WebViews, their titles, and URLs. This demonstrates how you can programmatically monitor active WebViews.

3.  **Testing Different URL Types:**

      * Modify the `loadUrl()` calls in `MainActivity.kt` (or `MainActivity.java`) to test various types of content:
          * **HTTP/HTTPS URLs:** Load different websites (e.g., `https://www.example.com`, `http://neverssl.com`).
          * **Local HTML:** Load HTML directly from a string or from your app's assets.
            ```kotlin
            // Example of loading local HTML from a string
            webView3.loadData("<html><body><h1>Local HTML Test</h1><p>This content is loaded from a string.</p></body></html>", "text/html", "UTF-8")
            ```
          * **`about:blank`:** Test a completely blank WebView.
      * Observe how each WebView renders and how it appears in Chrome DevTools.

4.  **Observing WebView Behavior:**

      * Interact with the web content in the app (e.g., click links, fill forms if available on the loaded pages).
      * Monitor the DevTools console for JavaScript errors or network activity.
      * Use the "Elements" tab in DevTools to see real-time DOM changes.

## Troubleshooting

  * **"App keeps stopping"**:

      * **Check Logcat first\!** The most common issue is a missing `INTERNET` permission in `AndroidManifest.xml` or an incorrect theme setup (as discussed in previous interactions).
      * Ensure your `AndroidManifest.xml` has `<uses-permission android:name="android.permission.INTERNET"/>` just before the `<application>` tag.
      * Verify your app's theme in `res/values/themes.xml` inherits from `Theme.AppCompat` or `Theme.MaterialComponents`.

  * **WebViews not appearing in `chrome://inspect`**:

      * Confirm `WebView.setWebContentsDebuggingEnabled(true)` is present and executed in your `MainActivity` (or Application class).
      * Ensure USB debugging is enabled on your device and it's properly connected (`adb devices` should list it).
      * Make sure Chrome is open on your Mac, and you've navigated to `chrome://inspect/#devices`.
      * Accept any "Allow USB debugging" prompts on your Android device.

## Contributing

Feel free to fork this repository, make improvements, or add more complex WebView scenarios for testing.
