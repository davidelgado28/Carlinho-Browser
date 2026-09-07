import React, { useRef } from 'react';
import { View, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';

const TELA_INICIAL = '...html do logo...'; 
const INJECTED_JAVASCRIPT = `
  const style = document.createElement('style');
  style.innerHTML = 'body { background-color: #121212 !important; color: #ddd !important; } iframe { display: none !important; }';
  document.head.appendChild(style);
  true;
`;

export default function App() {
  const webviewRef = useRef(null);

  return (
    <View style={styles.container}>
      <WebView
        ref={webviewRef}
        source={{ html: TELA_INICIAL }}
        injectedJavaScript={INJECTED_JAVASCRIPT}
        onShouldStartLoadWithRequest={(request) => {
          const blocklist = ['doubleclick.net', 'analytics'];
          if (blocklist.some(ad => request.url.includes(ad))) {
            return false; 
          }
          return true;
        }}
        thirdPartyCookiesEnabled={false}
        sharedCookiesEnabled={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' } 
});
