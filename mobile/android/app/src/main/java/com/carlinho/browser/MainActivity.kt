package com.carlinho.browser
import android.os.Bundle
import android.webkit.CookieManager
import android.webkit.WebSettings
import android.webkit.WebView
import androidx.appcompat.app.AppCompatActivity
class MainActivity:AppCompatActivity(){
 override fun onCreate(savedInstanceState:Bundle?){super.onCreate(savedInstanceState);val webView=WebView(this);setContentView(webView)
  webView.settings.apply{javaScriptEnabled=true;domStorageEnabled=false;cacheMode=WebSettings.LOAD_NO_CACHE;setSupportMultipleWindows(false)}
  CookieManager.getInstance().setAcceptCookie(true);CookieManager.getInstance().setAcceptThirdPartyCookies(webView,false)
  webView.webViewClient=PrivacyWebViewClient();webView.loadUrl("https://example.com")
 }
}
