package com.example.multiwebviewapp

import android.os.Bundle
import android.webkit.WebView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Explicitly disable WebView debugging for security - MULTIPLE LAYERS
        WebView.setWebContentsDebuggingEnabled(false)
        
        val webView1: WebView = findViewById(R.id.webView1)
        val webView2: WebView = findViewById(R.id.webView2)
        val webView3: WebView = findViewById(R.id.webView3)
        
        // Apply security settings to each WebView
        configureWebViewSettings(webView1)
        configureWebViewSettings(webView2)
        configureWebViewSettings(webView3)

        // Configure WebView settings (optional but good practice)
        webView1.settings.javaScriptEnabled = true
        webView2.settings.javaScriptEnabled = true
        webView3.settings.javaScriptEnabled = true

        // Load some content
        webView1.loadUrl("https://www.google.com")
        webView2.loadUrl("https://developer.android.com/develop/ui/views/layout/webapps/webview")
        webView3.loadUrl("about:blank") // You can load a blank page or local HTML here
        // webView3.loadData("<html><body><h1>Local HTML WebView</h1><p>This is from a string.</p></body></html>", "text/html", "UTF-8")
    }
     private fun configureWebViewSettings(webView: WebView) {
        webView.settings.apply {
            javaScriptEnabled = true
            // Additional security settings
            allowFileAccess = false
            allowContentAccess = false
            allowFileAccessFromFileURLs = false
            allowUniversalAccessFromFileURLs = false
        }
    }
}