package com.carlinho.browser
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
class PrivacyWebViewClient: WebViewClient(){
 private val blockedHosts=setOf("doubleclick.net","googletagmanager.com","google-analytics.com","facebook.net","connect.facebook.net")
 private fun blocked(host:String?)=host?.lowercase()?.trimEnd('.')?.let{h->blockedHosts.any{h==it||h.endsWith(".$it")}}?:false
 override fun shouldInterceptRequest(view:WebView?,request:WebResourceRequest?):WebResourceResponse?=
   if(blocked(request?.url?.host)) WebResourceResponse("text/plain","utf-8",null) else super.shouldInterceptRequest(view,request)
}
